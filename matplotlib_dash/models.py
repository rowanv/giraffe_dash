from sqlalchemy.engine import create_engine

class SingleItemResponse(object):

	def __init__(self, engine, query):
		self.query = query
		self.connection = engine.connect()

	def fetch_result(self):
		self.result = self.connection.execute(self.query)
		self.result = self.result.fetchone()[0]
		return self.result


