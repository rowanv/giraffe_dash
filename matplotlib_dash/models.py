from sqlalchemy.engine import create_engine
import pandas as pd

class SingleItemResponse(object):

	def __init__(self, engine, query):
		self.query = query
		self.connection = engine.connect()

	def fetch_result(self):
		self.result = self.connection.execute(self.query)
		self.result = self.result.fetchone()[0]
		return self.result


class TableItemResponse(object):

	def __init__(self, engine, query):
		self.query = query
		self.engine = engine
		self.connection = engine.connect()

	def fetch_table(self):
		df = pd.read_sql(self.query, self.engine)
		return df
