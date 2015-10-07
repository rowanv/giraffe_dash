query_movies_currently_out = '''select * from rental
						where return_date is null;'''

query_movies_returned_last_day = '''select *
from rental
where date(return_date) = (select date(max(return_date)) from rental);'''

query_movie_inventory_by_category = '''select fc.category_id, name, count(*)
from film_category fc join category c on fc.category_id = c.category_id
group by fc.category_id, name'''

query_movie_inventory_by_language = '''select l.language_id, l.name,
count(*) from language l
join film on l.language_id = film.language_id
group by l.language_id, l.name;'''

query_sales_by_movie = '''select *
from sales_by_film_category;'''

query_sales_by_store = '''select *
from sales_by_store ss join
group by store_id
TODO: Finish'''

query_customer_by_country = '''
select country, count(*) as number_customers
from customer_list
group by country
order by number_customers desc'''

query_staff_sales_last_3_months = '''
select staff_id, year(payment_date), month(payment_date),
    sum(amount) from payment
    where year(payment_date)=2005 group by staff_id, year(payment_date), month(payment_date) ;
'''

query_payments_by_date = '''
select sum(amount), payment_date
from payment
group by payment_date
limit 100;
'''

query_length_time_movies_rented = '''
select DATEDIFF(return_date, rental_date) from rental;
'''

query_avg_length_time_movies_rented = '''
select AVG(DATEDIFF(return_date, rental_date)) from rental;
'''

query_number_rentals_returned_late = '''select count(*)
from (
	select datediff(return_date, rental_date) rental_length
	from rental where datediff(return_date, rental_date) > 7) a;'''

