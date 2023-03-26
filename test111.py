import pymysql


class MysqlConn:
    def __init__(self, host, port, user, password, db):
        self.host = host
        self.user = user
        self.password = password
        self.port = port
        self.db = db

    def __enter__(self):
        self.conn = pymysql.connect(
            host=self.host, port=self.port, user=self.user, password=self.password, db=self.db, charset="utf8")
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_value, traceback):
        if self.conn:
            if exc_type:
                self.conn.rollback()
            else:
                self.conn.commit()
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()


def get_conn():
    with MysqlConn(host="localhost",
                   user="root",
                   password="root@lab3",
                   port=43062,
                   db="spj") as conn:
        conn.execute("select * from S")
        S = conn.fetchall()
        conn.execute("select * from SPJ")
        SPJ = conn.fetchall()
        dic = {}
        for item in SPJ:
            if item[0] not in dic.keys():
                dic[item[0]]=set()
                dic[item[0]].add(item[1])
            else:
                dic[item[0]].add(item[1])
        ans = set()
        for item in S:
            for item1 in S:
                ans.add((item[0],item1[0]))
        res = []
        for item in ans:
            if item[0] not in dic.keys() and item[1] not in dic.keys():
                res.append(item)
            elif dic[item[0]]==dic[item[1]]:
                res.append(item)
        print(res)
        
        


if __name__=='__main__':
    get_conn()

