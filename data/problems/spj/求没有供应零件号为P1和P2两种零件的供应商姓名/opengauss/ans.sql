SELECT sname FROM S WHERE sno NOT IN ( SELECT sno FROM SPJ WHERE pno = 'P1' OR pno = 'P2')
