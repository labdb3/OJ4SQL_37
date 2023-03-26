select sname
from student
where
  sno in ( select sno
    from sc
    where cno = "c01"
  );
