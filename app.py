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
	gen_search = GeneralSearchBar()
	org_form = OrganizationForm()
	user_form = UserForm()
	ticket_form = TicketForm()

	return render_template('forms.html',
		gen_search=gen_search,
		org_form=org_form,
		user_form=user_form,
		ticket_form=ticket_form
		)


@app.route('/search', methods=['GET'])
def search_results():
	import pdb;pdb.set_trace()
	if request.method == 'GET':
		data = request.args.to_dict()
		search_results = process_query(data)
		return render_template('results_tbl.html', search_results=search_results)


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

