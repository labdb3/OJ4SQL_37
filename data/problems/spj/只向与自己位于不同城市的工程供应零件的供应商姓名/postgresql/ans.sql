select distinct sname
from S,SPJ
where SPJ.sno = S.sno and S.sno not in
(select S.sno
from SPJ, S, J
where SPJ.sno = S.sno and SPJ.jno = J.jno and S.city = J.city)
