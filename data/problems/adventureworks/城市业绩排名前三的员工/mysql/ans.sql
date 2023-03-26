with temp_1 as(select city,SalesPersonID,_count
from (select SalesPersonID,sum(LineTotal) as _count
from salesorderheader inner join salesorderdetail
where salesorderdetail.SalesOrderID=salesorderheader.SalesOrderID
group by SalesPersonID) Temp join businessentityaddress join address 
where Temp.SalesPersonID=businessentityaddress.BusinessEntityID 
and businessentityaddress.AddressID=address.AddressID)

select city,SalesPersonID
from temp_1 a
where (select count(1) from temp_1 b where a.city=b.city and a._count<b._count )<3;
