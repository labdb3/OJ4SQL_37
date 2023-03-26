select emp_no
from titles t
where exists(
select emp_no
from dept_emp
where emp_no=t.emp_no
group by emp_no
having count(distinct dept_no)>=2)
group by emp_no
having count(*)>=3
order by emp_no ASC
limit 10;
