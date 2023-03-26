SELECT DISTINCT
    SNAME,
    PNAME
FROM
    S
    LEFT OUTER JOIN (
    SELECT
        SPJ.SNO,
        P.PNAME
    FROM
        SPJ,
        P
    WHERE
        SPJ.PNO = P.PNO) AS SP ON S.SNO = SP.SNO
