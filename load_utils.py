import csv
from collections import defaultdict
import pymysql
from db.conn import trainee_conn, TeacherConn
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from os.path import join as opj
import os


def load_tables_mysql(csvs, dbname):
    with TeacherConn('mysql', dbname=dbname) as c:
        c.execute('SET FOREIGN_KEY_CHECKS = 0')
        for fpath in csvs:
            table = os.path.splitext(os.path.basename(fpath))[0]
            cr = csv.reader(open(fpath), delimiter=',')
            header = next(cr)
            header = ['`{}`'.format(h) for h in header]
            sqltemp = 'insert into {}({}) value({})'.format(
                table, ','.join(header), ('%s,'*len(header))[:-1])
            for ri, row in enumerate(cr):
                try:
                    row = [None if r == '' else r for r in row]
                    c.execute(sqltemp, row)
                except Exception as e:
                    print('fpath:{} row:{}'.format(fpath, ri))
                    print(row)
                    raise e
            print(fpath, 'loaded into mysql')
        c.execute('SET FOREIGN_KEY_CHECKS = 1')


def load_tables_pg(csvs, dbname, schema):
    with TeacherConn('postgresql', dbname=dbname, schema=schema) as c:
        c.execute("SET session_replication_role = 'replica';")
        for fpath in csvs:
            table = os.path.splitext(os.path.basename(fpath))[0]
            cr = csv.reader(open(fpath), delimiter=',')
            header = next(cr)
            #  sqltemp = 'insert into {}({}) values({})'.format(
            #      table, ','.join(header), ('%s,'*len(header))[:-1])
            sqltemp = 'insert into {} values({})'.format(
                table, ('%s,'*len(header))[:-1])
            for row in cr:
                row = [None if r == '' else r for r in row]
                c.execute(sqltemp, row)
            print(fpath, 'loaded into postgresql')
        c.execute("SET session_replication_role = 'origin';")


def load_tables_og(csvs, dbname):
    with TeacherConn('opengauss', dbname=dbname) as c:
        c.execute("SET session_replication_role = 'replica';")
        for fpath in csvs:
            table = os.path.splitext(os.path.basename(fpath))[0]
            cr = csv.reader(open(fpath), delimiter=',')
            header = next(cr)
            sqltemp = 'insert into {}({}) values({})'.format(
                table, ','.join(header), ('%s,'*len(header))[:-1])
            for row in cr:
                row = [None if r == '' else r for r in row]
                c.execute(sqltemp, row)
            print(fpath, 'loaded into opengauss')
        c.execute("SET session_replication_role = 'origin';")


def clear_mysqldb(c):
    c.execute("select database()")
    db_name = c.fetchone()[0]
    sql = "SELECT table_name FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = '{}'"
    c.execute(sql.format(db_name))
    names = c.fetchall()
    dropall = ['drop table {};'.format(name[0]) for name in names]
    dropall = ['SET FOREIGN_KEY_CHECKS=0;'] + \
        dropall+['SET FOREIGN_KEY_CHECKS=1;']
    for sql in dropall:
        c.execute(sql)


def clear_postgresqldb(c):
    sql = 'SELECT table_name FROM information_schema.tables WHERE table_schema=current_schema()'
    c.execute(sql)
    r = c.fetchall()
    sql = 'DROP TABLE {} CASCADE'
    for table_name in r:
        c.execute(sql.format(table_name[0]))


def clear_opengaussdb(c):
    sql = 'SELECT table_name FROM information_schema.tables WHERE table_schema=current_schema()'
    c.execute(sql)
    r = c.fetchall()
    print('opengauss:', r)
    sql = 'DROP TABLE {} CASCADE'
    for table_name in r:
        print(sql.format(table_name[0]))
        c.execute(sql.format(table_name[0]))


def clear_practisedb():
    # 清空练习数据库里的所有表和约束
    with TeacherConn('mysql') as ct:
        clear_mysqldb(ct)
    with TeacherConn('postgresql') as ct:
        clear_postgresqldb(ct)
    #  with TeacherConn('opengauss') as ct:
    #      clear_opengaussdb(ct)


