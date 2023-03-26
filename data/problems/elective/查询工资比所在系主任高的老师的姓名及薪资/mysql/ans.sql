select   	t1.tname,t1.salary
from      	teacher  t1,teacher  t2,department
where    	t1.dno = department.dno
	and   	department.dean = t2.tno
	and  	t1.salary >t2.salary;
