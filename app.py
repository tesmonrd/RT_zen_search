import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from rt_zen_search.forms import GeneralSearchBar, OrganizationForm, UserForm, TicketForm
from flask import flash, render_template, request, redirect


app = Flask(__name__, template_folder='rt_zen_search/templates',static_folder='rt_zen_search/static')
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from rt_zen_search.db_setup import init_db, db_session
from rt_zen_search.views import process_query
init_db()


@app.route('/', methods=['GET'])
def index():
	forms = [GeneralSearchBar(),OrganizationForm(),UserForm(),TicketForm()]
	return render_template('forms.html',
		forms=forms,
		search_results=None,
		msg=None
		)


@app.route('/search', methods=['GET'])
def search_results():
	forms = [GeneralSearchBar(),OrganizationForm(),UserForm(),TicketForm()]
	if request.method == 'GET':
		data = request.args.to_dict()
		search_results = process_query(data)
		msg = None
		if not search_results:
			msg = 'No results found! (Queryied Data - data:{})'.format([v for v in data.values() if v])
		if isinstance(search_results, str):
			msg = search_results

		return render_template('forms.html',
			search_results=search_results,
			forms=forms,
			msg=msg
			)


	# search_string = search.data['search']
	# if search.data['search'] == '':
	#     qry = db_session.query(Album)
	#     results = qry.all()
	# if not results:
	#     flash('No results found!')
	#     return redirect('/')
	# else:
	#     # display results
	#     return render_template('results.html', results=results)


if __name__ == '__main__':
	app.run()

