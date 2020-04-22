import os
import json
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists, create_database
from rt_zen_search.models import Organizations, Users, Tickets
from rt_zen_search.db_init import create_tables


def init_db(db_url):
	"""Initialize database and load if needed."""
	engine = create_engine(db_url, pool_pre_ping=True)
	db_session = scoped_session(sessionmaker(autocommit=False,autoflush=False,bind=engine))
	Base = declarative_base()
	Base.query = db_session.query_property()
	
	try:
		return Base.metadata.create_all(bind=engine)
	except SQLAlchemyError:
		file_loc = ['rt_zen_search/data/' + f for f in os.listdir('rt_zen_search/data')]
		create_tables(db_url)
		load_data(db_session, file_loc)
		Base.metadata.create_all(bind=engine)


def load_data(db_session, file_path):
	"""Handle logic for loading data."""
	for json_file in file_path:
		if 'organizations' in json_file.lower():
			add_db_data(db_session, json_file, Organizations)
		elif 'users' in json_file.lower():
			add_db_data(db_session, json_file, Users)
		elif 'tickets' in json_file.lower():
			add_db_data(db_session, json_file, Tickets)
		else:
			print("File type not found for processing")
			pass
	db_session.commit()

def add_db_data(db_session, json_data_loc, target_model):
	"""Extracts JSON and flushes to postgres."""
	with open(json_data_loc, 'r') as f:
		data_dict = json.load(f)
		for data in data_dict:
			if target_model == Tickets and 'type' in data:
				data['type_'] = data.pop('type')
			db_session.add(target_model(**data))
	return db_session.flush()





	
