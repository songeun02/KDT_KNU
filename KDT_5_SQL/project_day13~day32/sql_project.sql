use fuel;

ALTER TABLE csi_file ADD PRIMARY KEY (년도);

desc csi_file;

set foreign_key_checks=0;    

alter table csi_file add foreign key(년도) references fuel_file(년도);

set foreign_key_checks=1;    

set foreign_key_checks=0; 
alter table cpi_file add foreign key(년도) references fuel_file(년도);
set foreign_key_checks=1;

desc csi_file;

select * from csi_file

select csi.년도, csi.여행비지출전망CSI , ppi.제트유 from csi_file as csi
inner join ppi_file as ppi 
on csi.년도=ppi.년도;

create table travel as 
select csi.년도, csi.여행비지출전망CSI , ppi.제트유 from csi_file as csi
inner join ppi_file as ppi 
on csi.년도=ppi.년도

select * from travel;
desc travel;

alter table travel add foreign key(년도) references fuel_file(년도);
ALTER TABLE travel ADD PRIMARY KEY (년도);

select * from csi_file;

select 생활형편전망CSI from csi_file;

select bsi.전체산업, csi.소비자심리지수, ppi.생산자물가지수, cpi.총지수 
from bsi_file as bsi inner join csi_file as csi inner join ppi_file as ppi inner join cpi_file as cpi
on bsi.년도 = csi.년도 and csi.년도 = ppi.년도 and ppi.년도 = cpi.년도

drop table total;

create table total as 
select bsi.년도, ppi.생산자물가지수, cpi.총지수 , csi.소비자심리지수, bsi.전체산업
from bsi_file as bsi inner join csi_file as csi inner join ppi_file as ppi inner join cpi_file as cpi
on bsi.년도 = csi.년도 and csi.년도 = ppi.년도 and ppi.년도 = cpi.년도

select * from total;

select * from fuel_file;

