from .base import FunctionalTest


class LayoutAndStylingTest(FunctionalTest):

	def test_layout_and_styling(self):

		self.browser.get(self.server_url)
		self.browser.set_window_size(1024, 768)

		#The top navigation bar is rendered
		top_navbar = self.browser.find_element_by_id('top-navbar')
		print(top_navbar)

		#And it is blue (or some equivalent bootstrap test)

