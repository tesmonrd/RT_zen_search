from flask import Blueprint
from rt_zen_search.views import process_query
from rt_zen_search.forms import GeneralSearchBar, OrganizationForm, UserForm, TicketForm
from flask import flash, render_template, request, redirect


bp = Blueprint('rt_zen_search', __name__)

@bp.route('/', methods=['GET'])
def index():
	gen_search = GeneralSearchBar()
	forms = [OrganizationForm(),UserForm(),TicketForm()]
	return render_template('forms_table.html',
		gen_search=gen_search,
		forms=forms,
		search_results=None,
		msg=None
	)

@bp.route('/search', methods=['GET'])
def search_results():
	gen_search = GeneralSearchBar()
	forms = [OrganizationForm(),UserForm(),TicketForm()]
	if request.method == 'GET':
		data = request.args.to_dict()
		search_results = process_query(data)
		if not search_results:
			msg = 'No results found! (Queried Data - data:{})'.format([v for v in data.values() if v])
			search_results=None
		else:
			res_ct = 0
			for tbl in search_results:
				if "No Items" in tbl.__html__():
					search_results.remove(tbl)
				else:
					res_ct += tbl.__html__().count('<tr>') - 1
			msg = '{} Results found for search {}.'.format(res_ct,[v for v in data.values() if v])

		return render_template('forms_table.html',
			gen_search=gen_search,
			search_results=search_results,
			forms=forms,
			msg=msg
		)