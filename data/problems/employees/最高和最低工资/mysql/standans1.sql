-- wrong
with es as(
 select dept_no, s.emp_no, salary 
    from dept_emp as de join salaries as s on de.emp_no=s.emp_no
  and de.from_date <= s.to_date and s.from_date <= de.to_date
)
select mm.dept_no,
 (select es.emp_no from es where es.salary=mm.max_s and es.dept_no=mm.dept_no limit 1) as max_e, mm.max_s,
 (select es.emp_no from es where es.salary=mm.min_s and es.dept_no=mm.dept_no limit 1) as min_e, mm.min_s
from (
 select dept_no, max(salary) as max_s, min(salary) as min_s
 from es group by dept_no
 order by 1 asc
) as mm;
