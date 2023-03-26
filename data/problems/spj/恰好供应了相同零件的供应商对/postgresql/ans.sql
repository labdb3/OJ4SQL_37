SELECT
    S1.SNO,
    S2.SNO
FROM
    S AS S1,
    S AS S2
WHERE
    S1.SNO < S2.SNO
    AND NOT EXISTS (
        SELECT
            *
        FROM
            SPJ AS SPJ1
        WHERE
            SPJ1.SNO = S1.SNO
            AND NOT EXISTS (
                SELECT
                    *
                FROM
                    SPJ
                WHERE
                    SPJ.SNO = S2.SNO
                    AND SPJ.PNO = SPJ1.PNO))
        AND NOT EXISTS (
            SELECT
                *
            FROM
                SPJ AS SPJ2
            WHERE
                SPJ2.SNO = S2.SNO
                AND NOT EXISTS (
                    SELECT
                        *
                    FROM
                        SPJ
                    WHERE
                        SPJ.SNO = S1.SNO
                        AND SPJ.PNO = SPJ2.PNO))
