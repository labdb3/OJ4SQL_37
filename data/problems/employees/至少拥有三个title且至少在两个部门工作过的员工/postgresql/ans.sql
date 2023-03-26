select emp_no eo
from titles
group by emp_no
having count(*)>=3 and
(select count(DISTINCT dept_no) from dept_emp where dept_emp.emp_no=eo)>=2
order by eo ASC
limit 10;
