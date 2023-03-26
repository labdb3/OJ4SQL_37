--d 创建学生表
--t mysql
create table   student
(	sno    	char(8),					
	sname    char(8)  not null default  '佚名',
	age	   	tinyint,
	sex	   	char(1),
	dno		char(8),
	supervisor	char(8),  
	primary key (sno),
	check (sex = 'M'  or  sex='F')
);
--t postgresql
CREATE TABLE student
(	sno    	char(8),					
	sname   varchar(16)  not null default  '佚名',
	age	   	smallint,
	sex	   	char(1),
	dno		char(8),
	supervisor	char(8),  
	primary key (sno),
	check (sex = 'M'  or  sex='F')
);
--t opengauss
CREATE TABLE   student
(	sno    	char(8),					
	sname       char(8)  not null default  '佚名',
	age	   	smallint,
	sex	   	char(1),
	dno		char(8),
	supervisor	char(8),  
	primary key (sno),
	check (sex = 'M'  or  sex='F')
);

--d 往学生表插入数据
--t mysql
SET FOREIGN_KEY_CHECKS = 0;
insert into student(sno,sname,age,sex,dno,supervisor) values('s01','张晓桐',18,'M','d01','t01');
insert into student(sno,sname,age,sex,dno,supervisor) values('s02','李晓峰',18,'M','d01','t01');
insert into student(sno,sname,age,sex,dno,supervisor) values('s03','刘莉',18,'F','d01','t01');
insert into student(sno,sname,age,sex,dno,supervisor) values('s04','朱英杰',19,'M','d01','t02');
insert into student(sno,sname,age,sex,dno,supervisor) values('s05','张子豪',18,'M','d01','t02');
insert into student(sno,sname,age,sex,dno,supervisor) values('s06','胡可琪',17,'F','d02','t03');
insert into student(sno,sname,age,sex,dno,supervisor) values('s07','李佳音',18,'F','d02','t03');
insert into student(sno,sname,age,sex,dno,supervisor) values('s08','陈凯琦',18,'M','d02','t04');
insert into student(sno,sname,age,sex,dno,supervisor) values('s09','刘英涛',19,'M','d02','t04');
insert into student(sno,sname,age,sex,dno,supervisor) values('s10','肖英俊',17,'M','d03','t05');
insert into student(sno,sname,age,sex,dno,supervisor) values('s11','桑家琦',18,'F','d03','t05');
insert into student(sno,sname,age,sex,dno,supervisor) values('s12','鲍泽峰',18,'M','d04','t06');
SET FOREIGN_KEY_CHECKS = 1;
--t postgresql
insert into student(sno,sname,age,sex,dno,supervisor) values('s01','张晓桐',18,'M','d01','t01');
insert into student(sno,sname,age,sex,dno,supervisor) values('s02','李晓峰',18,'M','d01','t01');
insert into student(sno,sname,age,sex,dno,supervisor) values('s03','刘莉',18,'F','d01','t01');
insert into student(sno,sname,age,sex,dno,supervisor) values('s04','朱英杰',19,'M','d01','t02');
insert into student(sno,sname,age,sex,dno,supervisor) values('s05','张子豪',18,'M','d01','t02');
insert into student(sno,sname,age,sex,dno,supervisor) values('s06','胡可琪',17,'F','d02','t03');
insert into student(sno,sname,age,sex,dno,supervisor) values('s07','李佳音',18,'F','d02','t03');
insert into student(sno,sname,age,sex,dno,supervisor) values('s08','陈凯琦',18,'M','d02','t04');
insert into student(sno,sname,age,sex,dno,supervisor) values('s09','刘英涛',19,'M','d02','t04');
insert into student(sno,sname,age,sex,dno,supervisor) values('s10','肖英俊',17,'M','d03','t05');
insert into student(sno,sname,age,sex,dno,supervisor) values('s11','桑家琦',18,'F','d03','t05');
insert into student(sno,sname,age,sex,dno,supervisor) values('s12','鲍泽峰',18,'M','d04','t06');

--d 创建课程表
--t mysql
create table   course
(	cno    	char(8)  primary key,    
	cname	      char(8)  not null  unique,
	pcno	      char(8),
	credit	tinyint
);
--t postgresql
create table   course
(	cno    	char(8)  primary key,    
	cname	      char(8)  not null  unique,
	pcno	      char(8),
	credit	smallint
);
--t opengauss
create table   course
(	cno    	char(8)  primary key,    
	cname	      varchar(16)  not null  unique,
	pcno	      char(8),
	credit	smallint
);

