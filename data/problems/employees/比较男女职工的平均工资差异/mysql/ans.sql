select msalary.avg_salary, fsalary.avg_salary, msalary.avg_salary-fsalary.avg_salary
from
(
select sum(salary/360*datediff(if(to_date='9999-01-01','2003-08-01',to_date),from_date))/sum(datediff(if(to_date='9999-01-01','2003-08-01',to_date),from_date)) as avg_salary
from employees natural join salaries
where gender='M'
) msalary,
(
select sum(salary/360*datediff(if(to_date='9999-01-01','2003-08-01',to_date),from_date))/sum(datediff(if(to_date='9999-01-01','2003-08-01',to_date),from_date)) as avg_salary
from employees natural join salaries
where gender='F'
) fsalary
