select sno, max(grade), min(grade), avg(grade)
from sc
group by sno;
