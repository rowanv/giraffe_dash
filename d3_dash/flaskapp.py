from flask import Flask
from collections import Counter
import MySQLdb

from pandas.io.sql import read_sql

app = Flask(__name__)


db_connection = MySQLdb.connect('localhost', 'root', '', 'sakila')


query = 'select staff_id, year(payment_date), month(payment_date), sum(amount) from payment where year(payment_date)=2005 group by staff_id, year(payment_date), month(payment_date) ;'

def execute_query(query, args=()):
	df = read_sql(query, db_connection)
	#db_connection.close()
	return df


@app.teardown_appcontext
def close_connection(exception):
	if db_connection is not None:
		db_connection.close()

@app.route('/viewdb')
def viewdb():
	df = execute_query(query)
	return '<br>'.join(str(x) for x in df.iterrows())


@app.route('/')
def hello_world():
	return 'Hello from Flask!'

@app.route('/countme/<input_str>')
def count_me(input_str):
	input_counter = Counter(input_str)
	response = []
	for letter, count in input_counter.most_common():
		response.append('"{}": {}'.format(letter, count))
	return '<br>'.join(response)

if __name__ == '__main__':
	app.run()