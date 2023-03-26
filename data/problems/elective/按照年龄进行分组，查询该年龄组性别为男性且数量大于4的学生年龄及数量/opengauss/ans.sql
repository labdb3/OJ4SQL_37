select age, count(sno)
from student
where sex = "M"
group by age
having count(*) > 4;

