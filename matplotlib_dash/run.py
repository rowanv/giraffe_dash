#!/usr/bin/env python

from flask import Flask, make_response, render_template, send_from_directory, Markup
#from cStringIO import StringIO
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib.pyplot as plt
from matplotlib import rcParams
import seaborn as sns
from flask.ext.bower import Bower

import MySQLdb
from pandas.io.sql import read_sql
import pandas as pd
import brewer2mpl
from math import ceil

#set static folder
app = Flask(__name__, static_url_path='/static/dist')
Bower(app)


db_connection = MySQLdb.connect('localhost', 'root', '', 'sakila')




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


def read_new_orders():
    query = '''
    select sum(amount), payment_date
    from payment
    group by payment_date
    limit 100;
    '''

    df = read_sql(query, db_connection, coerce_float=False)
    df.payment_date = pd.to_datetime(df.payment_date)
    df.set_index('payment_date', inplace=True)
    print(df.head())
    orders_today = df.head(1)['sum(amount)'].iloc[0]
    orders_today = int(ceil(orders_today))
    #TODO: Fix issue with floating point numbers in data transfer
    print(orders_today)
    return orders_today

def indicator_panels(panel_colour, panel_icon, panel_text):
    panel_colour_to_class_mapping = {
        'blue': 'panel-primary',
        'green': 'panel-green',
        'yellow': 'panel-yellow',
        'red': 'panel-red'
    }
    panel_icon_to_class_mapping = {
        'shopping_cart': 'fa-shopping-cart',
        'comments': 'fa-comments',
        'tasks': 'fa-tasks',
        'support': 'fa-support'
    }
    panel_class = panel_colour_to_class_mapping[panel_colour]
    icon_class = panel_icon_to_class_mapping[panel_icon]


    panel_html = '''
                <div class="col-lg-3 col-md-6">
                    <div class="panel {}">
                        <div class="panel-heading">
                            <div class="row">
                                <div class="col-xs-3">
                                    <i class="fa {} fa-5x"></i>
                                </div>
                                <div class="col-xs-9 text-right">
                                    <div class="huge">26</div>
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
    '''.format(panel_class, icon_class, panel_text)
    panel_html = Markup(panel_html)
    return(panel_html)

def morris_line():
    line_graph_html = '''
    <div class="panel panel-default">
                        <div class="panel-heading">
                            <i class="fa fa-bar-chart-o fa-fw"></i> Area Chart Example
                            <div class="pull-right">
                                <div class="btn-group">
                                    <button type="button" class="btn btn-default btn-xs dropdown-toggle" data-toggle="dropdown">
                                        Actions
                                        <span class="caret"></span>
                                    </button>
                                    <ul class="dropdown-menu pull-right" role="menu">
                                        <li><a href="#">Action</a>
                                        </li>
                                        <li><a href="#">Another action</a>
                                        </li>
                                        <li><a href="#">Something else here</a>
                                        </li>
                                        <li class="divider"></li>
                                        <li><a href="#">Separated link</a>
                                        </li>
                                    </ul>
                                </div>
                            </div>
                        </div>
                        <!-- /.panel-heading -->
                        <div class="panel-body">
                            <div id="morris-area-chart"></div>
                        </div>
                        <!-- /.panel-body -->
                    </div>
                    <!-- /.panel -->
    '''
    line_graph_html = Markup(line_graph_html)
    return line_graph_html

#Dashboard Views

@app.route('/')
@app.route('/index.html')
def index(**kwargs):
    context = {'new_orders': read_new_orders(),
                'panels_html': {
                    indicator_panels('blue', 'comments', 'New comments!'),
                    indicator_panels('green', 'tasks', ''),
                    indicator_panels('yellow', 'shopping_cart', ''),
                    indicator_panels('red', 'support', '')},
                'line_graph_html': morris_line(),}
    print('in context')
    print context['panels_html']
    return render_template('index.html', context=context, **kwargs)

@app.route('/customers.html')
def customers(**kwargs):
    context = {
        'panels_html': {
            indicator_panels('blue', 'tasks', 'Total Customers'),
            indicator_panels('green', 'tasks', 'Customers Gained Last Month'),
            indicator_panels('red', 'support', 'Customers Lost Last Month'),
            indicator_panels('yellow', 'shopping_cart', 'Active Customers')
        }
    }
    return render_template('customers.html', context=context, **kwargs)

@app.route('/employees.html')
def employees(**kwargs):
    context = {
        'panels_html': {
            indicator_panels('yellow', 'shopping_cart',
                'Average Sales per Employee'),
            indicator_panels('blue', 'tasks', 'Employee Retention Rate')
        }
    }
    return render_template('employees.html', context=context, **kwargs)

@app.route('/inventory.html')
def inventory(**kwargs):
    context = {
        'panels_html': {
            indicator_panels('blue', 'shopping_cart', 'Films in Inventory'),
            indicator_panels('green', 'shopping_cart', 'Films Checked Out'),
            indicator_panels('yellow', 'tasks', 'Avg. Days Film Checked Out'),
            indicator_panels('red', 'tasks', 'Rentals Returned Late')
        }
    }
    return render_template('inventory.html', context=context, **kwargs)

@app.route('/recent_sales.html')
def recent_sales(**kwargs):
    context = {
        'panels_html': {
            indicator_panels('yellow', 'shopping_cart', 'Sales Last Week'),
            indicator_panels('blue', 'shopping_cart', 'Sales Last Day')
        }
    }
    return render_template('recent_sales.html', context=context, **kwargs)

@app.route('/alltime_sales.html')
def alltime_sales(**kwargs):
    context = {
        'panels_html': {
            indicator_panels('blue', 'shopping_cart', 'All-Time Rentals')
        }
    }
    return render_template('alltime_sales.html', context=context, **kwargs)

#@app.route('/plot1.png')
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

#@app.route('/plot2.png')
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