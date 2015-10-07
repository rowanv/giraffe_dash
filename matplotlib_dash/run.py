#!/usr/bin/env python

from flask import Flask, make_response, render_template
from cStringIO import StringIO
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib.pyplot as plt
from matplotlib import rcParams
import seaborn as sns
from flask.ext.bower import Bower

import MySQLdb
from pandas.io.sql import read_sql
import pandas as pd
import brewer2mpl

#set static folder
app = Flask(__name__)
Bower(app)


db_connection = MySQLdb.connect('localhost', 'root', '', 'sakila')


#Static file handling


def make_matplotlib_pretty():


    # Set up some better defaults for matplotlib


    #colorbrewer2 Dark2 qualitative color table
    dark2_colors = brewer2mpl.get_map('Dark2', 'Qualitative', 7).mpl_colors

    #rcParams['figure.figsize'] = (3.5, 2.5)
    #rcParams['figure.dpi'] = 150

    rcParams['axes.color_cycle'] = dark2_colors

    rcParams['lines.linewidth'] = 2

    rcParams['axes.facecolor'] = 'white'

    #rcParams['font.size'] = 14
    rcParams['patch.edgecolor'] = 'white'
    rcParams['patch.facecolor'] = dark2_colors[0]
    '''
    rcParams['font.family'] = 'StixGeneral'
    '''

def remove_border(axes=None, top=False, right=False, left=True, bottom=True):
    """
    Minimize chartjunk by stripping out unnecesasry plot borders and axis ticks

    The top/right/left/bottom keywords toggle whether the corresponding plot border is drawn
    """
    ax = axes or plt.gca()
    ax.spines['top'].set_visible(top)
    ax.spines['right'].set_visible(right)
    ax.spines['left'].set_visible(left)
    ax.spines['bottom'].set_visible(bottom)

    #turn off all ticks
    ax.yaxis.set_ticks_position('none')
    ax.xaxis.set_ticks_position('none')

    #now re-enable visibles
    if top:
        ax.xaxis.tick_top()
    if bottom:
        ax.xaxis.tick_bottom()
    if left:
        ax.yaxis.tick_left()
    if right:
        ax.yaxis.tick_right()

make_matplotlib_pretty()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/plot1.png')
def plot1():
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
    df.plot(title='Payments Last 100 Days')
    canvas = FigureCanvas(plt.gcf())
    output = StringIO()
    canvas.print_png(output)
    response = make_response(output.getvalue())
    response.mimetype = 'image/png'
    return response

@app.route('/plot2.png')
def plot2():


    query = '''select staff_id, year(payment_date), month(payment_date),
    sum(amount) from payment
    where year(payment_date)=2005 group by staff_id, year(payment_date), month(payment_date) ;
    '''

    df = read_sql(query, db_connection)
    fig, ax = plt.subplots()


    for employee in range(1,3):
        current_data = df[df['staff_id']==employee]
        dates = current_data['month(payment_date)']
        ax.plot(dates, current_data['sum(amount)'], label='Employee: {0}'.format(employee))

    plt.xlabel('Month')
    plt.ylabel('Sales')
    plt.title('Sales by Employee Over Time')
    ax.legend()

    canvas = FigureCanvas(plt.gcf())
    output = StringIO()
    canvas.print_png(output)
    response = make_response(output.getvalue())
    response.mimetype = 'image/png'
    return response




if __name__ == '__main__':
    app.run(debug=True)