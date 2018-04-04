import unittest
from app import app, db, Expression
import requests

class TestAll(unittest.TestCase):

	def setUp(self):
		app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
		app.testing = True
		self.app = app.test_client()
		db.drop_all()
		db.create_all()

	def tearDown(self):
		db.session.remove()
		db.drop_all()

	def test_add(self):
		response = self.app.post('/add', data=dict(expression="2+2"), follow_redirects=True)
		self.assertEqual(response.status_code, 200)
		#self.assertIn(b'4.00 = 2+2', response.data)

	def test_db_store(self):
		self.app.post('/add', data=dict(expression="7+7"), follow_redirects=True)
		result = Expression.query.filter_by(text="7+7").first().text
		self.assertEqual(result,"7+7")

	# def test_invalid_expression(self):
	# 	response = self.app.post('/add', data=dict(expression="2/0"), follow_redirects=True)
	# 	self.assertEqual(response.data, "Division by 0 kills baby whales")

	def test_len_database(self):
		self.app.post('/add', data=dict(expression="7+7"), follow_redirects=True)
		self.app.post('/add', data=dict(expression="1+2"), follow_redirects=True)
		result = len(Expression.query.all())
		self.assertEqual(result, 2)

if __name__ == '__main__':
	unittest.main()


