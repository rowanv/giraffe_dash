#!/usr/bin/env python

from flask import Flask, make_response
from cStringIO import StringIO
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib.pyplot as plt

import MySQLdb
from pandas.io.sql import read_sql
import pandas as pd

app = Flask(__name__)
db_connection = MySQLdb.connect('localhost', 'root', '', 'sakila')

@app.route('/')
def index():
    return """\
<html>
<body>
<img src="/plot.png">
</body>
</html>"""

@app.route('/plot.png')
def plot():
    query = """\
select sum(amount), payment_date
from payment
group by payment_date
limit 100;
"""
    df = read_sql(query, db_connection)
    df.payment_date = pd.to_datetime(df.payment_date)
    df.set_index('payment_date', inplace=True)
    #df = df.reindex(pd.date_range(min(df.index), max(df.index)), fill_value=0)

    df.plot()
    canvas = FigureCanvas(plt.gcf())
    output = StringIO()
    canvas.print_png(output)
    response = make_response(output.getvalue())
    response.mimetype = 'image/png'
    return response

if __name__ == '__main__':
    app.run(debug=True)