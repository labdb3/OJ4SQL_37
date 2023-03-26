
select "ProductModelID",

avg("ListPrice")

from product

where "ListPrice">1000

group by "ProductModelID";



