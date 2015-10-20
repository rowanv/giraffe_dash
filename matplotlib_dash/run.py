#!/usr/bin/env python
from flask import Flask, make_response, render_template, send_from_directory, Markup
from flask.ext.bower import Bower

from sqlalchemy.engine import create_engine
from pandas.io.sql import read_sql
import pandas as pd
import brewer2mpl
from math import ceil

from models import SingleItemResponse, TableItemResponse, Table, IndicatorPanel
import queries as q

# set static folder
app = Flask(__name__, static_url_path='/static/dist')
Bower(app)


engine = create_engine('mysql+pymysql://root@localhost/sakila')
connection = engine.connect()

#TODO:
# - Fix time labels on sales: recent: sales over time graph
# - Add chart to overview page
# Add 3 tables to overview page
# Deploy
# Handle disconnect from db

# Read up on flask-sqlalchemy vs. pure sqlalchemy
# - Add all-time sales chart
# Then fix all-time sales layout
# Implement search functionality
# Change messages from lorem ipsum
# Add table to recent sales

##############
# Customers
##############


def read_customers_added_last_month():
    response = SingleItemResponse(connection,
                                  q.query_customers_added_last_month)
    result = response.fetch_result()
    return result

def read_customers_lost_last_month():
    response = SingleItemResponse(connection,
                                  q.query_customers_lost_last_month)
    result = response.fetch_result()
    return result

def read_number_active_customers():
    response = SingleItemResponse(connection,
                                  q.query_active_customers)
    result = response.fetch_result()
    return result

def calc_customer_retention_rate():
    cust_added = read_customers_added_last_month()
    cust_lost = read_customers_lost_last_month()
    retention_rate = 100 * cust_added / (cust_added + cust_lost)
    retention_rate = '%.2f' % (retention_rate)
    return str(retention_rate) + '%'

def read_customers_by_country():
    this_table = Table(connection, q.query_customers_by_country)
    columns = ['Country', 'Number of Customers']
    html_rep = this_table.get_html_rep(columns)
    return html_rep

def read_customers_lost_by_country():
    this_table = Table(connection, q.query_customers_lost_by_country)
    columns = ['Country', 'Number of Customers Lost']
    html_rep = this_table.get_html_rep(columns)
    return html_rep

##########
# Sales
##########

def read_sales_by_genre():
    this_table = Table(connection, q.query_sales_by_movie)
    columns = ['Category', 'Total Sales']
    html_rep = this_table.get_html_rep(columns)
    return html_rep

def read_sales_last_month_over_time():
    table = Table(connection, q.query_payments_by_date_month)
    table.df = table.df[['day(payment_date)', 'sum(amount)']]
    columns = ['Day', 'Payments']
    result_json = table.get_json_rep(columns)
    return result_json


################
# Inventory
################

def read_films_in_inventory_by_category():
    table = Table(connection, q.query_movie_inventory_by_category)
    columns = ['Category', 'Inventory Count']
    table.df = table.df[['name', 'count(*)']]
    result_json = table.get_json_rep(columns)
    return result_json

def read_films_in_inventory_by_store():
    table = Table(connection, q.query_films_in_inventory_by_store)
    columns = ['Store ID', 'Number of Films']
    result_json = table.get_json_rep(columns)
    return result_json

def read_films_in_inventory_most_rented():
    this_table = Table(connection, q.query_top_rented_films)
    columns = ['Film ID', 'Title', 'Release Year', 'Number of Rentals']
    html_rep = this_table.get_html_rep(columns)
    return html_rep


############
# Staff / Employee
############

def read_sales_by_employee_over_time():
    table = Table(connection, q.query_rental_by_staff)
    table.df = table.df[['staff_id', 'month(rental_date)', 'total_sales']]
    table.df = table.df.pivot(index='month(rental_date)',
                          columns='staff_id', values='total_sales')
    table.df = table.df.reset_index()
    result_json = table.df.to_json(orient='records')
    return Markup(result_json)

################
# Chart Views
################


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


# Dashboard Views

@app.route('/')
@app.route('/index.html')
def index(**kwargs):

    green_panel = IndicatorPanel(connection, None)
    green_panel.set_values('green', 'comments', 'New Orders!')
    green_panel.panel_num = ('1')
    red_panel = IndicatorPanel(connection, q.query_customers_lost_last_month)
    red_panel.set_values('red', 'support', 'Customers Lost Last Month')
    blue_panel = IndicatorPanel(connection, None)
    blue_panel.set_values('blue', 'tasks', 'Customer Retention Rate')
    blue_panel.panel_num = calc_customer_retention_rate()
    yellow_panel = IndicatorPanel(connection, q.query_films_checked_out)
    yellow_panel.set_values('yellow', 'shopping_cart', 'Films Checked Out')

    context = {'panels_html': [
        blue_panel.get_html_rep(),
        green_panel.get_html_rep(),
        yellow_panel.get_html_rep(),
        red_panel.get_html_rep(),
    ],
        'line_graph_html': morris_line(),
        'donut_chart': {'active_customers':
                        read_number_active_customers(),
                        'inactive_customers':
                        read_customers_lost_last_month(),
                        },
    }
    return render_template('index.html', context=context, **kwargs)


