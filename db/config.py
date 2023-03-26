from collections import namedtuple
DATATABLEMAXLINES = 50
RESULTTABLEMAXLINES = 50

DBIP = '127.0.0.1'
MYSQL_PORT = 43062
POSTGRESQL_PORT = 64321
OPENGAUSS_PORT = 35432

TRAINEE_USER = 's1'
TRAINEE_PSWD = 'students@mysql@DB3'

PRACTISE_HOST = DBIP
PRACTISE_DB = 'testdb'

DBAccount = namedtuple('DBAccount', ['host', 'port', 'db', 'user', 'pswd'])
DBAccounts = namedtuple('DBAccounts', ['mysql', 'postgresql', 'opengauss'])
acnt = DBAccount(DBIP, MYSQL_PORT, PRACTISE_DB, 'teacher', 'Oj4dblcui_')
# 向各个数据库导入表格数据的用户
pg_acnt = acnt._replace(port=POSTGRESQL_PORT)
og_acnt = acnt._replace(port=OPENGAUSS_PORT)
TEACHER = DBAccounts(acnt, pg_acnt, og_acnt)

print(TEACHER)