--d 往课程表插入数据
--t mysql
SET FOREIGN_KEY_CHECKS = 0;
insert into course(cno,cname,pcno,credit) values('c01','数据库原理','c05',2);
insert into course(cno,cname,pcno,credit) values('c02','操作系统','c05',3);
insert into course(cno,cname,pcno,credit) values('c03','计算机网络','c05',3);
insert into course(cno,cname,pcno,credit) values('c04','数据结构','c04',3);
insert into course(cno,cname,pcno,credit) values('c05','编译原理','c04',2);
insert into course(cno,cname,pcno,credit) values('c06','算法分析','c04',3);
insert into course(cno,cname,pcno,credit) values('c07','离散数学','c04',2);
SET FOREIGN_KEY_CHECKS = 1;
--t postgresql
insert into course(cno,cname,pcno,credit) values('c01','数据库原理','c05',2);
insert into course(cno,cname,pcno,credit) values('c02','操作系统','c05',3);
insert into course(cno,cname,pcno,credit) values('c03','计算机网络','c05',3);
insert into course(cno,cname,pcno,credit) values('c04','数据结构','c04',3);
insert into course(cno,cname,pcno,credit) values('c05','编译原理','c04',2);
insert into course(cno,cname,pcno,credit) values('c06','算法分析','c04',3);
insert into course(cno,cname,pcno,credit) values('c07','离散数学','c04',2);

--d 创建教师表
--t mysql
create table   teacher
(	tno    	char(8) primary key,					
	tname	char(8)  	not null  default  '佚名',
	dno		char(8),
	salary	int,
title		char(8)	check (title in('讲师', '副教授', '教授'))
);
--t postgresql
create table   teacher
(	tno    	char(8) primary key,					
	tname	char(8)  	not null  default  '佚名',
	dno		char(8),
	salary	int,
title		char(8)	check (title in('讲师', '副教授', '教授'))
);
--t opengauss
create table   teacher
(	tno    	char(8) primary key,					
	tname	varchar(16)  	not null  default  '佚名',
	dno		char(8),
	salary	int,
title		varchar(16)	check (title in('讲师', '副教授', '教授'))
);

--d 往教师表导入数据
--t mysql
SET FOREIGN_KEY_CHECKS = 0;
insert into teacher(tno,tname,dno,salary,title) values('t01','柏叶平','d01',10000,'副教授');
insert into teacher(tno,tname,dno,salary,title) values('t02','崔锡勇','d01',8000,'讲师');
insert into teacher(tno,tname,dno,salary,title) values('t03','邓辉','d02',12000,'教授');
insert into teacher(tno,tname,dno,salary,title) values('t04','郝小可','d02',10000,'副教授');
insert into teacher(tno,tname,dno,salary,title) values('t05','朱承斐','d03',8000,'讲师');
insert into teacher(tno,tname,dno,salary,title) values('t06','邓娜敏','d04',12000,'教授');
SET FOREIGN_KEY_CHECKS = 1;
--t postgresql
insert into teacher(tno,tname,dno,salary,title) values('t01','柏叶平','d01',10000,'副教授');
insert into teacher(tno,tname,dno,salary,title) values('t02','崔锡勇','d01',8000,'讲师');
insert into teacher(tno,tname,dno,salary,title) values('t03','邓辉','d02',12000,'教授');
insert into teacher(tno,tname,dno,salary,title) values('t04','郝小可','d02',10000,'副教授');
insert into teacher(tno,tname,dno,salary,title) values('t05','朱承斐','d03',8000,'讲师');
insert into teacher(tno,tname,dno,salary,title) values('t06','邓娜敏','d04',12000,'教授');

--d 创建系表
--t mysql
create table   department
(	dno    	char(8) primary key,					
	dname	char(8)  	not null  default  '佚名',
	dean	char(8)
);
--t postgresql
create table   department
(	dno    	char(8) primary key,					
	dname	char(8)  	not null  default  '佚名',
	dean	char(8)
);

--d 往系表导入数据
--t mysql
SET FOREIGN_KEY_CHECKS = 0;
insert into department(dno,dname,dean) values('d01','网络所','t01');
insert into department(dno,dname,dean) values('d02','语言所','t03');
insert into department(dno,dname,dean) values('d03','软件所','t05');
insert into department(dno,dname,dean) values('d04','结构所','t06');
SET FOREIGN_KEY_CHECKS = 1;
--t postgresql
insert into department(dno,dname,dean) values('d01','网络所','t01');
insert into department(dno,dname,dean) values('d02','语言所','t03');
insert into department(dno,dname,dean) values('d03','软件所','t05');
insert into department(dno,dname,dean) values('d04','结构所','t06');

