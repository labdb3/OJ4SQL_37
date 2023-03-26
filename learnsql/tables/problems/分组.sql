--d 按照学号分组从表sc中查询学生的学号，最高成绩，最低成绩，及平均成绩。
select sno, max(grade), min(grade), avg(grade)
from sc
group by sno;

--d 按照学号分组从表sc中查询最低分高于80的学生学号及平均成绩。
select sno, avg(grade)
from sc
group by sno
having min(grade) >= 80;

--d 按照学号分组从表sc中查询最低分高于80的学生学号及平均成绩。
select sno, avg(grade)
from sc
where grade >= 80
group by sno;

--d 按照年龄进行分组，查询该年龄组性别为男性且数量大于4的学生年龄及数量。
select age, count(sno)
from student
where sex = "M"
group by age
having count(*) > 4;

--d 按照系名进行分组，查询各系的学生姓名，连接显示。
select dname, group_concat(sname)
from department, student
where student.dno = department.dno
group by dname;

--d 按照系名进行分组，查询各系的学生姓名，按照姓名升序连接显示。
select dname, group_concat(sname order by sname)
from department, student
where student.dno = department.dno
group by dname;

--d 按照系名进行分组，查询各系的学生姓名，通过分隔符"|"连接显示。
select dname, group_concat(sname separator "|")
from department, student
where student.dno = department.dno
group by dname;

--d 在group分组的基础上再进行数据统计。按照性别分组，查询不同性别学生的平均年龄。
select sex, avg(age)
from student
group by sex with rollup;

--d group by与null的关系----创建表1
create table group_null(A int, B int, C int);
insert into group_null(A,B) values (1,2);
insert into group_null(A,B,C) values(1,2,3),(1,2,4);
insert into group_null(A,C) values(1,5),(2,6),(2,7);

--d group by与null的关系----创建表2
create table sales(model char(10),year int,color char(10),sales int);
insert into sales values('Chevy',1990,'red',5);
insert into sales values('Chevy',1990,'white',87);
insert into sales values('Chevy',1990,'blue',62);
insert into sales values('Chevy',1991,'red',54);
insert into sales values('Chevy',1991,'white',95);
insert into sales values('Chevy',1991,'blue',49);
insert into sales values('Chevy',1992,'red',31);
insert into sales values('Chevy',1992,'white',54);
insert into sales values('Chevy',1992,'blue',71);
insert into sales values('Ford',1990,'red',64);
insert into sales values('Ford',1990,'white',62);
insert into sales values('Ford',1990,'blue',63);
insert into sales values('Ford',1991,'red',52);
insert into sales values('Ford',1991,'white',9);
insert into sales values('Ford',1991,'blue',55);
insert into sales values('Ford',1992,'red',27);
insert into sales values('Ford',1992,'white',62);
insert into sales values('Ford',1992,'blue',39);

--d group by与null的关系----查询1
select * from group_null;

--d group by与null的关系----查询2
select A,count(*),count(B),count(C) 
from group_null 
group by A;

--d group by与null的关系----查询3
select B, count(B),count(*) 
from group_null 
group by B;

--d group by与null的关系----查询4
select A,B, count(*) 
from group_null 
group by A,B;

--d group by与null的关系----查询5
select A,B, count(*) 
from group_null 
group by A,B 
with rollup;

--d group by与null的关系----查询6
select 	if(grouping(A)=1,'汇总','原始') grpA,A, if(grouping(B)=1,'汇总','原始') grpB,B, count(*) 
from 	group_null 
group by A, B 
with rollup;

--d group by与null的关系----查询7
select 	A,B, count(*) 
from 	group_null 
group by B,A 
with rollup 
having grouping(A)=1 or grouping(B)=1;

--d group by与null的关系----查询8
select 	grouping(A,B),A,B, count(*) 
from 	group_null 
group by A, B 
with rollup;	

--d group by与null的关系----查询9
select		sum(sales) TotleSold ,		
case 	when(grouping(model) =1)  then '汇总' else  nullif(model, '未知') end model,		
case 	when(grouping(year) =1 )  then '汇总' else nullif(year, '未知')	end year,		
case 	when(grouping(color) =1)  then '汇总'else nullif(color, '未知')	end color
from sales 
group by	model, year, color with rollup;

--d group by与null的关系----查询10
select 	grouping(A,B,C),A,B,C,count(*) 
from 	group_null 
group by A, B,C 
with rollup order by 1;	

--d group by与null的关系----生成多个分组语句的合并报表
select 	model, year, null as color, sum(sales)
from 	sales 
group by	model, year 
union all 
select 	model, null as year, color, sum(sales)
from 	sales 
group by	model, color 
union all 
select 	null as model, year, color, sum(sales)
from 	sales 
group by	year, color 
union all 
select 	null as model, null as year, null as color, sum(sales)
from sales;