def fixperm_mysql(dbname, perm):
    sql = 'GRANT select ON {}.* TO student_role_s;'.format(dbname)
    if perm == 'readonly':
        with TeacherConn('mysql') as c:
            c.execute(sql)
    elif perm == 'write':
        sql = 'GRANT select,create,drop,update,alter on {}.* TO student_role_s;'.format(
            dbname)
        with TeacherConn('mysql') as c:
            c.execute(sql)


def create_database_mysql(dbname, perm):
    sql = 'create database '+dbname
    with TeacherConn('mysql') as c:
        c.execute(sql)
    fixperm_mysql(dbname, perm)


def fixperm_pg(dbname, perm):
    sql = '''REVOKE CREATE ON schema public FROM public;
GRANT CONNECT ON DATABASE {} TO s1;
GRANT USAGE ON SCHEMA public TO s1;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO s1;
GRANT SELECT ON ALL SEQUENCES IN SCHEMA public TO s1;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO s1;'''
    sql = sql.format(dbname)
    if perm == 'readonly':
        with TeacherConn('postgresql', dbname=dbname) as c:
            c.execute(sql)
    elif perm == 'write':
        sql = 'GRANT SELECT,UPDATE,INSERT ON ALL TABLES IN SCHEMA public TO s1;\
               GRANT CREATE ON SCHEMA public TO s1;'
        with TeacherConn('postgresql', dbname=dbname) as c:
            c.execute(sql)


def create_database_pg(dbname, perm):
    sql = 'create database '+dbname
    with TeacherConn('postgresql') as c:
        c.connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        c.execute(sql)
    fixperm_pg(dbname, perm)


def fixperm_og(dbname, perm):
    sql = '''REVOKE CREATE ON schema public FROM public;
GRANT CONNECT ON DATABASE {} TO s1;
GRANT USAGE ON SCHEMA public TO s1;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO s1;
GRANT SELECT ON ALL SEQUENCES IN SCHEMA public TO s1;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO s1;'''
    sql = sql.format(dbname)
    if perm == 'readonly':
        with TeacherConn('opengauss', dbname=dbname) as c:
            c.execute(sql)
    elif perm == 'write':
        sql = 'GRANT SELECT,UPDATE,INSERT ON ALL TABLES IN SCHEMA public TO s1;\
               GRANT CREATE ON SCHEMA public TO s1;'
        with TeacherConn('opengauss', dbname=dbname) as c:
            c.execute(sql)


def create_database_og(dbname, perm):
    sql = 'create database '+dbname
    with TeacherConn('opengauss') as c:
        c.connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        c.execute(sql)
    fixperm_og(dbname, perm)


def drop_database_mysql(dbname):
    sql = 'drop database '+dbname
    with TeacherConn('mysql') as c:
        c.execute(sql)


def drop_database_pg(dbname):
    sql = 'drop database '+dbname
    with TeacherConn('postgresql') as c:
        c.connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        c.execute(sql)


def drop_database_og(dbname):
    sql = 'drop database '+dbname
    with TeacherConn('opengauss') as c:
        c.connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        c.execute(sql)


def create_database_all(dbname):
    create_database_mysql(dbname)
    create_database_pg(dbname)
    create_database_og(dbname)


def fixperm_all(dbname, perm):
    fixperm_mysql(dbname, perm)
    fixperm_pg(dbname, perm)
    fixperm_og(dbname, perm)


load_tables_fn = {'mysql': load_tables_mysql,
                  'postgresql': load_tables_pg, 'opengauss': load_tables_og}

create_database_fn = {'mysql': create_database_mysql,
                      'postgresql': create_database_pg, 'opengauss': create_database_og}
fixperm_fn = {'mysql': fixperm_mysql,
              'postgresql': fixperm_pg, 'opengauss': fixperm_og}
drop_database_fn = {'mysql': drop_database_mysql,
                    'postgresql': drop_database_pg, 'opengauss': drop_database_og}
