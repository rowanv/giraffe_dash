from flask import Markup
from sqlalchemy.engine import create_engine
import pandas as pd

class SingleItemResponse:

    def __init__(self, engine, query):
        self.query = query
        self.connection = engine.connect()

    def fetch_result(self):
        self.result = self.connection.execute(self.query)
        self.result = self.result.fetchone()[0]
        return self.result


class TableItemResponse:

    def __init__(self, engine, query):
        self.query = query
        self.engine = engine
        self.connection = engine.connect()

    def fetch_table(self):
        df = pd.read_sql(self.query, self.engine)
        return df

class Vignette:

    def __init__(self, engine, query):
        self.query = query
        self.engine = engine
        self.connection = engine.connect()


class Table(Vignette):

    def __init__(self, engine, query):
        Vignette.__init__(self, engine, query)
        self.response = TableItemResponse(engine, self.query)
        self.df = self.response.fetch_table()

    def get_html_rep(self, columns):
        '''Returns html string representing Table object'''
        result = self.df
        result.index += 1
        result.columns = columns
        result_html = result.to_html(
        classes='table table-bordered table-hover table-striped',
        bold_rows=False)
        return Markup(result_html)


