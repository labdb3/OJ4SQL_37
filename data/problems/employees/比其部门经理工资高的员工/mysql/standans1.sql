select distinct e.emp_no, m.emp_no
from dept_emp e inner join salaries se using (emp_no), dept_manager m inner join salaries sm using(emp_no)
where e.dept_no=m.dept_no -- 同一个部门
and se.salary>sm.salary -- 员工薪水大于经理薪水
and greatest(e.from_date, m.from_date) < least(e.to_date, m.to_date) -- 任职交集
order by e.emp_no ASC
limit 10;
