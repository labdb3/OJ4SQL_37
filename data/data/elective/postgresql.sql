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

create table   course
(	cno    	char(8)  primary key,    
	cname	      char(8)  not null  unique,
	pcno	      char(8),
	credit	smallint
);

create table   teacher
(	tno    	char(8) primary key,					
	tname	char(8)  	not null  default  '佚名',
	dno		char(8),
	salary	int,
title		char(8)	check (title in('讲师', '副教授', '教授'))
);

create table   department
(	dno    	char(8) primary key,					
	dname	char(8)  	not null  default  '佚名',
	dean	char(8)
);
			       
--  为学生表student中的dno列添加外键参考department表中的dno
--  alter table student add constraint student_dept_fk foreign key(dno) references  department(dno);

--  增加索引否则无法建立外键约束
-- alter table teacher add index teacher_dno_index(dno);
create index teacher_dno_index on teacher(dno);

--  为学生表student中的supervisor列添加外键参考teacher表中的tno
--  alter table student add constraint student_teacher_fk foreign key(supervisor) references  teacher(tno);
			       
--  为课程表course中的pcno列添加外键参考course表中的cno
--  alter table course add constraint course_course_fk foreign key(pcno) references  course(cno);
			       
--  为教师表teacher中的dno列添加外键参考department表中的dno
--  alter table teacher add constraint teacher_dept_fk foreign key(dno) references  department(dno);
			       
--  为部门表department中的dean列添加外键参考teacher表中的tno
--  alter table department add constraint dept_teacher_fk foreign key(dean) references  teacher(tno);

create table   sc
(	sno    	char(8),
	--  constraint sc_student_fk foreign key(sno) references  student(sno),
	cno   	char(8),
	--  Constraint sc_course_fk foreign key(cno) references course(cno),
	grade 	smallint,
	primary key (sno, cno),
	check((grade  is null) 	or  grade between 0 and 100)
);

create table   tc
(	tno    	char(8),
	--  constraint tc_teacher_fk foreign key (tno) references  teacher(tno),
	cno   	char(8)
	--  constraint tc_course_fk foreign key(cno) references course(cno)
);


--  金融场景化实验

--  创建银行客户表
CREATE TABLE  client
(
        c_id INT PRIMARY KEY,
        c_name VARCHAR(100) NOT NULL,
        c_mail CHAR(30) UNIQUE,
        c_id_card CHAR(20) UNIQUE NOT NULL,
        c_phone CHAR(20) UNIQUE NOT NULL,
        c_password CHAR(20) NOT NULL
);

--  创建银行卡信息表
CREATE TABLE  bank_card
(
        b_number CHAR(30) PRIMARY KEY,
        b_type CHAR(20),
        b_c_id INT NOT NULL
);

-- 创建理财产品信息表
CREATE TABLE  finances_product
(
        p_name VARCHAR(100) NOT NULL,
        p_id INT PRIMARY KEY,
        p_description VARCHAR(4000),
        p_amount INT,
        p_year INT
);

-- 创建保险信息表
CREATE TABLE  insurance
(
        i_name VARCHAR(100) NOT NULL,
        i_id INT PRIMARY KEY,
        i_amount INT,
        i_person CHAR(20),
        i_year INT,
        i_project VARCHAR(200)
);

-- 创建基金信息表

CREATE TABLE  fund
(
        f_name VARCHAR(100) NOT NULL,
        f_id INT PRIMARY KEY,
        f_type CHAR(20),
        f_amount INT,
        risk_level CHAR(20) NOT NULL,
        f_manager INT NOT NULL
);

-- 创建资产信息表
CREATE TABLE  property
(
        pro_id INT PRIMARY KEY,
	    pro_c_id INT NOT NULL,
        pro_pif_id INT NOT NULL,
        pro_type INT NOT NULL,
        pro_status CHAR(20),
        pro_quantity INT,
        pro_income INT,
        pro_purchase_time DATE
);

-- 对表添加外键约束，在银行信息表和资产信息表中，都存在每个银行卡必须有一个持卡者、每份资产必须都有一个资产拥有者这样的对应关系。因此针对这种对应关系，创建外键约束。

-- 给表bank_card添加外键约束
ALTER TABLE bank_card ADD CONSTRAINT fk_c_id FOREIGN KEY (b_c_id) REFERENCES client(c_id) ON DELETE CASCADE;

-- 给表property添加外键约束
ALTER TABLE property ADD CONSTRAINT fk_pro_c_id FOREIGN KEY (pro_c_id) REFERENCES client(c_id) ON DELETE CASCADE;

-- 在理财产品表、保险信息表和基金信息表中，都存在金额这个属性，在现实生活中，金额不会存在负数。因此针对表中金额的属性，增加大于0的约束条件。

-- 为finances_product表的p_amount列添加大于等于0的约束
ALTER table finances_product ADD CONSTRAINT c_p_mount CHECK (p_amount >=0);

-- 为fund表的f_amount列添加大于等于0的约束
ALTER table fund ADD CONSTRAINT c_f_mount CHECK (f_amount >=0);

-- 为insurance表的i_amount列添加大于等于0的约束
ALTER table insurance ADD CONSTRAINT c_i_mount CHECK (i_amount >=0);
