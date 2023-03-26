select  dept_no, msalary, min(salaries.salary) nsalary
from(
        select dept_no, salary msalary
        from dept_emp natural join(
                select emp_no, salary
                from salaries
                where salary = (select max(salary) from salaries)
        ) maxsalary
)dept_ms natural join dept_emp, salaries
where dept_emp.emp_no=salaries.emp_no
group by dept_no,msalary
order by dept_no ASC
