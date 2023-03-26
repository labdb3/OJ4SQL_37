SELECT p."Name" AS ProductName,

"OrderQty" * "UnitPrice" as NonDiscountSales,

(("OrderQty" * "UnitPrice") * "UnitPriceDiscount") as Discounts

FROM product AS p

INNER JOIN salesorderdetail AS sod

ON p."ProductID" = sod."ProductID"

ORDER BY "Name" DESC;



