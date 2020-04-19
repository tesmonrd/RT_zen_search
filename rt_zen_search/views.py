import re
from app import db
from distutils.util import strtobool
from sqlalchemy import cast, or_, Text
from sqlalchemy.sql.expression import false, true
from rt_zen_search.models import Organizations, Users, Tickets


id_field_mod = ['org_id','user_id','ticket_id']
sql_arr_mod = ['domain_names','tags']
type_val_mod = ['shared_tickets','active','verified','shared','has_incidents',
				'organization_id','submitter_id','assignee_id']


def process_query(query_data):
	tbl_map = {'org_id': Organizations,'user_id':Users,'ticket_id':Tickets}
	if 'query_all' in query_data and validated_general(query_data['query_all']):
		create_query(query_data)

	elif 'org_id' in query_data or 'user_id' in query_data or 'ticket_id' in query_data:
		for k in tbl_map.keys():
			if k in query_data.keys():
				create_query(query_data, tbl_map[k])
	else:
		return "Invalid query sent."


def create_query(query_data, db_table=None):
	cleaned_data = {k:v for k,v in query_data.items() if v != ''}
	import pdb;pdb.set_trace()
	if db_table != None:
		cleaned_data = data_corrections(cleaned_data)
		result_data = db_table.query
		for attr, value in cleaned_data.items():
			if attr in type_val_mod or attr == '_id':
				result_data = db_table.query.filter(getattr(db_table, attr).__eq__(value)).all()
			elif attr in sql_arr_mod:
				result_data = db_table.query.filter(or_(*[cast(getattr(db_table, attr), Text).contains(x) for x in value])).all()
			else:
				result_data = db_table.query.filter(getattr(db_table, attr).ilike("%%s%%" % value)).all()


	# 	query = db_table.query
	# 	for f in filter_data:
	# 		_col, _val = f[0], f[1]
	# 		results = query.filter(db_table._col.like(_val))

def validated_general(query_data):
	regex = re.compile('[!#$%^&*()<>?/\|}{~:]')
	if(regex.search(query_data) == None):
		return True
	else:
		return False

def data_corrections(cleaned_data):
	try:
		cleaned_keys = cleaned_data.keys()
		for id_mod in id_field_mod:
			if id_mod in cleaned_keys and 'ticket_id' not in cleaned_keys:
				cleaned_data['_id'] = int(cleaned_data.pop(id_mod))
			if id_mod in cleaned_keys:
				cleaned_data['_id'] = cleaned_data.pop(id_mod)

		for sql_mod in sql_arr_mod:
			if sql_mod in cleaned_keys:
				# cleaned_data[sql_mod] = '{'+cleaned_data[sql_mod]+'}'
				cleaned_data[sql_mod] = cleaned_data[sql_mod].split(",")

		for type_mod in type_val_mod:
			if type_mod in cleaned_keys and '_id' in cleaned_data[type_mod]:
				cleaned_data[type_mod] = int(cleaned_data[type_mod])
			if type_mod in cleaned_keys:
				if strtobool(cleaned_data[type_mod]) == 0:
					cleaned_data[type_mod] = false()
				else:
					cleaned_data[type_mod] = true()


		return cleaned_data
	except KeyError as e:
		return "Invalid key passed in data: {}".format(e)

