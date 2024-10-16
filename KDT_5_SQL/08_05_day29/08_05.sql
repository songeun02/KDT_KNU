use sakila;
select * from language;

select name, last_update from language;

select name from language;

select language_id, 'common' as language_usage, 
	language_id * 3.14 as lang_pi_value,
	upper(name) as language_name
	from language;
	

select actor_id from film_actor order by actor_id;

select distinct actor_id from film_actor order by actor_id;

select concat(cust.last_name, ', ',cust.first_name) as full_name from
(select first_name, last_name, email from customer
where first_name='JESSIE') as cust;

create temporary table actor_j
(actor_id smallint(5),
first_name varchar(45),
last_name varchar(45));
desc actor_j

insert into actor_j
select actor_id, first_name, last_name from actor where last_name like 'J%';

select * from actor_j;

create view cust_vw as 
select customer_id, first_name, last_name, active from customer;

select * from cust_vw

select customer.first_name, customer.last_name, time(rental.rental_date) as rental_time
from customer inner join rental 
on customer.customer_id=rental.customer_id
where date(rental.rental_date)='2005-06-14';

select c.first_name, c.last_name, time(r.rental_date) rental_date 
from customer c inner join rental r
on c.customer_id=r.customer_id
where date(r.rental_date)='2005-06-14';


select title from film 
where rating='G' and rental_duration>=7;

select title, rating, rental_duration
from film
where (rating='G' and rental_duration >=7) or 
(rating='PG-13' and rental_duration<4);

select * from rental ;
select * from customer where customer_id='229';


select c.first_name, c.last_name, count(*) as rental_count
from customer as c inner join rental as r
on c.customer_id = r.customer_id
group by c.first_name, c.last_name
having count(*) >= 40
order by count(*);


select c.first_name, c.last_name, time(r.rental_date) as rental_time
from customer as c inner join rental as r
on c.customer_id = r.customer_id
where date(r.rental_date) = '2005-06-14'
order by c.last_name, c.first_name asc;

select c.first_name, c.last_name, time(r.rental_date) as rental_time
from customer as c inner join rental as r
on c.customer_id = r.customer_id
where date(r.rental_date) = '2005-06-14'
order by c.last_name desc, c.first_name;

select * from customer c inner join rental r
on c.customer_id = r.customer_id

select c.first_name, c.last_name, time(r.rental_date) as rental_time
from customer as c inner join rental as r 
on c.customer_id = r.customer_id
where date(r.rental_date) = '2005-06-14'
order by time(r.rental_date) desc;

select c.first_name, c.last_name, time(r.rental_date) as rental_time
from customer as c inner join rental as r 
on c.customer_id = r.customer_id
where date(r.rental_date) = '2005-06-14'
order by 1 desc;

select actor_id, first_name, last_name from actor
order by last_name, first_name;

select actor_id, first_name, last_name from actor 
where last_name='WILLIAMS' or last_name='DAVIS';

select * from rental;

select distinct customer_id from rental
where date(rental_date)='2005-07-05';

select c.store_id, c.emailp, r.rental_date, r.return_date 
from customer c inner join renta                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                l r 
on c.customer_id = r.customer_id
where date(r.rental_date) = '2005-06-14'
order by return_date desc;

select c.email, r.rental_date 
from customer as c inner join rental as r 
on c.customer_id = r.customer_id
where date(r.rental_date)='2005-06-14';

select c.email, r.rental_date
from customer as c inner join rental as r
on c.customer_id = r.customer_id
where date(r.rental_date) <> '2005-06-14'

select customer_id, rental_date from rental 
where rental_date < '2005-05-25';

select customer_id, rental_date from rental 
where rental_date <='2005-06-15' and rental_date>='2005-06-14';

select customer_id, rental_date from rental 
where date(rental_date) <= '2005-06-16' and date(rental_date) >= '2005-06-14';

select customer_id, rental_date from rental
where date(rental_date) between '2005-06-14' and '2005-06-16';

select customer_id, payment_date, amount from payment 
where amount between 10.0 and 11.99;

select last_name, first_name from customer
where last_name between 'FA' and 'FRB'

select title, rating from film
where rating='G' or rating='PG'

select title, rating from film
where rating in ('G','PG');

select title, rating from film where title like '%PET%';

select title, rating from film
where rating in (select rating from film where title like '%PET%')

