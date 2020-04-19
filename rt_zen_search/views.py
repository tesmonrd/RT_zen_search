import re
from app import db
from rt_zen_search.models import Organizations, Users, Tickets



def process_query(query_data):
	tbl_map = {'org_id': Organizations,'user_id':Users,'ticket_id':Tickets}
	if 'query_all' in query_data and validated_general(query_data['query_all']):
		query_search(query_data)

	elif 'org_id' in query_data or 'user_id' in query_data or 'ticket_id' in query_data:
		for k in tbl_map.keys():
			if k in query_data.keys():
				query_search(query_data, tbl_map[k])
	else:
		return "Invalid query sent."


def query_search(query_data, db_table=None):
	cleaned_data = {k:v for k,v in query_data.items() if v != ''}
	if db_table != None:
		data_field_mod = ['org_id','user_id','ticket_id']
		sql_arr_mod = ['domain_names','tags']
		for key_mod in data_field_mod:
			if key_mod in cleaned_data.keys():
				cleaned_data['_id'] = cleaned_data.pop(key_mod)

		for sql_mod in sql_arr_mod:
			if sql_mod in cleaned_data.keys():
				cleaned_data[sql_mod] = '{'+cleaned_data[sql_mod]+'}'

		results = db_table.query.filter_by(**cleaned_data).all()
	# else:
	# 	results = []
	# 	for table in list(Organizations,Users,Tickets):
	# 		results = db_table.query.filter_by(**query_data).all()

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

