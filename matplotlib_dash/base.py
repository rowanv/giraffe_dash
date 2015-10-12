from selenium import webdriver
from selenium.webdriver.common.keys import keys
import unittest


browser = webdriver.Firefox()


class NewVisitorTest(unittest.TestCase):

	def setUp(self):
		self.browser = webdriver.Firefox()
		self.browser.implicitly_wait(3)

	def tearDown(self):
		self.browser.quit()

	def test_index_page_resolves():
		
