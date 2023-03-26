select sname
from student
where exists (
    select *
    from sc
    where cno = "c01" and sno = student.sno
  );
