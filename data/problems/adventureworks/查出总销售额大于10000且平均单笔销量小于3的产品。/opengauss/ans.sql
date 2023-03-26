
select "ProductID",

avg("UnitPrice") avg_price,sum("LineTotal") as sum_LineTotal

from salesorderdetail

group by "ProductID"

having avg("OrderQty")<3

and sum("LineTotal")>10000;



