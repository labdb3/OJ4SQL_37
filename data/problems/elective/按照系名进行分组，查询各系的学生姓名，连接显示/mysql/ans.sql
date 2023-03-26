select dname, group_concat(sname)
from department, student
where student.dno = department.dno
group by dname;
