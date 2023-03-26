
select ProductModelID

from product

group by product.ProductModelID

having  MAX(ListPrice)=avg(ListPrice);




