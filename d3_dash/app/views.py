from app import app



from collections import Counter
from flask import Flask
import MySQLdb
import pandas as pd

from pandas.io.sql import read_sql





query = '''select staff_id, year(payment_date), month(payment_date), sum(amount)
from payment
where year(payment_date)=2005
group by staff_id, year(payment_date), month(payment_date) ;
'''

def execute_query(query, args=()):
	db_connection = MySQLdb.connect('localhost', 'root', '', 'sakila')
	df = read_sql(query, db_connection)
	db_connection.close()
	#db_connection.close()
	return df




@app.route('/viewdb')
def viewdb():
	df = execute_query(query)
	df.to_csv('app/static/data.csv')
	return('Wrote the dataset')


@app.route('/viz')
def visualization():
	df = execute_query(query)
	df.to_csv('app/static/data.csv')
	page = '''<html>
	<head>
		<link rel='stylesheet' type='text/css' href='/static/nv.d3.css'>
	</head>
	<body>
	</body>
	<script src="/static/d3.v3.min.js"  charset="utf-8"></script>
	<script src='/static/nv.d3.min.js' charset='utf-8'></script>

	<script type="text/javascript" src='/static/viz.js'></script>
	</html>'''
	return page


@app.route('/')
@app.route('/index')
def hello_world():
	return 'Hello from Flask!'

@app.route('/countme/<input_str>')
def count_me(input_str):
	input_counter = Counter(input_str)
	response = []
	for letter, count in input_counter.most_common():
		response.append('"{}": {}'.format(letter, count))
	return '<br>'.join(response)
