--d 替代主码相同的现有行---建表
create table test_replace( id int auto_increment primary key, name  char(10),cur_time  datetime);
insert into  test_replace(name,cur_time) values('A',now()),('B',now());

--d 替代主码相同的现有行---查询1
replace  test_replace values(1,'AA',now());

--d 替代主码相同的现有行---查询2
replace into  test_replace  values( 1,'AA', now() );

--d 替代主码相同的现有行---查询3
replace into  test_replace  values( 3, 'C', now() );

--d in的用法示例----建表
create table  delA (a int);
create table  delB (b int);
insert into  delA  values (1),(3),(4);
insert into  delB  values (3),(4),(5);

--d in的用法示例----查询1
select * from delA;

--d in的用法示例----查询2
delete from  delA  where  a = (select  b  from  delB  where b<4);

--d in的用法示例----查询3
delete from  delA  where  a = (select  b  from  delB  where b>4);

--d 删除操作-----建表
create table testDel (val int);
insert into testDel values (2),(4),(5),(7),(8);

--d 删除操作-----查询1
delete from testDel
where val > (select avg(val) from (select * from testDel) as E);

--d 删除操作-----查询2
with tmp as ( select avg(val) as A from testDel) 
delete  testDel 
from testDel inner join tmp where val > A;


--d 多表删除----建表
create table tA ( a int );
create table tB ( b int );
create table tC ( c int );
insert into tA values (1),(2),(3);
insert into tB values (2),(3),(4);
insert into tC values (3),(4),(5);

--d 多表删除----查询1
delete  tA  from  tA inner join  tB  where a=b;

--d 多表删除----查询2
delete  tA, tB  from  tA  inner join  tB  inner join  tC where  a=b  and  b=c;
