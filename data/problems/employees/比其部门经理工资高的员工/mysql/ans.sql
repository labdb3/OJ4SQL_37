select distinct e.emp_no, m.emp_no
from dept_emp e inner join salaries se using (emp_no), dept_manager m inner join salaries sm using(emp_no)
where e.dept_no=m.dept_no -- 同一个部门
and se.salary>sm.salary -- 员工薪水大于经理薪水
and greatest(e.from_date, m.from_date) < least(e.to_date, m.to_date) -- 任职交集
and greatest(se.from_date,sm.from_date)<least(se.to_date,sm.to_date) -- 薪水交集
and greatest(greatest(e.from_date,m.from_date),greatest(se.from_date,sm.from_date))<
least(least(e.to_date,m.to_date),least(se.to_date,sm.to_date))
order by e.emp_no ASC
limit 10;
