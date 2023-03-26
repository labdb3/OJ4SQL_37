select t1.dept_no, max_emp_no, max_salary, min_emp_no, min_salary
from(
select dept_no, emp_no as max_emp_no, salary as max_salary
from dept_emp join salaries using (emp_no)
where greatest(dept_emp.from_date,salaries.from_date)<least(dept_emp.to_date, salaries.to_date) and
(dept_no,salary) in (select dept_no, max(salary) ms
        from dept_emp join salaries using (emp_no)
        where greatest(dept_emp.from_date,salaries.from_date)<least(dept_emp.to_date, salaries.to_date)
        group by dept_emp.dept_no
))t1,
(select dept_no, emp_no as min_emp_no, salary as min_salary
from dept_emp join salaries using (emp_no)
where greatest(dept_emp.from_date,salaries.from_date)<least(dept_emp.to_date, salaries.to_date) and
(dept_no,salary) in (select dept_no, min(salary) ms
        from dept_emp join salaries using (emp_no)
        where greatest(dept_emp.from_date,salaries.from_date)<least(dept_emp.to_date, salaries.to_date)
        group by dept_emp.dept_no
))t2
where t1.dept_no=t2.dept_no
