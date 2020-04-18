from rt_zen_search.db_setup import db_session
from rt_zen_search.forms import GeneralSearchBar, OrganizationForm, UserForm, TicketForm



def process_query(query_data):
	if 'query_all' in query_data and validated_general(query_data):
    	query_search(data)

    elif 'org_id' in query_data and OrganizationForm(query_data).validate():
    		query_search(data, 'user')
    		
    elif 'user_id' in query_data and UserForm(query_data).validate():
    		query_search(data, 'user')

    elif 'ticket_id' in query_data and TicketForm(query_data).validate():
    		query_search(data, 'org')
    else:
    	return "Invalid query sent."


def validated_general(query_data):
	unsafe = ['<','>','#','%', '{', '}', '|', '^', '~', '[', ']', '`']


def query_search(query_data, db_table=None):

