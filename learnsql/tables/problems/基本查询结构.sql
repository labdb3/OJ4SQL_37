--d 查询学生表中的所有信息。
--t mysql
select * from student;
--t postgresql 
select * from student;
--t opengauss
select * from student;

--d 将多列信息进行连接，结果表述为自然语言描述。
--t mysql
select group_concat(tname, "老师的工资是", salary ," , 职称是", title )
from teacher;
--t postgresql
select tname || '老师的工资是' || salary::text || ' ,职称是' || title
from teacher;
--t opengauss
select tname || '老师的工资是' || salary::text || ' ,职称是' || title
from teacher;

--d 查询选取课程的学生姓名、课程名称及成绩。
--t mysql
select	sname, cname, grade
from   	student , course,sc
where  	student.sno = sc.sno
	and course.cno = sc.cno;
--t postgresql
select	sname, cname, grade
from   	student , course,sc
where  	student.sno = sc.sno
	and course.cno = sc.cno;
--t opengauss
select	sname, cname, grade
from   	student , course,sc
where  	student.sno = sc.sno
	and course.cno = sc.cno;

--d 查询薪资在5000-9000的老师姓名。
--t mysql
select  tname
from  teacher
where salary  between  5000 and 9000;
--t postgresql
select  tname
from  teacher
where salary  between  5000 and 9000;
--t opengauss
select  tname
from  teacher
where salary  between  5000 and 9000;

--d 查询所有选课的学生（对选多门课程的学生不重复出现）。
--t mysql
select  distinct  sno  from  sc;
--t postgresql
select  distinct  sno  from  sc;
--t opengauss
select  distinct  sno  from  sc;

--d 查询学生表中的所有信息，按照年龄升序，姓名降序的方式排列。
select  *
from student
order by age asc, sname  desc;

--d 查询学生的姓名、性别及出生日期，按照出生日期升序排列。
select	sname 姓名, sex  性别, 2019 - age  出生日期
from student
order by 2019 - age;

--d 查询选修课程C1成绩比s01高的学生的学号。
select 		s2.sno
from      sc  as  s1,sc  as  s2
where     	s1.sno = 's01'
and     	s1.cno = 'c01'
and     	s2. cno = 'c01'
and      	s1.grade < s2.grade ;

--d 查询工资比所在系主任高的老师的姓名及薪资。
select   	t1.tname,t1.salary
from      	teacher  t1,teacher  t2,department
where    	t1.dno = department.dno
	and   	department.dean = t2.tno
	and  	t1.salary >t2.salary;
