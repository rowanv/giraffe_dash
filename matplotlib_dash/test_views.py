import os
import unittest
from flask import Flask
from flask.ext.bower import Bower
from flask.ext.testing import LiveServerTestCase
from selenium import webdriver
from urllib.request import urlopen
from run import app




class TestCase(LiveServerTestCase):
	def create_app(self):
		#app = Flask(__name__, static_url_path='/static/dist')
		app.config['TESTING'] = True
		return app

	def setUp(self):
		self.driver = webdriver.Firefox()

	def tearDown(self):
		self.driver.close()

	def test_index_renders_index_template(self):
		response = urlopen(self.get_server_url())
		self.assertEqual(response.code, 200)
		#self.assertTemplateUsed('index.html')


	def test_customers_renders_customers_template(self):
		response = urlopen(self.get_server_url() + '/customers.html')
		self.assertEqual(response.code, 200)
		#self.assertTemplateUsed(response, 'customers.html')

	def test_employees_renders_employees_template(self):
		response = urlopen(self.get_server_url() + '/employees.html')
		self.assertEqual(response.code, 200)

	def test_sales_all_time_renders_sales_all_time_template(self):
		response = urlopen(self.get_server_url() + '/alltime_sales.html')
		self.assertEqual(response.code, 200)

	def test_recent_sales_renders_recent_sales_template(self):
		response = urlopen(self.get_server_url() + '/recent_sales.html')
		self.assertEqual(response.code, 200)
		#self.assertTemplateUsed(response, 'employees.html')

	def test_inventory_renders_inventory_template(self):
		response = urlopen(self.get_server_url() + '/inventory.html')
		self.assertEqual(response.code, 200)
		#self.assertTemplateUsed(response, 'inventory.html')



if __name__ == '__main__':
	unittest.main()