use sqlclass_db;

select * from nobel;

/*1*/ 
select year, category, fullname from nobel 
where (year=1960) and category in ('Peace', 'Physics');

/*2*/
select year, category, prize_amount, birth_continent, birth_country from nobel
where fullname='Albert Einstein';

/*3*/ 
select year, fullname, birth_country from nobel
where year between 1910 and 2010 
and category='Peace';

/*4*/
select category, fullname from nobel
where fullname like 'John%';

/*5*/
select * from nobel 
where (year=1964) and category not in ('Chemistry','Physiology or Medicine')
order by fullname;

/*6*/
select year, fullname, gender, birth_country from nobel
where year between 2000 and 2019
and category='Literature'

/*7*/
select category, count(*) as count from nobel
group by category
order by count desc;


/*8*/
select distinct year from nobel
where category='Physiology or Medicine';

/*9*/ 
select count(distinct n1.year) as count from nobel as n1
where n1.year not in (select distinct year from nobel as n2 where category='Physiology or Medicine');

/*10*/ 
select fullname from nobel
where gender='female';

/*11*/
select birth_country, count(*) from nobel
group by birth_country;

/*12*/
select * from nobel
where birth_country='Korea';

/*13*/
select * from nobel
where birth_continent not in ('Europe', 'North America', '');

/*14*/
select birth_country,count(*) as count from nobel
group by birth_country 
having count(*) >=10
order by count desc;

/*15*/
select fullname, count(*) as count from nobel
group by fullname
having count >= 2 and fullname != ''
order by fullname;


select distinct year from nobel;




