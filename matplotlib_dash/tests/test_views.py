import os
import unittest

from config import basedir
from run import app

class TestCase(unittest.TestCase):
	def setUp(self):
		app.config['TESTING'] = True
		app.config['WTF_CSRF_ENABLED'] = False
		self.app = app.test_client()

	def tearDown(self):
		pass

	def test_index_renders_index_template(self):
		response = self.client.get('/')
		self.assertTemplateUsed(response, 'index.html')

	def test_customers_renders_customers_template(self):
		response = self.client.get('/customers')
		self.assertTemplateUsed(response, 'customers.html')

	def test_employees_renders_employees_template(self):
		response = self.client.get('/employees')
		self.assertTemplateUsed(response, 'employees.html')

	def test_inventory_renders_inventory_template(self):
		response = self.client.get('/inventory')
		self.assertTemplateUsed(response, 'inventory.html')

	#TODO: alltime_sales, recent_sales