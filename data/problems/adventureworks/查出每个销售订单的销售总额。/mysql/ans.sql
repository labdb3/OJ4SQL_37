
select salesorderdetail.SalesOrderID,sum(LineTotal) as total

from salesorderdetail

group by SalesOrderID;





