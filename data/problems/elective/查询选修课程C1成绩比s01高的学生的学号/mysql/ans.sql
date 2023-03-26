select 		s2.sno
from      sc  as  s1,sc  as  s2
where     	s1.sno = 's01'
and     	s1.cno = 'c01'
and     	s2. cno = 'c01'
and      	s1.grade < s2.grade ;
