from sqlalchemy.engine import create_engine

engine = create_engine('mysql+pymysql://root@localhost/sakila')
connection = engine.connect()

result = connection.execute('''
    select sum(amount), payment_date
    from payment
    group by payment_date
    limit 100;
    '''
	)
for row in result:
	print(row)

