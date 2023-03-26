with temp_1 as(select address."City","SalesPersonID",_count
from (select "SalesPersonID",sum("LineTotal") as _count
from salesorderheader inner join salesorderdetail
on salesorderdetail."SalesOrderID"=salesorderheader."SalesOrderID"
group by "SalesPersonID") as Temp inner join businessentityaddress on Temp."SalesPersonID"=businessentityaddress."BusinessEntityID"
               inner join address on  businessentityaddress."AddressID"=address."AddressID")

select "City","SalesPersonID"
from temp_1 a
where (select count(1) from temp_1 b where a."City"=b."City" and a."_count"<b."_count" )<3;
