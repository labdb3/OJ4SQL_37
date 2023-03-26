--d 查询成绩最高的学生编号。
select sno
from sc
where grade = (select max(grade)from sc);

--d 查询sc表中grade列不为空值的行数。
select count(grade)
from sc;

--d 查询sc表中的行数。
select count(*)
from sc;

--d 查询sc表中grade列的总体标准差和样本方差。
select stddev_pop(grade), stddev_samp(grade)
from sc;

--d 聚集函数----创建表
create  table  aggR(a int);
insert into  aggR values  (1),(2),(2);
insert into aggR values(),();
insert into aggR values (5),(7);

--d 聚集函数----查询1
select * from aggR;

--d 聚集函数----查询2
select count(a),count(*) from aggR;

--d 聚集函数----查询3
select avg(a),sum(a)/count(a),sum(a)/count(*) from aggR;

--d 统计型聚集函数---创建表
create table  height( h int);
insert into height values (3),(3),(4),(5),(9),(100),(1000);

--d 统计型聚集函数----查询1
select std(h),stddev_pop(h),stddev_samp(h) from height;

--d 统计型聚集函数----查询2
select var_pop(h),var_samp(h) from height;
