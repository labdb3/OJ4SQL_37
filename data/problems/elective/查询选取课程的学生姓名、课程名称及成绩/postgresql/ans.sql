select	sname, cname, grade
from   	student , course,sc
where  	student.sno = sc.sno
	and course.cno = sc.cno;
