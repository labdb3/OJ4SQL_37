import pymysql
import psycopg2

from .config import MYSQL_PORT, POSTGRESQL_PORT, OPENGAUSS_PORT
from .config import PRACTISE_HOST, PRACTISE_DB, TRAINEE_PSWD, TRAINEE_USER, TEACHER


class MysqlConn:
    def __init__(self, host, port, user, password, db, multi=False):
        self.host = host
        self.user = user
        self.password = password
        self.port = port
        self.db = db
        if multi:
            multi = pymysql.constants.CLIENT.MULTI_STATEMENTS
        self.multi = multi

    def __enter__(self):
        self.conn = pymysql.connect(
            host=self.host, port=self.port, user=self.user, password=self.password, db=self.db, client_flag=self.multi)
        self.c = self.conn.cursor()
        return self.c

    def __exit__(self, exc_type, exc_value, traceback):
        if self.conn:
            if exc_type:
                self.conn.rollback()
            else:
                self.conn.commit()
        if self.c:
            self.c.close()
        if self.conn:
            self.conn.close()


class PostgresqlConn:
    """pg connection"""

    def __init__(self, host, port, user, password, db, schema=None):
        self.host = host
        self.user = user
        self.password = password
        self.port = port
        self.db = db
        self.schema=schema

    def __enter__(self):
        self.conn = psycopg2.connect(database=self.db, user=self.user,
                                     password=self.password, host=self.host, port=self.port)
        self.conn.set_session(autocommit=False)
        self.c = self.conn.cursor()
        if self.schema:
            self.c.execute("SET search_path TO " + self.schema)
            self.conn.commit()
        return self.c

    def __exit__(self, exc_type, exc_value, traceback):
        if self.conn:
            if exc_type:
                self.conn.rollback()
            else:
                self.conn.commit()
        if self.c:
            self.c.close()
        if self.conn:
            self.conn.close()


def getconnect(ip, port, user, password, db):
    return pymysql.connect(ip, user, password, db)


class TraineeConn(MysqlConn):
    def __init__(self):
        super().__init__(PRACTISE_HOST, MYSQL_PORT, TRAINEE_USER, TRAINEE_PSWD, PRACTISE_DB)


def trainee_conn(sqltype, testdb):
    if sqltype == 'mysql':
        return MysqlConn(PRACTISE_HOST, MYSQL_PORT, TRAINEE_USER, TRAINEE_PSWD, testdb)
    elif sqltype == 'postgresql':
        return PostgresqlConn(PRACTISE_HOST, POSTGRESQL_PORT, TRAINEE_USER, TRAINEE_PSWD, testdb)
    elif sqltype == 'opengauss':
        return PostgresqlConn(PRACTISE_HOST, OPENGAUSS_PORT, TRAINEE_USER, TRAINEE_PSWD, testdb)
    else:
        return None

def custom_conn(sqltype, execdb, user, passwd, multi=False):
    if sqltype == 'mysql':
        return MysqlConn(PRACTISE_HOST, MYSQL_PORT, user, passwd, execdb, multi=multi)
    elif sqltype == 'postgresql':
        return PostgresqlConn(PRACTISE_HOST, POSTGRESQL_PORT, user, passwd, execdb)
    elif sqltype == 'opengauss':
        return PostgresqlConn(PRACTISE_HOST, OPENGAUSS_PORT, user, passwd, execdb)
    else:
        return None

def TeacherConn(sqltype, multi=False, dbname=None, schema=None):
    if sqltype == 'mysql':
        if not dbname:
            dbname = TEACHER.mysql.db
        return MysqlConn(TEACHER.mysql.host, TEACHER.mysql.port, TEACHER.mysql.user, TEACHER.mysql.pswd, dbname, multi=multi)
    elif sqltype == 'postgresql':
        if not dbname:
            dbname = 'postgres'
        return PostgresqlConn(TEACHER.postgresql.host, TEACHER.postgresql.port, TEACHER.postgresql.user, TEACHER.postgresql.pswd, dbname, schema=schema)
    elif sqltype == 'opengauss':
        if not dbname:
            dbname = TEACHER.opengauss.db
        return PostgresqlConn(TEACHER.opengauss.host, TEACHER.opengauss.port, TEACHER.opengauss.user, TEACHER.opengauss.pswd, dbname, schema=schema)
    else:
        return None


if __name__ == "__main__":
    trainee_conn('mysql').__enter__()
    trainee_conn('postgresql').__enter__()
    trainee_conn('opengauss').__enter__()
