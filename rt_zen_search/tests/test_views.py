import os
from flask import Flask
from rt_zen_search.db_setup import init_db, add_db_data
from sqlalchemy.orm import sessionmaker
from flask_testing import TestCase
from rt_zen_search import views
from rt_zen_search.models import db, Organizations, Users, Tickets



class BaseTestCase(TestCase):
	"""Base Class that inits our test app and test db."""

	def create_app(self):
		app = Flask(__name__)
		app.config.from_object('config.TestConfig')
		init_db(app.config['SQLALCHEMY_DATABASE_URI'])
		db.init_app(app)
		return app

	def setUp(self):
		db.create_all()

	def tearDown(self):
		db.session.remove()
		db.drop_all()


class ViewsTests(BaseTestCase):
	"""Test for views methods."""

	def test_validated_general_true(self):
		res = views.validated_general("AllGood.")
		self.assertEqual(res, True)

	def test_validated_general_false(self):
		res = views.validated_general("****")
		self.assertEqual(res, False)

class DBTests(BaseTestCase):
	"""Tests for DB."""

	def test_db_init_(self):
		tbl_user = db.session.query(Users)
		tbl_org = db.session.query(Organizations)
		tbl_tickets = db.session.query(Tickets)
		self.assertEqual(tbl_user.all(), [])
		self.assertEqual(tbl_org.all(), [])
		self.assertEqual(tbl_tickets.all(), [])

	def test_db_load(self):
		test_loc = ['rt_zen_search/tests/data_test_files/' + f for f in os.listdir('rt_zen_search/tests/data_test_files')]
		for test_file in test_loc:
			if 'org' in test_file.lower():
				add_db_data(db.session, test_file, Organizations)
			elif 'user' in test_file.lower():
				add_db_data(db.session, test_file, Users)
			elif 'ticket' in test_file.lower():
				add_db_data(db.session, test_file, Tickets)
		db_session.commit()


