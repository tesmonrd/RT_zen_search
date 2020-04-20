import re
from app import db
from distutils.util import strtobool
from itertools import chain
from sqlalchemy import cast, or_, Text
from sqlalchemy.sql.expression import false, true
from rt_zen_search.models import Organizations, Users, Tickets


tbl_map = {'org_id': Organizations,'user_id':Users,'ticket_id':Tickets}
id_field_mod = ['_id','org_id','user_id','ticket_id']
sql_arr_mod = ['domain_names','tags', 'query_all']
type_bool_mod = ['shared_tickets','active','verified','shared','suspended','has_incidents']
type_int_mod = ['organization_id','submitter_id','assignee_id']


def process_query(query_data):
	# import pdb;pdb.set_trace()
	if 'query_all' in query_data and validated_general(query_data['query_all']):
		if len(query_data['query_all'].split(',')) > 1:
			multi_search_val = query_data['query_all'].split(',')
			results = [clean_and_execute({'query_all':s_t},[v for k,v in tbl_map.items()]) for s_t in multi_search_val]
		else:
			results = clean_and_execute(query_data,[v for k,v in tbl_map.items()])
		return results

	elif any(key in id_field_mod for key in query_data.keys()):
		for k in tbl_map.keys():
			if k in query_data.keys():
				results = clean_and_execute(query_data, tbl_map[k])
			return results
			
	else:
		return "Invalid query sent."


def clean_and_execute(query_data, db_table):
	if isinstance(db_table,list):
		result_data = []
		for table in db_table:
			_column_names = table.__table__.c.keys()

			if table == Tickets:
				_column_names = ['ticket_id' if x == '_id' else x for x in _column_names]
			if 'true' in query_data['query_all'].lower() or 'false' in query_data['query_all'].lower():
				_column_names = [bool_f for bool_f in _column_names if bool_f in type_bool_mod]

			_mapped_data = {k:query_data['query_all'] for k in _column_names}
			_cleaned_data = data_corrections({k:v for k,v in _mapped_data.items() if v != ''})
			result_data.append(execute_queries(_cleaned_data,table))

		result_data = list(chain.from_iterable(result_data))
		return result_data

	else:
		_cleaned_data = data_corrections({k:v for k,v in query_data.items() if v != ''})
		result_data = execute_queries(_cleaned_data, db_table)
		return result_data


def execute_queries(cleaned_data, db_table):
	result_data = []
	for attr, value in cleaned_data.items():
		if attr in type_int_mod or attr in type_bool_mod or attr == '_id':
			result_data.append(db_table.query.filter(getattr(db_table, attr).__eq__(value)).all())
		elif attr in sql_arr_mod:
			result_data.append(db_table.query.filter(or_(*[cast(getattr(db_table, attr), Text).contains(x) for x in value])).all())
		else:
			result_data.append(db_table.query.filter(getattr(db_table, attr).ilike(value)).all())

	flattened_data = list(chain.from_iterable(result_data))
	return flattened_data


def data_corrections(cleaned_data):
	"""Correct type issues and handle field modifications."""
	try:
		cleaned_keys = cleaned_data.keys()
		for id_mod in id_field_mod:
			if id_mod in cleaned_keys and 'ticket_id' not in cleaned_keys:
				if not cleaned_data[id_mod].isdigit():
					del cleaned_data[id_mod]
				else:
					cleaned_data['_id'] = int(cleaned_data.pop(id_mod))
			if id_mod in cleaned_keys:
				cleaned_data['_id'] = cleaned_data.pop(id_mod)

		for sql_mod in sql_arr_mod:
			if sql_mod in cleaned_keys:
				cleaned_data[sql_mod] = cleaned_data[sql_mod].split(",")

		for int_mod in type_int_mod:
			if int_mod in cleaned_keys:
				if not cleaned_data[int_mod].isdigit():
					del cleaned_data[int_mod]
				else:
					cleaned_data[int_mod] = int(cleaned_data[int_mod])

		for bool_mod in type_bool_mod:
			if bool_mod in cleaned_keys:
				try:
					if strtobool(cleaned_data[bool_mod]) == 0:
						cleaned_data[bool_mod] = false()
					else:
						cleaned_data[bool_mod] = true()
				except ValueError:
					del cleaned_data[bool_mod]

		return cleaned_data

	except KeyError as e:
		return "Invalid key passed in data: {}".format(e)


def validated_general(query_data):
	"""Basic check for unsafe characters in search."""
	regex = re.compile('[!#$%^&*()<>?\|}{~:]')
	if(regex.search(query_data) == None):
		return True
	else:
		return False

