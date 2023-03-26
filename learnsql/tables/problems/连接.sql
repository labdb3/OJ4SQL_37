--d 查询所有老师的教工号、姓名、工资、所教课程号
select teacher.tno,tname,salary,cno
from teacher left join tc on teacher.tno = tc.tno;

--d 按照课程编号内连接表tc与sc。
select *
from sc inner join tc on sc.cno=tc.cno;

--d 按照课程编号左连接表tc与sc。
select *
from sc
left join tc on sc.cno=tc.cno;

--d 按照课程编号右连接表tc与sc。
select *
from sc right join tc on sc.cno=tc.cno;

--d 查询Left join excluding inner join部分的内容。
select tc.*
from tc left join sc on tc.cno =sc.cno
where tc.cno is null;

--d 查询full join excluding inner部分的内容。
(select	*
from tc left join sc on tc.cno = sc.cno
where sc.cno is null
)
union 
(select *
from tc right join sc on tc.cno = sc.cno
where tc.cno is null);

--d 建表
create table tbA(a int,b int);
create table tbC(b int,c int);
insert into tbA values(1,2),(3,2),(5,4);
insert into tbC values(2,4),(3,5);

--d 查询1
select   	* from 	tbA  inner join  tbC  on  tbA.b = tbC.b;

--d 查询2
select   	* from 	tbA  inner join  tbC  on  tbA.b <> tbC.b;

--d 查询3
select   	* from 	tbA  left join  tbC  on  tbA.b = tbC.b;

--d 查询4
select   	* from 	tbA  right join  tbC  on  tbA.b = tbC.b;

--d 查询5
select   	tbA.* from 	tbA  left join  tbC  on  tbA.b = tbC.b where	tbC.b  is null;

--d 查询6
select   	* from 	tbA  cross join  tbC;

--d 查询7
select   	* from 	tbA  natural join  tbC;

--d 查询8
select   	* from 	tbA join tbC using(b);

--d 查询9
select  * from 	tbA A  join   (tbA B, tbA C)	on 	(A.b=B.b and  A.b=C.b);

--d 查询10
select   	* from 		tbA  left join  tbC  on  tbA.b = tbC.b where	tbC.b  is null
union
select   	* from 		tbA  right join  tbC  on  tbA.b = tbC.b where	tbA.b  is null;

--d 查询11
select   * from  tbA  straight_join  tbC;