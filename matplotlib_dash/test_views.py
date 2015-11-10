import os
import unittest
from run import app

class HomePageTest(unittest.TestCase):

	def setUp(self):
		self.tester = app.test_client(self)

	def test_home_page_contains_indicator_panels(self):
		response = self.tester.get('/')
		assert 'Customer Retention Rate' in response.data.decode('UTF-8')

	def test_home_page_contains_active_customers_vingette(self):
		response = self.tester.get('/')
		assert 'Active vs. Inactive Customers' in response.data.decode('UTF-8')

	def test_recent_sales_contains_indicator_panels(self):
		response = self.tester.get('/recent_sales.html')
		assert 'Sales Last Week' in response.data.decode('UTF-8')

	def test_recent_sales_contains_vingettes(self):
		response = self.tester.get('/recent_sales.html')
		assert 'Sales Over Time: Last Month' in response.data.decode('UTF-8')


	def test_all_time_sales_contains_indicator_panels(self):
		response = self.tester.get('/alltime_sales.html')
		assert 'All-Time Rentals' in response.data.decode('UTF-8')
		assert 'All-Time Sales' in response.data.decode('UTF-8')

	def test_all_time_sales_contains_vingettes(self):
		response = self.tester.get('/alltime_sales.html')
		assert 'All-Time Sales per Unit in Stock, by Genre' in response.data.decode('UTF-8')
		assert 'Avg. All-Time Sales per Unit in Stock' in response.data.decode('UTF-8')

	def test_employees_contains_indicator_panels(self):
		response = self.tester.get('/employees.html')
		assert 'Average Sales per Employee' in response.data.decode('UTF-8')

	def test_employees_contains_vignettes(self):
		response = self.tester.get('/employees.html')
		assert 'Sales Over Time (Months) by Employee' in response.data.decode('UTF-8')

	def test_customers_contains_indicator_panels(self):
		response = self.tester.get('/customers.html')
		assert 'Active Customers' in response.data.decode('UTF-8')

	def test_customers_contains_vignettes(self):
		response = self.tester.get('/customers.html')
		assert 'Active vs. Inactive Customers' in response.data.decode('UTF-8')

	def test_inventory_contains_indicator_panels(self):
		response = self.tester.get('/inventory.html')
		assert 'Film Titles in Inventory' in response.data.decode('UTF-8')

	def test_inventory_contains_vignettes(self):
		response = self.tester.get('/inventory.html')
		assert 'Inventory by Genre' in response.data.decode('UTF-8')



if __name__ == '__main__':
	unittest.main()