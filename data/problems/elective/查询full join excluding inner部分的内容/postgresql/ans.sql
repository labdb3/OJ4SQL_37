(select	*
from tc left join sc on tc.cno = sc.cno
where sc.cno is null
)
union 
(select *
from tc right join sc on tc.cno = sc.cno
where tc.cno is null);
