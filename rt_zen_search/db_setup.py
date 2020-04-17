import os
import json
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists, create_database
from rt_zen_search.models import Organizations, Users, Tickets
from rt_zen_search.db_init import create_tables


engine = create_engine(os.environ['DATABASE_URL'], pool_pre_ping=True)
db_session = scoped_session(sessionmaker(autocommit=False,
										 autoflush=False,
										 bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

if not database_exists(engine.url):
	create_database(engine.url)


def init_db():
	"""Initialize database and load if needed."""
	if not inspect(engine).get_table_names():
		create_tables()
		Base.metadata.create_all(bind=engine)
		file_loc = ['rt_zen_search/data/' + f for f in os.listdir('rt_zen_search/data')]
		for json_file in file_loc:
			if 'organizations' in json_file.lower():
				add_db_data(json_file, Organizations)
			elif 'users' in json_file.lower():
				add_db_data(json_file, Users)
			elif 'tickets' in json_file.lower():
				add_db_data(json_file, Tickets)
		db_session.commit()

	else:
		Base.metadata.create_all(bind=engine)


def add_db_data(json_data_loc, target_model):
	"""Extracts JSON and flushes to postgres."""
	with open(json_data_loc, 'r') as f:
		data_dict = json.load(f)
		for data in data_dict:
			if target_model == Tickets and 'type' in data:
				data['type_'] = data.pop('type')
			db_session.add(target_model(**data))
	db_session.flush()





	
