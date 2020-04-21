import unittest
from flask import Flask
from flask_testing import TestCase
from rt_zen_search import views
from rt_zen_search.models import *



class BaseTestCase(TestCase):
	"""A"""

	def create_app(self):
		app = Flask(__name__)
		app.config.from_object('config.TestConfig')
		db.init_app(app)
		return app

	def setUp(self):
		db.create_all()

	def tearDown(self):
		db.session.remove()
		db.drop_all()


class DBQueryTests(BaseTestCase):
	def test_validated_general(self):
		res = views.validated_general("****")
		self.assertEquals(res, False)


# if __name__ == '__main__':
#     unittest.main()