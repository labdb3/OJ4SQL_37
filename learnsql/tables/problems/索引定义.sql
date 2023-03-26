--d  为学生表student中的dno列添加外键参考department表中的dno
--t mysql
alter table student add constraint student_dept_fk foreign key(dno) references  department(dno);

--d  增加索引否则无法建立外键约束
--t mysql
alter table teacher add index teacher_dno_index(dno);
--t postgresql
create index teacher_dno_index on teacher (dno);

--d  为学生表student中的supervisor列添加外键参考teacher表中的tno
--t mysql
alter table student add constraint student_teacher_fk foreign key(supervisor) references  teacher(tno);

--d  为课程表course中的pcno列添加外键参考course表中的cno
--t mysql
alter table course add constraint course_course_fk foreign key(pcno) references  course(cno);

--d  为教师表teacher中的dno列添加外键参考department表中的dno
--t mysql
alter table teacher add constraint teacher_dept_fk foreign key(dno) references  department(dno);

--d  为部门表department中的dean列添加外键参考teacher表中的tno
--t mysql
alter table department add constraint dept_teacher_fk foreign key(dean) references  teacher(tno);