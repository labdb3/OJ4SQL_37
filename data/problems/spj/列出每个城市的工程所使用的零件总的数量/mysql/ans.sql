SELECT
    CITY,
    sum(QTY)
FROM
    J,
    SPJ
WHERE
    J.JNO = SPJ.JNO
GROUP BY
    CITY
