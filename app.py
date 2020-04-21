import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from rt_zen_search.models import db
from rt_zen_search.forms import GeneralSearchBar, OrganizationForm, UserForm, TicketForm
from flask import flash, render_template, request, redirect
from rt_zen_search.db_setup import init_db
from rt_zen_search.views import process_query


app = Flask(__name__, template_folder='rt_zen_search/templates',static_folder='rt_zen_search/static')
app.config.from_object('config.AppConfig')
init_db(app.config['SQLALCHEMY_DATABASE_URI'])
db.init_app(app)


@app.route('/', methods=['GET'])
def index():
	gen_search = GeneralSearchBar()
	forms = [OrganizationForm(),UserForm(),TicketForm()]
	return render_template('forms_table.html',
		gen_search=gen_search,
		forms=forms,
		search_results=None,
		msg=None
	)


@app.route('/search', methods=['GET'])
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


if __name__ == '__main__':
	app.run()

