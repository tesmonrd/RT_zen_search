import os
from app import app
from flask import Flask
from sqlalchemy.orm import sessionmaker
from flask_testing import TestCase
from werkzeug import exceptions
from rt_zen_search.db_setup import init_db, load_data, add_db_data
from rt_zen_search.route_bp import bp
from rt_zen_search import views
from rt_zen_search.models import db, Organizations, Users, Tickets


valid_query = {'org_id': '101', 'url': '', 'external_id': '', 'name': '',
				'domain_names': '', 'created_at': '', 'details': '', 'shared_tickets': '', 'tags': ''}
valid_all_query = {'query_all': 'true'}
invalid_query = {'cat': 'meow'}
test_loc = ['rt_zen_search/tests/data_test_files/' + f for f in os.listdir('rt_zen_search/tests/data_test_files')]


class BaseTestCase(TestCase):
	"""Base Class that inits our test app and test db."""

	def create_app(self):
		app = Flask(__name__, template_folder='../templates')
		app.config.from_object('config.TestConfig')
		init_db(app.config['SQLALCHEMY_DATABASE_URI'])
		db.init_app(app)
		app.register_blueprint(bp)
		client = app.test_client()
		return app

	def setUp(self):
		db.create_all()

	def tearDown(self):
		db.session.remove()
		db.drop_all()


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
		load_data(db.session, test_loc)
		self.assertEqual(len(db.session.query(Users).all()), 4)
		self.assertEqual(db.session.query(Users).first().name, 'Francisca Rasmussen')
		self.assertEqual(len(db.session.query(Organizations).all()), 3)
		self.assertEqual(db.session.query(Organizations).first().name, 'Enthaze')
		self.assertEqual(len(db.session.query(Tickets).all()), 5)
		self.assertEqual(db.session.query(Tickets).first().subject, 'A Catastrophe in Korea (North)')

	def test_db_queries_output_valid(self):
		load_data(db.session, test_loc)
		res = views.process_query(valid_query)
		self.assertIn("<td>9270ed79-35eb-4a38-a46f-35725197ea8d</td><td>Enthaze</td>", res[0].__html__())

	def test_db_queries_all(self):
		load_data(db.session, test_loc)
		res = views.process_query(valid_all_query)
		self.assertEqual(len(res), 3)
		self.assertEqual(res[0].__html__(), '<p>No Items</p>')
		self.assertIn("<td>coffeyrasmussen@flotonic.com</td><td>8335-422-718</td><td>Don&#39;t Worry Be Happy", res[1].__html__())
		self.assertIn("<td>A Catastrophe in Hungary</td>", res[2].__html__())

	def test_db_invalid(self):
		load_data(db.session, test_loc)
		with self.assertRaises(exceptions.BadRequest):
			views.process_query(invalid_query)


class ViewsTests(BaseTestCase):
	"""Test for views methods."""

	def test_data_correction(self):
		res1 = views.data_corrections(valid_query)
		self.assertEqual(res1['_id'],101)
		self.assertEqual(res1['tags'],[''])
		self.assertEqual(res1['domain_names'],[''])

	def test_validated_general_true(self):
		res = views.validated_general("AllGood.")
		self.assertEqual(res, True)

	def test_validated_general_false(self):
		res = views.validated_general("****")
		self.assertEqual(res, False)


class RoutesTests(BaseTestCase):
	"""Test Routes."""

	def test_basic_index(self):
		res = self.client.get("/")
		self.assertEqual(res.status_code, 200)

	def test_basic_search(self):
		res = self.client.get("/search?")
		self.assertEqual(res.status_code, 200)

	def test_invalid_method_post(self):
		res = self.client.post("/search")
		self.assertEqual(res.status_code, 405)

	def test_invalid_method_put(self):
		res = self.client.put("/search")
		self.assertEqual(res.status_code, 405)

	def test_invalid_method_delete(self):
		res = self.client.put("/search")
		self.assertEqual(res.status_code, 405)

	def test_valid_search_resp(self):
		res = self.client.get("/search?query_all=101")
		self.assertEqual(res.status_code, 200)

	def test_invalid_search_resp(self):
		res = self.client.get("/search?<script>Malicious;</script>")
		self.assertEqual(res.status_code, 400)

