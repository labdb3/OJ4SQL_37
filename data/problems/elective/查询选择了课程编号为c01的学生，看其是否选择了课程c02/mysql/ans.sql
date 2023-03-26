select sno
from sc sc1
where sc1.cno = "c01"
  and exists (
    select sno
    from sc
    where cno = "c02" and sno = sc1.sno
  );
