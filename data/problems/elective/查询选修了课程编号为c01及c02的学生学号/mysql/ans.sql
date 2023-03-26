select sno
from sc
where
  sc.cno = "c01"
  and sc.sno in (
    select sno
    from sc
    where cno = "c02"
  );
