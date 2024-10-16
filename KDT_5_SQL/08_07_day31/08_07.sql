use sakila;

select customer_id, count(*) from rental
group by customer_id;

select customer_id, count(*) from rental
group by customer_id
order by 2 desc;

select customer_id, count(*) from rental
group by customer_id
order by count(*) desc;

select customer_id, count(*) from rental
group by customer_id
having count(*) >= 40;

select max(amount) as max_amt, 
min(amount) as min_amt,
avg(amount) as avg_amt,
sum(amount) as tot_amt,
count(*) as num_payments
from payment;     

select customer_id, 
max(amount) as max_amt, 
min(amount) as min_amt, 
avg(amount) as avg_amt,
sum(amount) as tot_amt,
count(*) as num_payments
from payment
group by customer_id

select count(customer_id) as num_rows,
count(distinct customer_id) as num_customers
from payment;

select max(datediff(return_date, rental_date)) from rental;

select avg(datediff(return_date,  rental_date)) from rental;

use sqlclass_db;
create table number_tbl(val smallint);

desc number_tbl;

insert into number_tbl values(1),(3),(5);

select * from number_tbl;

select count(*) as num_rows, 
count(val) as num_vals,
sum(val) as total,
max(val) as max_val,
avg(val) as avg_val
from number_tbl;

use sakila;

select actor_id, count(*) from film_actor
group by actor_id;

select fa.actor_id, f.rating, count(*) from film_actor as fa
inner join film as f on fa.film_id = f.film_id
group by fa.actor_id, f.rating
order by 1,2;

select fa.actor_id, f.rating, count(*)
from film_actor as fa
inner join film as f
on fa.film_id = f.film_id
group by fa.actor_id, f.rating with rollup 
order by 1,2;

select fa.actor_id, f.rating, count(*) 
from film_actor fa
inner join film f 
on fa.film_id = f.film_id
where f.rating in ('G','PG')
group by fa.actor_id, f.rating
having count(*) > 9
order by count(*);                                                                                                                            

select customer_id, count(*), sum(amount)
from payment
group by customer_id;