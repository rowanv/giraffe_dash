#!/usr/bin/env python
from flask import Flask, make_response, render_template, send_from_directory, Markup
from flask.ext.bower import Bower

from sqlalchemy.engine import create_engine
from pandas.io.sql import read_sql
import pandas as pd
import brewer2mpl
from math import ceil

from models import SingleItemResponse

#set static folder
app = Flask(__name__, static_url_path='/static/dist')
Bower(app)




engine = create_engine('mysql+pymysql://root@localhost/sakila')
#db_connection = engine.connect()



def read_new_orders():
    query = '''
    select sum(amount), payment_date
    from payment
    group by payment_date
    limit 100;
    '''

    df = read_sql(query, engine, coerce_float=False)
    df.payment_date = pd.to_datetime(df.payment_date)
    df.set_index('payment_date', inplace=True)
    print(df.head())
    orders_today = df.head(1)['sum(amount)'].iloc[0]
    orders_today = int(ceil(orders_today))
    #TODO: Fix issue with floating point numbers in data transfer
    print(orders_today)
    return orders_today

def read_avg_length_time_checked_out():
    query_avg_length_time_movies_rented = '''
    select AVG(DATEDIFF(return_date, rental_date)) from rental;
    '''
    response = SingleItemResponse(engine,
        query_avg_length_time_movies_rented)
    result = response.fetch_result()
    return result

def read_rentals_returned_late():
    query_number_rentals_returned_late = '''
    select count(*)
    from (
    select datediff(return_date, rental_date) rental_length
    from rental where datediff(return_date, rental_date) > 7) a;'''
    response = SingleItemResponse(engine,
        query_number_rentals_returned_late)
    result = response.fetch_result()
    return result

def read_films_checked_out():
    query_films_checked_out = '''
    select count(*)
    from (
    select *
    from rental
    where return_date is null) a;
    '''
    response = SingleItemResponse(engine,
        query_films_checked_out)
    result = response.fetch_result()
    return result

def read_films_in_inventory():
    query_films_in_inventory = '''
    select count(*)
    from (
    select f.film_id, count(*)
    from film f join inventory i on f.film_id = i.film_id
    group by f.film_id) a;
    '''
    response = SingleItemResponse(engine,
    query_films_in_inventory)
    result = response.fetch_result()
    return result

#Chart Views
def indicator_panels(panel_colour, panel_icon, panel_text, panel_num):
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
    '''.format(panel_class, icon_class, panel_num, panel_text)
    panel_html = Markup(panel_html)
    return(panel_html)

def morris_line():
    '''
    chart_id: id element for html
    chart_data: data in JSON format
        returns: tuple with HTML data for chart , JS script for chart
    '''
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
    context = {'panels_html': [
                    indicator_panels('blue', 'comments',
                        'New Orders!', read_new_orders()),
                    indicator_panels('green', 'tasks', '', ''),
                    indicator_panels('yellow', 'shopping_cart',
                        'Films Checked Out', read_films_checked_out()),
                    indicator_panels('red', 'support', '', '')
                ],
                'line_graph_html': morris_line(),
            }
    return render_template('index.html', context=context, **kwargs)

@app.route('/customers.html')
def customers(**kwargs):
    context = {
        'panels_html': [
            indicator_panels('blue', 'tasks', 'Total Customers', ''),
            indicator_panels('green', 'tasks',
                'Customers Gained Last Month', ''),
            indicator_panels('red', 'support',
                'Customers Lost Last Month', ''),
            indicator_panels('yellow', 'shopping_cart',
                'Active Customers', '')
        ]
    }
    return render_template('customers.html', context=context, **kwargs)

@app.route('/employees.html')
def employees(**kwargs):
    context = {
        'panels_html': {
            indicator_panels('yellow', 'shopping_cart',
                'Average Sales per Employee', ''),
            indicator_panels('blue', 'tasks',
                'Employee Retention Rate', '')
        }
    }
    return render_template('employees.html', context=context, **kwargs)

@app.route('/inventory.html')
def inventory(**kwargs):
    context = {
        'panels_html': [
            indicator_panels('blue', 'shopping_cart',
                'Films in Inventory', read_films_in_inventory()),
            indicator_panels('green', 'shopping_cart',
                'Films Checked Out', read_films_checked_out()),
            indicator_panels('yellow', 'tasks',
                'Avg. Days Film Checked Out',
                read_avg_length_time_checked_out()),
            indicator_panels('red', 'tasks',
                'Rentals Returned Late', read_rentals_returned_late())
        ]
    }
    return render_template('inventory.html', context=context, **kwargs)

@app.route('/recent_sales.html')
def recent_sales(**kwargs):
    context = {
        'panels_html': [
            indicator_panels('yellow', 'shopping_cart',
                'Sales Last Week', ''),
            indicator_panels('blue', 'shopping_cart',
                'Sales Last Day', '')
        ]
    }
    return render_template('recent_sales.html', context=context, **kwargs)

@app.route('/alltime_sales.html')
def alltime_sales(**kwargs):
    context = {
        'panels_html': [
            indicator_panels('blue', 'shopping_cart',
                'All-Time Rentals', '')
        ]
    }
    return render_template('alltime_sales.html', context=context, **kwargs)




if __name__ == '__main__':
    app.run(debug=True)