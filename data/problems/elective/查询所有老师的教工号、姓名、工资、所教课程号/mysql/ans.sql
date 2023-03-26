select teacher.tno,tname,salary,cno
from teacher left join tc on teacher.tno = tc.tno;

