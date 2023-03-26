--d 查询学生姓名为张晓桐，朱英杰的全部信息
select *
from student
where sname in ("张晓桐", "朱英杰");

--d 查询选修课程编号为c01的学生姓名。
select sname
from student
where
  sno in ( select sno
    from sc
    where cno = "c01"
  );

--d 查询选修了课程编号为c01及c02的学生学号。
select sno
from sc
where
  sc.cno = "c01"
  and sc.sno in (
    select sno
    from sc
    where cno = "c02"
  );

--d 查询平均成绩最高的学生的学号。
select sno
from sc
group by sno
having
  avg(grade) >= all (
    select avg(grade)
    from sc
    group by sno
  );

--d 查询选择了课程编号c01的学生姓名。
select sname
from student
where exists (
    select *
    from sc
    where cno = "c01" and sno = student.sno
  );

--d 查询选择了课程编号为c01的学生，看其是否选择了课程c02。
select sno
from sc sc1
where sc1.cno = "c01"
  and exists (
    select sno
    from sc
    where cno = "c02" and sno = sc1.sno
  );

--d some/all子查询----建表
create table Comp1 (value1 int);
create table Comp2 (value2 int);
insert into Comp1 values (1),(3),(7),(9);
insert into Comp2 values (2),(4),(7),(8);
insert into Comp2 values (8);

--d some/all子查询----查询1
select value1 from Comp1 where value1 > some (select value2  from Comp2);

--d some/all子查询----查询2
select value1 from Comp1 where value1 > all (select value2  from Comp2);  

--d some/all子查询----查询3
select value1 from Comp1 where value1 = some (select value2  from Comp2); 

--d some/all子查询----查询4
select value1 from Comp1 where value1 <> some (select value2  from Comp2);  

--d some/all子查询----查询5
select value1 from Comp1 where value1 <> all (select value2  from Comp2); 

--d some/all子查询----查询6
select value1 from Comp1 where value1 in (select value2  from Comp2);  

--d some/all子查询----查询7
select value1 from Comp1 where value1 not in (select value2  from Comp2); 

--d 子查询中的属性解析匹配---建表
create table MyS (sno char(4));
create table FooSC (sno char(4), cn char(4));
insert into MyS values ('s1'),('s2');
insert into FooSC values ('s1','c1'),('s2','c2');

--d 子查询中的属性解析匹配---查询
select  sno from  MyS where  sno  in ( select sno from FooSC where cn = 'c1');

--d 子查询和空值的关系---建表
create table T_1(A int);
create table T_2(B int);
create table T_3(C int);
insert into T_1 values (1),(2);
insert into T_2 values (null);

--d 子查询和空值的关系---查询1
select 	* from	T_1 where 	A   not in ( select  *  from  T_2 );

--d 子查询和空值的关系---查询2
select 	* from	T_1 where  not exists 	( select  *  from  T_2  where A=B);

--d 子查询和空值的关系---查询3
select 	* from		T_1 where 	A  not in ( select  *  from  T_3 );

--d 子查询和空值的关系---查询4
select 	* from		T_1 where 	 not exists	( select  *  from  T_3  where  A=C);
