query_movies_currently_out = '''select * from rental
						where return_date is null;'''

query_movies_returned_last_day = '''select *
from rental
where date(return_date) = (select date(max(return_date)) from rental);'''

query_movie_inventory_by_category = '''select fc.category_id, name, count(*)
from film_category fc join category c on fc.category_id = c.category_id
group by fc.category_id, name'''

query_sales_by_movie_category = '''
select fc.category_id, c.name, sum(amount)
from film_category fc join category c
on fc.category_id = c.category_id
join film on film.film_id = fc.film_id
join inventory i on i.film_id = film.film_id
join rental on rental.inventory_id = i.inventory_id
join payment on payment.rental_id = rental.rental_id
group by fc.category_id, c.name
'''

query_movie_inventory_by_language = '''select l.language_id, l.name,
count(*) from language l
join film on l.language_id = film.language_id
group by l.language_id, l.name;'''

query_sales_by_genre = '''select *
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

query_payments_by_date_month = '''
select year(payment_date), month(payment_date), day(payment_date),
sum(amount)
from payment
where month(payment_date) = 7
group by year(payment_date), month(payment_date), day(payment_date)
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

query_films_checked_out = '''
select count(*)
from (
select *
from rental
where return_date is null) a;
'''

query_customers_rental_overdue = '''
SELECT CONCAT(customer.last_name, ', ', customer.first_name) AS customer,
address.phone, film.title
FROM rental INNER JOIN customer ON rental.customer_id = customer.customer_id
INNER JOIN address ON customer.address_id = address.address_id
INNER JOIN inventory ON rental.inventory_id = inventory.inventory_id
INNER JOIN film ON inventory.film_id = film.film_id
WHERE rental.return_date IS NULL
AND rental_date + INTERVAL film.rental_duration DAY < CURRENT_DATE()
LIMIT 5;
'''

query_rental_by_staff = '''
select staff_id, year(rental_date), month(rental_date), count(*)
from rental
where year(rental_date) = 2005
group by staff_id, year(rental_date), month(rental_date);
'''

query_avg_rental_by_staff = '''
select avg(total_rented) from (select count(*) as total_rented
	from rental
	group by staff_id) a;
'''

query_top_rented_films = '''
select f.film_id, f.title, f.release_year, count(*) as number_rentals
from film f join inventory
on inventory.film_id = f.film_id
join rental on rental.inventory_id = inventory.inventory_id
group by f.film_id, f.title, f.release_year
order by number_rentals desc
limit 50;
'''