--d 创建选课表
--t mysql
create table   sc
(	sno    	char(8),
	constraint sc_student_fk foreign key(sno) references  student(sno),
	cno   	char(8),
	Constraint sc_course_fk foreign key(cno) references course(cno),
	grade 	tinyint,
	primary key (sno, cno),
	check((grade  is null) 	or  grade between 0 and 100)
);
--t postgresql
create table   sc
(	sno    	char(8),
	--  constraint sc_student_fk foreign key(sno) references  student(sno),
	cno   	char(8),
	--  Constraint sc_course_fk foreign key(cno) references course(cno),
	grade 	smallint,
	primary key (sno, cno),
	check((grade  is null) 	or  grade between 0 and 100)
);

--d 往选课表导入数据
--t mysql
SET FOREIGN_KEY_CHECKS = 0;
insert into sc(sno,cno,grade) values('s01','c01',85);
insert into sc(sno,cno,grade) values('s02','c01',88);
insert into sc(sno,cno,grade) values('s03','c01',92);
insert into sc(sno,cno,grade) values('s04','c02',87);
insert into sc(sno,cno,grade) values('s05','c02',79);
insert into sc(sno,cno,grade) values('s06','c03',90);
insert into sc(sno,cno,grade) values('s07','c03',82);
insert into sc(sno,cno,grade) values('s08','c04',83);
insert into sc(sno,cno,grade) values('s09','c04',88);
insert into sc(sno,cno,grade) values('s10','c05',75);
insert into sc(sno,cno,grade) values('s11','c05',86);
insert into sc(sno,cno,grade) values('s12','c05',81);
insert into sc(sno,cno,grade) values('s01','c05',67);
insert into sc(sno,cno,grade) values('s01','c02',56);
insert into sc(sno,cno,grade) values('s04','c04',82);
insert into sc(sno,cno,grade) values('s02','c03',65);
insert into sc(sno,cno) values('s03','c03');
insert into sc(sno,cno) values('s06','c05');
SET FOREIGN_KEY_CHECKS = 1;
--t postgresql
insert into sc(sno,cno,grade) values('s01','c01',85);
insert into sc(sno,cno,grade) values('s02','c01',88);
insert into sc(sno,cno,grade) values('s03','c01',92);
insert into sc(sno,cno,grade) values('s04','c02',87);
insert into sc(sno,cno,grade) values('s05','c02',79);
insert into sc(sno,cno,grade) values('s06','c03',90);
insert into sc(sno,cno,grade) values('s07','c03',82);
insert into sc(sno,cno,grade) values('s08','c04',83);
insert into sc(sno,cno,grade) values('s09','c04',88);
insert into sc(sno,cno,grade) values('s10','c05',75);
insert into sc(sno,cno,grade) values('s11','c05',86);
insert into sc(sno,cno,grade) values('s12','c05',81);
insert into sc(sno,cno,grade) values('s01','c05',67);
insert into sc(sno,cno,grade) values('s01','c02',56);
insert into sc(sno,cno,grade) values('s04','c04',82);
insert into sc(sno,cno,grade) values('s02','c03',65);
insert into sc(sno,cno) values('s03','c03');
insert into sc(sno,cno) values('s06','c05');

--d 创建授课表
--t mysql
create table   tc
(	tno    	char(8),
	constraint tc_teacher_fk foreign key (tno) references  teacher(tno),
	cno   	char(8),
	constraint tc_course_fk foreign key(cno) references course(cno)	
);

--d 往授课表导入数据
--t mysql
SET FOREIGN_KEY_CHECKS = 0;
insert into tc(tno,cno) values('t01','c01');
insert into tc(tno,cno) values('t02','c02');
insert into tc(tno,cno) values('t03','c03');
insert into tc(tno,cno) values('t04','c04');
insert into tc(tno,cno) values('t05','c05');
insert into tc(tno,cno) values('t01','c06');
insert into tc(tno,cno) values('t04','c07');
SET FOREIGN_KEY_CHECKS = 1;
--t postgresql
insert into tc(tno,cno) values('t01','c01');
insert into tc(tno,cno) values('t02','c02');
insert into tc(tno,cno) values('t03','c03');
insert into tc(tno,cno) values('t04','c04');
insert into tc(tno,cno) values('t05','c05');
insert into tc(tno,cno) values('t01','c06');
insert into tc(tno,cno) values('t04','c07');
