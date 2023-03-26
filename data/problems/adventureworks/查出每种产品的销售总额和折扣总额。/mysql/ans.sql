

select Name , LineTotal, OrderQty*UnitPriceDiscount as discount

from product join salesorderdetail

on product.ProductID=salesorderdetail.ProductID

order by Name asc;




