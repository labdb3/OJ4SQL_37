with temp as(
select a.emp_no as emp_no,GROUP_CONCAT(b.from_date,"~",b.to_date,"\r\n",b.title) as date
from employees as a,titles as b
where a.emp_no=b.emp_no
and a.emp_no=11027
)
select temp.emp_no as emp_no,SUBSTRING_INDEX(date,",",1)as tenure1,substring_index(SUBSTRING_INDEX(date,",",2),",",-1)as tenure2,SUBSTRING_INDEX(date,",",-1)as tenure3
from temp

