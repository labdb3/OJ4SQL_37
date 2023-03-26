select sno, avg(grade)
from sc
where grade >= 80
group by sno;
