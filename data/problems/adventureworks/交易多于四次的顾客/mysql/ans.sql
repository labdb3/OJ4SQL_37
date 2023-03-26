SELECT CustomerID, SalesOrderID, OrderDate
FROM salesorderheader 
WHERE CustomerID IN     
(SELECT CustomerID     
FROM salesorderheader     
GROUP BY CustomerID    
HAVING COUNT(*) > 4);
