import time
import datetime

import pymysql

while True:
    try:
        conn = pymysql.connect(host="127.0.0.1", port=43062,
                             user="root", password="root@lab3")
        c = conn.cursor()

        while True:
            c.execute("show processlist")
            result = c.fetchall()
            testexes = list(filter(lambda r: len(
                r[1]) == 2 and r[1] == 's1' and r[5] > 10 and r[6] == "executing", result))
            logs = []
            for e in testexes:
                sql = "kill "+str(e[0])
                c.execute(sql)
                print(sql)
                logs.append(sql)
            t = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            logs = [t+' '+log for log in logs]
            if len(logs)>0:
                with open('killzombie.log', 'at') as f:
                    f.write('\n'.join(logs))
            time.sleep(10)
        c.close()
        conn.close()
    except Exception as e:
        print(e)
        time.sleep(5)

