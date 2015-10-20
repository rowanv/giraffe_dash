from flask import Markup
from sqlalchemy.engine import create_engine
import pandas as pd


class ItemResponse:
    '''represents a response to a MySQL query from a database'''

    def __init__(self, engine, query):
        self.query = query
        self.engine = engine
        self.connection = engine.connect()


class SingleItemResponse(ItemResponse):

    def __init__(self, engine, query):
        ItemResponse.__init__(self, engine, query)

    def fetch_result(self):
        self.result = self.connection.execute(self.query)
        self.result = self.result.fetchone()[0]
        return self.result


class TableItemResponse(ItemResponse):

    def __init__(self, engine, query):
        ItemResponse.__init__(self, engine, query)

    def fetch_table(self):
        df = pd.read_sql(self.query, self.engine)
        return df


class Vignette:
    '''Represents a single item of visual representation on dashboard'''

    def __init__(self, engine, query):
        self.query = query
        self.engine = engine
        self.connection = engine.connect()


class IndicatorPanel(Vignette):
    '''Represents an indicator panel vignette in dashboard'''

    def __init__(self, engine, query):
        Vignette.__init__(self, engine, query)
        if query is not None:
            self.panel_num = SingleItemResponse(engine, query).fetch_result()
        self.panel_colour_to_class_mapping = {
            'blue': 'panel-primary',
            'green': 'panel-green',
            'yellow': 'panel-yellow',
            'red': 'panel-red'
        }
        self.panel_icon_to_class_mapping = {
            'shopping_cart': 'fa-shopping-cart',
            'comments': 'fa-comments',
            'tasks': 'fa-tasks',
            'support': 'fa-support'
        }

    def set_values(self, panel_colour, panel_icon, panel_text):
        self.panel_class = self.panel_colour_to_class_mapping[panel_colour]
        self.icon_class = self.panel_icon_to_class_mapping[panel_icon]
        self.panel_text = panel_text

    def get_html_rep(self):
        panel_html = '''
                <div class="col-lg-3 col-md-6">
                    <div class="panel {}">
                        <div class="panel-heading">
                            <div class="row">
                                <div class="col-xs-3">
                                    <i class="fa {} fa-5x"></i>
                                </div>
                                <div class="col-xs-9 text-right">
                                    <div class="huge">{}</div>
                                    <div>{}</div>
                                </div>
                            </div>
                        </div>
                        <a href="#">
                            <div class="panel-footer">
                                <span class="pull-left">View Details</span>
                                <span class="pull-right"><i class="fa fa-arrow-circle-right"></i></span>
                                <div class="clearfix"></div>
                            </div>
                        </a>
                    </div>
                </div>
        '''.format(self.panel_class, self.icon_class,
                   self.panel_num, self.panel_text)
        return Markup(panel_html)


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

    def get_json_rep(self, columns):
        result = self.df
        result.columns = columns
        result_json = result.to_json(orient='records')
        return Markup(result_json)
