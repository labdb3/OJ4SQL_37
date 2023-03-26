select dname, group_concat(sname separator "|")
from department, student
where student.dno = department.dno
group by dname;
