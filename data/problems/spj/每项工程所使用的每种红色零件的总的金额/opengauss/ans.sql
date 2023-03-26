SELECT
    jno,
    SPJ.pno,
    sum(qty * price) AS sum_money
    --  sum(qty) AS sum_red_qty
FROM
    SPJ,
    P
WHERE
    SPJ.pno = P.pno
    AND P.color = '红色'
GROUP BY
    SPJ.jno,
    SPJ.pno
ORDER BY
    sum(qty) DESC
