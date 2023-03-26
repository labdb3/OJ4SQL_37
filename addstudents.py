import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'OJ4SQL.settings')
django.setup()

import learnsql.models as learnsql_models
import utils.db_conn as db_conn
import utils.config as config
import user.models as user_models
import argparse


"""
    1. 在 user.User 和 learnsql.User 中新增用户账号
    2. 给learnsql,learncase,practise 创建每个学生的个人数据库
    3. 在jupyterhub 中 创建单独的用户
"""

mysql_template = """
    CREATE DATABASE if not exists {db};
    CREATE USER IF NOT EXISTS {username} identified BY '{passwd}';
    grant ALL PRIVILEGES on {db}.* to {username}@'%';
    flush privileges;
"""

# learnsql_pg_database
postgres_template = """
    CREATE USER  {username} WITH PASSWORD '{passwd}';
    grant connect on database learnsql_pg_database to {username};
    create schema {username};
    grant all on schema {username} to {username};
"""
# learncase_pg_database
learncase_postgres_template = """
    CREATE USER  {username} WITH PASSWORD '{passwd}';
    grant connect on database learncase_pg_database to {username};
    create schema {username};
    grant all on schema {username} to {username};
"""
# practise_pg_database
practise_postgres_template = """
    CREATE USER  {username} WITH PASSWORD '{passwd}';
    grant connect on database practise_pg_database to {username};
    create schema {username};
    grant all on schema {username} to {username};
"""


def read_data(fileName):
    with open(fileName, "r") as f:
        lines = f.readlines()[1:]
        id_name = [line.strip().split("\t")[:2] for line in lines]

    return id_name


def add_user_account(id_name):
    for id, name in id_name:
        # add user to user.User
        try:
            user = user_models.User.objects.get(accountname=id)
        except user_models.User.DoesNotExist:
            u = user_models.User(nickname=name, name=name,
                                 accountname=id, studentid=id, passwd=id)
            u.save()
        # add user to learnsql.User
        try:
            user = learnsql_models.User.objects.get(
                uid=user_models.User.objects.get(studentid=id))
        except learnsql_models.User.DoesNotExist:
            u = learnsql_models.User(uid=user_models.User.objects.get(studentid=id),
                                     mysqlUserName="stu"+str(id),
                                     mysqlUserPassWord="stu"+str(id),
                                     mysqlDBName="stu"+str(id),

                                     postgresqlUserName="stu"+str(id),
                                     postgresqlUserPassWord="stu"+str(id),
                                     postgresqlSchemaName="stu"+str(id))
            u.save()

def add_user_db_learnsql(id_name):
    # learnsql
    with db_conn.MysqlConn4DB(host=config.LearnSql_Mysql_IP,
                              port=config.LearnSql_Mysql_PORT,
                              password=config.LearnSql_Mysql_Password,
                              user=config.LearnSql_Mysql_User) as conn:

        for id, name in id_name:
            sqls = mysql_template.format(
                db="stu"+id, username="stu"+id, passwd="stu"+id)
            for sql in sqls.split(";")[:-1]:
                conn.execute(sql)

    with db_conn.PostgresqlConn(host=config.LearnSql_Postgresql_IP,
                                port=config.LearnSql_Postgresql_PORT,
                                user=config.LearnSql_Postgresql_User,
                                password=config.LearnSql_Postgresql_PassWord,
                                db="learnsql_pg_database"
                                ) as conn:
        for id, name in id_name:
            sqls = postgres_template.format(username="stu"+id, passwd="stu"+id)
            for sql in sqls.split(";")[:-1]:
                conn.execute(sql)


def add_user_db_practise(id_name):
    # practise
    with db_conn.MysqlConn4DB(host=config.Practise_Mysql_IP,
                              port=config.Practise_Mysql_PORT,
                              password=config.Practise_Mysql_PassWord,
                              user=config.Practise_Mysql_User) as conn:

        for id, name in id_name:
            sqls = mysql_template.format(
                db="stu"+id, username="stu"+id, passwd="stu"+id)
            for sql in sqls.split(";")[:-1]:
                conn.execute(sql)

    # with db_conn.PostgresqlConn(host=config.Practise_Postgresql_IP,
    #                             port=config.Practise_Postgresql_PORT,
    #                             user=config.Practise_Postgresql_User,
    #                             password=config.Practise_Postgresql_PassWord,
    #                             db="practise_pg_database"
    #                             ) as conn:
    #     for id, name in id_name:
    #         sqls = practise_postgres_template.format(
    #             username="stu"+id, passwd="stu"+id)
    #         for sql in sqls.split(";")[:-1]:
    #             conn.execute(sql)


def add_user_db_learncase(id_name):
    # learncase
    with db_conn.MysqlConn4DB(host=config.Learncase_Mysql_IP,
                              port=config.Learncase_Mysql_PORT,
                              password=config.Learncase_Mysql_PassWord,
                              user=config.Learncase_Mysql_User) as conn:

        for id, name in id_name:
            sqls = mysql_template.format(
                db="stu"+id, username="stu"+id, passwd="stu"+id)
            for sql in sqls.split(";")[:-1]:
                conn.execute(sql)

    with db_conn.PostgresqlConn(host=config.Learncase_Postgresql_IP,
                                port=config.Learncase_Postgresql_PORT,
                                user=config.Learncase_Postgresql_User,
                                password=config.Learncase_Postgresql_PassWord,
                                db="learncase_pg_database"
                                ) as conn:
        for id, name in id_name:
            sqls = learncase_postgres_template.format(
                username="stu"+id, passwd="stu"+id)
            for sql in sqls.split(";")[:-1]:
                conn.execute(sql)


def grant(id_name):
    with db_conn.MysqlConn4DB(host=config.Practise_Mysql_IP,
                              port=config.Practise_Mysql_PORT,
                              password=config.Practise_Mysql_PassWord,
                              user=config.Practise_Mysql_User) as conn:

        for id, name in id_name:
            sql = "grant select on mysql.* to {}".format("stu"+id)
            
            # sqls = mysql_template.format(
            #     db="stu"+id, username="stu"+id, passwd="stu"+id)
            # for sql in sqls.split(";")[:-1]:
            conn.execute(sql)



def get_args():
    description = 'Add new students.'
    parser = argparse.ArgumentParser(description=description,
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        '--fileName', default="file.csv")
    parser.add_argument('--add_user_account',action="store_true",default=False)
    parser.add_argument('--add_user_db_learnsql',  action="store_true", default=False)
    parser.add_argument('--add_user_db_learncase',
                        action="store_true", default=False)
    parser.add_argument('--add_user_db_practise',
                        action="store_true", default=False)
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = get_args()
    id_name = read_data(args.fileName)
    
    print(id_name)
    #add_user_db_practise(id_name)
    #grant(id_name)
    
    # if args.add_user_account:
    #     add_user_account(id_name)

    # if args.add_user_db_learnsql:
    #     add_user_db_learnsql(id_name)

    # if args.add_user_db_learncase:
    #     add_user_db_learncase(id_name)

    # if args.add_user_db_practise:
    #     add_user_db_practise(id_name)



