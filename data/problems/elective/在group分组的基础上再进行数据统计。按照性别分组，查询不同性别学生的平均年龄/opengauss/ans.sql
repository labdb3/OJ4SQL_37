select sex, avg(age)
from student
group by sex with rollup;
