select tc.*
from tc left join sc on tc.cno =sc.cno
where tc.cno is null;