select title, rating from film
where rating not in ('PG-13','R','NC-17');

select last_name, first_name from customer
where last_name like '_A_T%S'

select last_name, first_name from customer
where last_name like 'Q%' or last_name like 'Y%';

select last_name, first_name 
from customer 
where last_name regexp '^[QY]';

select rental_id, customer_id, return_date from rental 
where return_date is null;

select rental_id, customer_id, return_date from rental
where return_date is not null

select rental_id, customer_id, return_date from rental
where return_date is null 
or return_date not between '2005-05-01' and '2005-09-01';

select payment_id, customer_id, amount, date(payment_date) as payment_date
from payment where (payment_id between 101 and 120);

select payment_id, customer_id, amount, date(payment_date) payment_date from payment
where (payment_id between 101 and 120)
and customer_id != 5 and amount > 8 or date(payment_date) = '2005-08-23';

select amount from payment 
where amount in (1.98, 7.98, 9.98)

select * from rental where return_date='2005-09-01';

select c.first_name, c.last_name, a.address
from customer as c cross join address as a;

select count(*) from customer

select count(*) from customer as c cross join address

select * from address

select c.first_name, c.last_name, a.address, a.district 
from customer as c inner join address as a
on c.address_id = a.address_id

select count(*) 
from customer as c inner join address as a
on c.address_id = a.address_id

select c.first_name, c.last_name, ct.city, a.address, a.district, a.postal_code 
from customer as c
inner join address as a on c.address_id = a.address_id
inner join city as ct on a.city_id = ct.city_id;

select c.first_name, c.last_name, addr.address, addr.city, addr.district 
from customer as c inner join
(select a.address_id, a.address, ct.city, a.district 
from address as a
inner join city as ct
on a.city_id = ct.city_id
where a.district = 'California'
) as addr 
on c.address_id = addr.address_id;

select f.title 
from film as f
inner join film_actor as fa on f.film_id = fa.film_id
inner join actor as a on fa.actor_id = a.actor_id
where ((a.first_name = 'CATE' and a.last_name='MCQUEEN')
or (a.first_name = 'CUBA' and a.Last_name='BIRCH'));


select f.title, f.film_id, a1.first_name, a1.last_name
from film as f 
inner join film_actor as fa1
on f.film_id = fa1.film_id
inner join actor a1
on fa1.actor_id = a1.actor_id
where (a1.first_name='CATE' and a1.last_name='MCQUEEN');

select f.title, f.film_id, a2.first_name, a2.last_name
from film as f
inner join film_actor as fa2
on f.film_id = fa2.film_id
inner join actor a2
on fa2.actor_id = a2.actor_id
where (a2.first_name= 'CUBA' and a2.last_name='BIRCH')

select f.title 
from film as f
inner join film_actor as fa1
on f.film_id = fa1.film_id
inner join actor a1
on fa1.actor_id=a1.actor_id
inner join film_actor as fa2
on f.film_id = fa2.film_id
inner join actor a2
on fa2.actor_id=a2.actor_id
where (a1.first_name='CATE' and a1.last_name='MCQUEEN')
and (a2.first_name='CUBA' and a2.last_name='BIRCH');




use sqlclass_db;


create table customer 
(customer_id smallint unsigned,
first_name varchar(20), 
last_name varchar(20),
birth_date date,
spouse_id smallint unsigned,
constraint primary key (customer_id));

desc customer;

insert into customer (customer_id, first_name, last_name, birth_date, spouse_id)
values 
(1,	'John',	'Mayer','1983-05-12', 2),
(2,	'Mary',	'Mayer','1990-07-30', 1),
(3,	'Lisa',	'Ross',	'1989-04-15', 5),
(4,	'Anna',	'Timothy','1988-12-26', 6),
(5,	'Tim',	'Ross',	'1957-08-15', 3),
(6,	'Steve','Donell','1967-07-09', 4);

insert into customer (customer_id, first_name, last_name, birth_date)
values (7,'Donna','Trapp','1978-06-23');

select * from customer;

select cust.customer_id, cust.first_name, cust.last_name, cust.birth_date, cust.spouse_id, spouse.first_name as spouse_first_name, spouse.last_name as spouse_lastname
from customer as cust join customer as spouse
on cust.spouse_id=spouse.customer_id;

