SELECT
    SNAME
FROM
    S,
    SPJ
WHERE
    S.SNO = SPJ.SNO
GROUP BY
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
        GROUP BY
            S1.SNO)