@app.route('/customers.html')
def customers(**kwargs):
    yellow_panel = IndicatorPanel(connection, q.query_active_customers)
    yellow_panel.set_values('yellow', 'shopping_cart', 'Active Customers')
    green_panel = IndicatorPanel(connection, q.query_customers_added_last_month)
    green_panel.set_values('green', 'tasks', 'Customers Gained Last Month')
    red_panel = IndicatorPanel(connection, q.query_customers_lost_last_month)
    red_panel.set_values('red', 'support', 'Customers Lost Last Month')
    blue_panel = IndicatorPanel(connection, None)
    blue_panel.set_values('blue', 'tasks', 'Customer Retention Rate')
    blue_panel.panel_num = calc_customer_retention_rate()
    context = {
        'panels_html': [
            yellow_panel.get_html_rep(),
            green_panel.get_html_rep(),
            red_panel.get_html_rep(),
            blue_panel.get_html_rep(),

        ],
        'customer_origin_table': read_customers_by_country(),
        'customer_lost_origin_table': read_customers_lost_by_country(),
        'donut_chart': {'active_customers':
                        read_number_active_customers(),
                        'inactive_customers':
                        read_customers_lost_last_month(),
                        },
    }
    return render_template('customers.html', context=context, **kwargs)


@app.route('/employees.html')
def employees(**kwargs):
    blue_panel = IndicatorPanel(connection, None)
    blue_panel.set_values('blue', 'tasks', 'Employee Retetention Rate')
    blue_panel.panel_num = ('100%')
    yellow_panel = IndicatorPanel(connection, q.query_avg_rental_by_staff)
    yellow_panel.set_values('yellow', 'shopping_cart',
                            'Average Sales per Employee')
    yellow_panel.panel_num = '%0.0f' % yellow_panel.panel_num
    yellow_panel.panel_num = '$' + str(yellow_panel.panel_num)
    context = {
        'panels_html': [
            yellow_panel.get_html_rep(),
            blue_panel.get_html_rep()
        ],
        'sales_by_employee_table': read_sales_by_employee_over_time(),
    }
    return render_template('employees.html', context=context, **kwargs)


@app.route('/inventory.html')
def inventory(**kwargs):
    blue_panel = IndicatorPanel(connection, q.query_films_in_inventory)
    blue_panel.set_values('blue', 'shopping_cart',
                          'Film Titles in Inventory')
    green_panel = IndicatorPanel(connection, q.query_films_checked_out)
    green_panel.set_values('green', 'shopping_cart', 'Films Checked Out')
    yellow_panel = IndicatorPanel(connection,
                                  q.query_avg_length_time_movies_rented)
    yellow_panel.set_values('yellow', 'tasks',
                            'Avg. Days Film Checked Out')
    yellow_panel.panel_num = '%.2f' % green_panel.panel_num
    red_panel = IndicatorPanel(connection,
                               q.query_number_rentals_returned_late)
    red_panel.set_values('red', 'tasks', 'Rentals Returned Late')
    context = {
        'panels_html': [
            blue_panel.get_html_rep(),
            green_panel.get_html_rep(),
            yellow_panel.get_html_rep(),
            red_panel.get_html_rep(),
        ],
        'table_films_by_category': read_films_in_inventory_by_category(),
        'table_films_by_store': read_films_in_inventory_by_store(),
        'table_top_rented_films': read_films_in_inventory_most_rented(),
    }
    return render_template('inventory.html', context=context, **kwargs)


@app.route('/recent_sales.html')
def recent_sales(**kwargs):
    blue_panel = IndicatorPanel(connection, q.query_sales_last_week)
    blue_panel.set_values('blue', 'shopping_cart', 'Sales Last Week')
    blue_panel.panel_num = '$' + str(blue_panel.panel_num)
    yellow_panel = IndicatorPanel(connection, q.query_sales_last_day)
    yellow_panel.set_values('yellow', 'shopping_cart', 'Sales Last Day')
    context = {
        'panels_html': [
            blue_panel.get_html_rep(),
            yellow_panel.get_html_rep(),
        ],
        'sales_last_month_json': read_sales_last_month_over_time(),
    }
    return render_template('recent_sales.html', context=context, **kwargs)


@app.route('/alltime_sales.html')
def alltime_sales(**kwargs):
    blue_panel = IndicatorPanel(connection, q.query_rentals_all_time)
    blue_panel.set_values('blue', 'shopping_cart', 'All-Time Rentals')
    yellow_panel = IndicatorPanel(connection, q.query_sales_all_time)
    yellow_panel.set_values('yellow', 'shopping_cart', 'All-Time Sales')
    yellow_panel.panel_num = '$ ' + str(yellow_panel.panel_num)
    context = {
        'panels_html': [
            blue_panel.get_html_rep(),
            yellow_panel.get_html_rep(),
        ],
        'sales_by_genre_table': read_sales_by_genre(),
    }
    return render_template('alltime_sales.html', context=context, **kwargs)


if __name__ == '__main__':
    app.run(debug=True)
