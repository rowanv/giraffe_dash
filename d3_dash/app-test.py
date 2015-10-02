from app import app
import unittest
import urllib2
from flask import Flask
from flask.ext.testing import LiveServerTestCase

class BasicTestCase(unittest.TestCase):

	def test_index(self):
		'''initial test. Ensure Flask was set up correctly'''
		tester = app.test_client(self)
		response = tester.get('/', content_type='html/text')
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.data, "Hello from Flask!")

	def test_visualization_status_code(self):
		tester = app.test_client(self)
		response = tester.get('/viz', content_type='html/text')
		self.assertEqual(response.status_code, 200)

	def test_d3_visualization_rendered(self):
		tester = app.test_client(self)
		response = tester.get('/viz', content_type='html/text')
		self.assertTrue('svg' in response.data)

if __name__ == '__main__':
	unittest.main()