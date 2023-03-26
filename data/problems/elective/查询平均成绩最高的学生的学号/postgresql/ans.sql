select sno
from sc
group by sno
having
  avg(grade) >= all (
    select avg(grade)
    from sc
    group by sno
  );

