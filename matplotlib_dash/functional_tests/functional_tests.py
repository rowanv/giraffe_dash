from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
#import urllib2
from flask import Flask
from flask.ext.testing import LiveServerTestCase


browser = webdriver.Firefox()


class FunctionalTest(LiveServerTestCase):

	def create_app(self):
		app = Flask(__name__)
		app.config['TESTING'] = True
		app.config['LIVESERVER_PORT'] = 8824
		return app
		#from https://pythonhosted.org/Flask-Testing/

	def setUp(self):
		self.browser = webdriver.Firefox()
		self.browser.implicitly_wait(3)

	def tearDown(self):
		self.browser.quit()
