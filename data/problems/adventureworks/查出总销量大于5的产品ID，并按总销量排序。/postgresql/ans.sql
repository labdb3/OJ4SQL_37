
select "ProductID",

sum("OrderQty") as count

from salesorderdetail

group by "ProductID"

having sum("OrderQty")>5

order by sum("OrderQty") desc;


