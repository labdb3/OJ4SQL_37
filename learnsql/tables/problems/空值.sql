--d 空值的逻辑计算-----创建表
create table test_null(a int);
insert into test_null values (1),(2),(3);

--d 空值的逻辑计算----1
select count(*) from test_null;

--d 空值的逻辑计算----2
select   count(*)   from   test_null where  1<1 or  null;

--d 空值的逻辑计算----3
select   count(*)   from   test_null where  1=1 or  1=null;

--d 空值的逻辑计算----4
select   count(*)   from   test_null where  1=1 and  1=null;

--d 空值的逻辑计算----5
select   count(*)   from   test_null where  1=1 and  not null;

--d 空值的逻辑计算----6
select   count(*)   from   test_null where  null<>null or null=null;

--d 空值的逻辑计算----7
select   count(*)   from   test_null where  not(1<1) or not null;

--d 列出满足如下条件的(sno, pno)对：或者供应商和零件的所在城市不同，或者零件所在城市不是Paris------创建表
create table supplier(sno varchar(10), city varchar(10)); 
create table product(pno varchar(10), city varchar(10));
insert into supplier values ('s1','London');
insert into product values('p2','Paris');
insert into product (pno) values('p1');

--d 列出满足如下条件的(sno, pno)对：或者供应商和零件的所在城市不同，或者零件所在城市不是Paris------查询
select	S.sno, P.pno 
from	supplier S , product P 
where 	S.city <> P.city or	P.city <> 'Paris';

--d distinct,group by对null值的处理-----创建表
create table   distinct_null(col  int,  val  int);
insert into   distinct_null  values   (1, null),(1, null),(null, 2),(null, 3),(null, null);
insert into distinct_null(col) values (1);
insert into distinct_null(col) values (1);
insert into distinct_null(val) values (2);
insert into distinct_null(val) values (3);
insert into distinct_null values();

--d distinct对null值的处理-----查询1
select distinct * from distinct_null;

--d group by对null值的处理-----查询2
select 	col, sum(val) from 	distinct_null group by 	col;

--d 空值处理函数的应用----创建表
create table NULL_TB( col char(10))
insert into NULL_TB values();
insert into NULL_TB values('');
insert into NULL_TB values('null');

--d 空值处理函数的应用----isnull
select isnull(1/0),isnull(0/1);

--d 空值处理函数的应用----nullif
select 	nullif (1, 2), nullif (1, 1);

--d 空值处理函数的应用----ifnull
select 	ifnull (1/0, 2), ifnull (0/1, 2);

--d 空值处理函数的应用----coalesce
select 	coalesce(null,not null,null is null,1<1);

--d 空值的排序处理----创建表
create table order_null(id int primary key auto_increment, val int);
insert into order_null(val) values(4);
insert into order_null values();
insert into order_null(val) values(2);
insert into order_null(val) values(5);
insert into order_null values();
insert into order_null(val) values(6);
insert into order_null values();

--d 空值的排序处理----查询1
select val from order_null order by val asc;