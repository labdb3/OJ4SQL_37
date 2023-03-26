select sno, avg(grade)
from sc
group by sno
having min(grade) >= 80;
