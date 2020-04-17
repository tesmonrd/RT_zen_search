from app import app
from rt_zen_search.db_setup import init_db, db_session
from rt_zen_search.forms import GeneralSearchBar, OrganizationForm, UserForm, TicketForm
from flask import flash, render_template, request, redirect


init_db()

@app.route('/', methods=['GET', 'POST'])
def index():
    gen_search = GeneralSearchBar()
    org_form = OrganizationForm()
    user_form = UserForm()
    ticket_form = TicketForm()

    # if request.method == 'GET':
    #     return search_results(gen_search)

    return render_template('forms.html',
    	gen_search=gen_search,
    	org_form=org_form,
    	user_form=user_form,
    	ticket_form=ticket_form
    	)


@app.route('/search')
def search_results():
    import pdb;pdb.set_trace()

    results = []
    search_string = search.data['search']
    if search.data['search'] == '':
        qry = db_session.query(Album)
    #     results = qry.all()
    # if not results:
    #     flash('No results found!')
    #     return redirect('/')
    # else:
    #     # display results
    #     return render_template('results.html', results=results)


if __name__ == '__main__':
    app.run()