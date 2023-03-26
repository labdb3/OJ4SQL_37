SELECT
    CITY,
    SNAME
FROM
    S,
    SPJ
WHERE
    S.SNO = SPJ.SNO
GROUP BY
    CITY,
    S.SNO,
    SNAME
HAVING
    sum(QTY) >= ALL (
        SELECT
            sum(SPJ1.QTY)
        FROM
            S S1,
            SPJ SPJ1
        WHERE
            S1.SNO = SPJ1.SNO
            AND S1.CITY = S.CITY
        GROUP BY
            S1.CITY,
            SPJ1.SNO)
