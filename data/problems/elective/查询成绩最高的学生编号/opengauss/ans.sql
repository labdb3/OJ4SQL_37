select sno
from sc
where grade = (select max(grade)from sc);
