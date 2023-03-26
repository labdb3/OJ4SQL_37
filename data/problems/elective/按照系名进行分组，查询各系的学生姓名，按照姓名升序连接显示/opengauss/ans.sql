select dname, group_concat(sname order by sname)
from department, student
where student.dno = department.dno
group by dname;
