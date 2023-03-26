select dept_no, SUBSTRING_INDEX(group_concat(last_name order by last_name ASC separator ','),',',5)
from dept_emp natural join employees
group by dept_no;
