# load的实现包含两部分
# 1. 实现数据库部分，完成数据加载
# 2.
import os
import utils.db_conn as db_conn
import utils.config as config
import pandas as pd


def load_data(fileName, conn):
    for file in os.listdir(fileName):
        if file.endswith(".csv"):
            print(file)
            data = pd.read_csv(fileName + "/" + file, header=0,
                               sep=",").fillna(0)
            headers = data.columns.values.tolist()
            data = data.to_numpy().tolist()
            tablename = file.split(".")[0]
            sql = "insert into {tablename} ({columns}) values({data})".format(
                tablename=tablename, columns=",".join(headers), data=('%s,'*len(data[0]))[:-1]
            )
            print(data[:2],fileName)
            # print(sql,len(data))
            # for i in range(len(data)//10000):
            conn.executemany(sql, data)



def read_data():
    with open("数据库选课名单.csv", "r") as f:
        lines = f.readlines()[1:]
        id_name = [line.strip().split(",")[:2] for line in lines]

    return id_name


def load(fileName, ids):
    with db_conn.MysqlConn(host=config.Practise_Mysql_IP,
                           port=config.Practise_Mysql_PORT, user=config.Practise_Mysql_User,
                           password=config.Practise_Mysql_PassWord,
                           db="dataset") as conn:
        mysql_def = open(fileName+"/mysql.sql").read().strip().split(";")[:-1]
        for sql in mysql_def:
            conn.execute(sql+";")
        load_data(fileName, conn)

        conn.executemany("GRANT select on dataset.* TO %s;", ids)

    # with db_conn.PostgresqlConn(host=config.Practise_Postgresql_IP,
    #                             port=config.Practise_Postgresql_PORT,
    #                             user=config.Practise_Postgresql_User,
    #                             password=config.Practise_Postgresql_PassWord,
    #                             db="practise_pg_database",
    #                             options="-c search_path=dataset") as conn:
    #     pg_def = open(
    #         fileName+"/postgresql.sql").read().strip().split(";")[:-1]
    #     for sql in pg_def:
    #         conn.execute(sql+";")
    #     load_data(fileName, conn)

    #     for id in ids:
    #         conn.execute("grant usage on schema dataset to {};".format(id[0]))
    #         conn.execute(
    #             'GRANT SELECT ON ALL TABLES IN SCHEMA dataset TO {};'.format(id[0]))
    #         conn.execute(
    #             'GRANT SELECT ON ALL SEQUENCES IN SCHEMA dataset TO {};'.format(id[0]))


if __name__ == '__main__':
    id_name = read_data()
    ids = [tuple(["stu" + str(id)]) for id, name in id_name]
    loaded_datasets = ['movielen','TheWorldHappinessReport','xzqh','supermarketTrans']
    for file in loaded_datasets:
        load("data/data/"+file, ids)
