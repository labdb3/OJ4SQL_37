SELECT
    sname
FROM
    S
WHERE
    NOT EXISTS (
        SELECT
            pno
        FROM
            P
        WHERE
            NOT EXISTS (
                SELECT
                    sno, pno
                FROM
                    SPJ
                WHERE
                    pno = P.pno
                    AND sno = S.sno))
