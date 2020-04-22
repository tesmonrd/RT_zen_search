# ZenSearch - Rick Tesmond

## Overview
Provides a main search bar that will query data that contains ANY data that contains the key words provided. Added in additional functionality to filter on Organizations, Users, and Tickets specifically which preforms an 'AND' type search, so you can get the exact data that you want!

* Built using MacOS and Python 3.6.
* Built using Flask because the microservice-nature of this project is perfect for Flask.
* Attached a POSTGRESQL database because 1) presence of key relationships in the data and 2) postgres is best at handling array fields (yes, I could've just done a json.loads call instead of implementing a DB but whats the fun in that!)

## Installation and Running
###Running the app
*REQUIRES POSTGRESQL (if you don't have it downloaded, please download from: https://www.postgresql.org/download/)*
1. navigate to a new project directory
2. 'git clone' from my master repo: https://github.com/tesmonrd/rt_zen_search.git
3. initialize you virtual environment of choice and activate it... i use 'python -m venv yourenvname'
4. load the requirements from requirements.txt using 'pip install -r requirements.txt'
5. load the environment variables from envs/local.env using 'source envs/local.env'
6. simply run 'flask run' from your commandline and you're off! Simply browse to your localhost:5000 or 127.0.0.1:5000

###Running Tests
1. Once steps are completed for running the app, execute tests by running 'python -m unittest discover'

## Future Dev
1. Do form validation on all fields using jquery dynamically on submit.
2. Have a "AND/OR" toggle in the Advanced Search fields to indicate the kind of search you want to use.
3. Better UI with the advanced search and results tables (maybe present in modal window?).
4. Custom 400 HTTP error handling page


## Other Notes
To expand on the base requirements: 
* Added in the addition "Advanced Search" functionality.
* Decided to attach the postgres DB layer rather than simply run a json.load() and process from there. This is because working with the DB layer is essential in development.
* Built out a full webapp vs a console app.
