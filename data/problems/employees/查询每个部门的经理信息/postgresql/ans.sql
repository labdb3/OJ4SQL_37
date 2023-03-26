select dept_name, last_name, first_name
from departments, dept_manager, employees
where departments.dept_no=dept_manager.dept_no
and dept_manager.emp_no=employees.emp_no;
