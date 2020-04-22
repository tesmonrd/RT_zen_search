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
		msg = None
		data = request.args.to_dict()
		search_results = process_query(data)
		if not search_results:
			msg = 'No results found! (Queryied Data - data:{})'.format([v for v in data.values() if v])
		if isinstance(search_results, str):
			msg = search_results

		return render_template('forms_table.html',
			gen_search=gen_search,
			search_results=search_results,
			forms=forms,
			msg=msg
		)