import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'OJ4SQL.settings')
django.setup()

from sqlite3 import SQLITE_DENY
import utils.db_conn as db_conn
from decimal import Decimal
import json
from django.http import HttpResponse
import timeout_decorator
from django.shortcuts import render
from utils.logger import *
import utils.config as config
from learnsql.models import TopicProblem,Topics,Problems,ProblemTable,User
import user.models as user_models


def nav(request):
    all_data = get_all_data()

    return render(request, "learnsql/nav.html", {
        "firstTopics": all_data
    })


def nav_second(request, firstTopicID):
    #
    all_data = get_all_data()
    logger.info("call nav_second:\t[firstTopicID={}]".format(
        all_data[firstTopicID].keys()))
    
    return render(request, "learnsql/desc.html", {
        "secondTopics": all_data[firstTopicID]["secondTopics"]
    })


def topic(request, thirdTopicID):
    sqltype = request.GET.get("sqltype", 'mysql')
    logger.info("call topic:\t [sqltype={},thirdTopicID={}]".format(
        sqltype, thirdTopicID))

    assert sqltype in ['mysql', 'postgresql']

    firstTopicID = None
    # pid,ptitle,pdesc,mysql,pg,op
    all_data = get_all_data()
    for k1 in all_data:
        for k2 in all_data[k1]["secondTopics"]:
            for k3 in all_data[k1]["secondTopics"][k2]["thirdTopics"]:
                if k3 == thirdTopicID:
                    firstTopicID = k1

                    problems = all_data[k1]["secondTopics"][k2]["thirdTopics"][k3]["problems"]
                    pros = []
                    if sqltype == "mysql":
                        for problem in problems:
                            pros.append(problem[:-1])
                    elif sqltype == "postgresql":
                        for problem in problems:
                            pros.append(problem[:-2]+[problem[-1]])


    tables = []
    datas = TopicProblem.objects.filter(topicID=Topics.objects.get(topicID=thirdTopicID))
    for data in datas:
        try:
            _ = ProblemTable.objects.filter(pid=data.pid)
            for __ in _:
                __ = __.tableName
                tables.append([__.tableName,__.tableDesc])
        except ProblemTable.DoesNotExist:
            continue
    
    studentid = request.session['studentid']
    studentinfo = User.objects.get(
        uid=user_models.User.objects.get(studentid=studentid))

    if sqltype == "mysql":

        with db_conn.MysqlConn(host=config.LearnSql_Mysql_IP,
                               port=config.LearnSql_Mysql_PORT,
                               user=studentinfo.mysqlUserName,
                               db=studentinfo.mysqlDBName,
                               password=studentinfo.mysqlUserPassWord) as cm:
            tables_fields = dict()
            tables_data = dict()
            cm.execute("show tables")
            existing_tables = [table[0] for table in cm.fetchall()]
            logger.info(existing_tables)

            for tablename, _ in tables:
                if tablename not in existing_tables:
                    continue

                sql = 'SHOW COLUMNS FROM {}'.format(tablename)
                cm.execute(sql)
                cols = cm.fetchall()
                cols = [col[0] for col in cols]
                logger.info(cols)
                tables_fields[tablename] = cols
                sql = 'select * from {}'.format(tablename)
                cm.execute(sql)
                data = cm.fetchall()
                data = [['NULL' if f is None else f for f in row]
                        for row in data]
                tables_data[tablename] = data

        logger.info("table_fields:", tables_fields)
        res = []

        for table in tables:
            if table[0] not in existing_tables:
                continue
            res.append(
                [table[0], table[1], tables_fields[table[0]], tables_data[table[0]]])

        return render(request, "learnsql/topic.html", {
            "problems": pros,
            "secondTopics": all_data[firstTopicID]["secondTopics"],
            "sqltype": sqltype,
            "tables": res
        })
    elif sqltype == "postgresql":
        with db_conn.PostgresqlConn(host=config.LearnSql_Postgresql_IP,
                                    port=config.LearnSql_Postgresql_PORT,
                                    user=studentinfo.postgresqlUserName,
                                    password=studentinfo.postgresqlUserPassWord,
                                    db="learnsql_pg_database",
                                    options="-c search_path={}".format(
                                        studentinfo.postgresqlSchemaName)
                                    ) as cm:
            tables_fields = dict()
            tables_data = dict()
            cm.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = '{}';".format(
                studentinfo.postgresqlSchemaName))
            existing_tables = [table[0] for table in cm.fetchall()]
            logger.info(existing_tables)

            for tablename, _ in tables:
                if tablename not in existing_tables:
                    continue

                cm.execute("Select * FROM {} LIMIT 0".format(tablename))
                cols = [desc[0] for desc in cm.description]
                tables_fields[tablename] = cols
                sql = 'select * from {}'.format(tablename)
                cm.execute(sql)
                data = cm.fetchall()
                data = [['NULL' if f is None else f for f in row]
                        for row in data]
                tables_data[tablename] = data

        logger.info("table_fields:", tables_fields)
        res = []

        for table in tables:
            if table[0] not in existing_tables:
                continue
            res.append(
                [table[0], table[1], tables_fields[table[0]], tables_data[table[0]]])
        return render(request, "learnsql/topic.html", {
            "problems": pros,
            "secondTopics": all_data[firstTopicID]["secondTopics"],
            "sqltype": sqltype,
            "tables": res
        })

    else:
        return render(request, "learnsql/topic.html", {
            "problems": pros,
            "secondTopics": all_data[firstTopicID]["secondTopics"],
            "sqltype": sqltype,
            "tables": []
        })


@timeout_decorator.timeout(5, use_signals=False, timeout_exception=TimeoutError)
def execute_code(sqltype, sqls,studentinfo):
    if sqltype == "mysql":
        with db_conn.MysqlConn(host=config.LearnSql_Mysql_IP,
                               port=config.LearnSql_Mysql_PORT,
                               user=studentinfo.mysqlUserName,
                               db=studentinfo.mysqlDBName,
                               password=studentinfo.mysqlUserPassWord) as ct:
            try:
                for sql in sqls.strip().split(";")[:-1]:
                    ct.execute(sql+";")
            except Exception as e:
                return {"error": str(e)}

            if len(sqls.strip().split(";")[:-1]) > 0 and (sqls.strip().split(";")[:-1][-1].lower().strip().startswith("select") or sqls.strip().split(";")[:-1][-1].lower().strip().startswith("show")):
                cols = ct.description
                resultName = [col[0] for col in cols]
                resultData = ct.fetchall()
                resultData = [[str(f) if isinstance(
                    f, Decimal) else 'NULL' if f is None else f for f in row] for row in resultData]
                result = {'fieldNames': resultName, 'data': resultData}
                return result
            else:
                return {"status": "OK"}
    elif sqltype == "postgresql":
        with db_conn.PostgresqlConn(host=config.LearnSql_Postgresql_IP,
                                    port=config.LearnSql_Postgresql_PORT,
                                    user=studentinfo.postgresqlUserName,
                                    password=studentinfo.postgresqlUserPassWord,
                                    db="learnsql_pg_database",
                                    options="-c search_path={}".format(
                                        studentinfo.postgresqlSchemaName)
                                    ) as ct:

            try:
                for sql in sqls.strip().split(";")[:-1]:
                    ct.execute(sql+";")
            except Exception as e:
                return {"error": str(e)}

            if len(sqls.strip().split(";")[:-1]) > 0 and (sqls.strip().split(";")[:-1][-1].lower().strip().startswith("select") or sqls.strip().split(";")[:-1][-1].lower().strip().startswith("show")):
                cols = ct.description
                resultName = [col[0] for col in cols]
                resultData = ct.fetchall()
                resultData = [[str(f) if isinstance(
                    f, Decimal) else 'NULL' if f is None else f for f in row] for row in resultData]
                result = {'fieldNames': resultName, 'data': resultData}
                return result
            else:
                return {"status": "OK"}
    else:
        return {}
def submitsql(request, pid):
    if request.method == "POST" and request.session['is_login']:
        payload = json.loads(request.body)
        sql = payload["sql"]
        sqltype = payload["sqltype"]
        studentid = request.session['studentid']
        logger.info("call submitsql():\t[studentid={},sql={},sqltype={}]".format(
            studentid, sql, sqltype))

        if sql:
            studentinfo = User.objects.get(uid=user_models.User.objects.get(studentid=studentid))
            result = execute_code(sqltype, sql,studentinfo)
            return HttpResponse(json.dumps(result), content_type="application/json")
        else:
            return HttpResponse()
    else:
        return HttpResponse("请登录")


# get all topic data
"""
{
    firstTopicID:{
        "topicName":,
        "topicdesc":,
        "topicOrd":,
        secondTopics:{
            secondTopicID:{
                "topicName":,
                "topicdesc":,
                "topicOrd":,
                thirdTopics:{
                    thirdTopicID:{
                        "topicName":,
                        "topicdesc":,
                        "topicOrd":,
                        Problems:[[pid,ptitle,pdesc,mysql,pg]]
                    }
                }
            }
        }
    }
}
"""


def get_all_data():
    all_data = {}

    records = Topics.objects.all()
    par = {}
    for record in records:
        par[record.topicID] = record.topicParent

    topic_data = {}
    for record in records:
        topic_data[record.topicID] = [record.topicName, record.topicDesc, record.topicOrd]

    records = Problems.objects.all()
    problems = {}
    for record in records:
        problems[record.pid] = [record.pid, record.ptitle,
                                   record.pdesc, record.mysql, record.postgresql]

    records = TopicProblem.objects.all()
    topicProblems = {}
    for record in records:
        topicProblems[record.pid.pid] = record.topicID.topicID

    topic_problems = {}
    for pid in problems:
        if topicProblems[pid] not in topic_problems.keys():
            topic_problems[topicProblems[pid]] = []
            topic_problems[topicProblems[pid]].append(problems[pid])
        else:
            topic_problems[topicProblems[pid]].append(problems[pid])

    # get all first topic [topicPar=0]
    for key, value in par.items():
        if value == 0:
            all_data[key] = {}
    # get all second topic
    for k in all_data:
        for key, value in par.items():
            if k == value:
                if "secondTopics" not in all_data[k].keys():
                    all_data[k]["secondTopics"] = {}
                all_data[k]["secondTopics"][key] = {}

    # get all third topic
    for k1 in all_data:
        for k2 in all_data[k1]["secondTopics"]:
            for key, value in par.items():
                if k2 == value:
                    if "thirdTopics" not in all_data[k1]["secondTopics"][k2].keys():
                        all_data[k1]["secondTopics"][k2]["thirdTopics"] = {}
                    all_data[k1]["secondTopics"][k2]["thirdTopics"][key] = {}

    # fill data
    for k1 in all_data:
        all_data[k1]["topicName"] = topic_data[k1][0]
        all_data[k1]["topicdesc"] = topic_data[k1][1]
        all_data[k1]["topicOrd"] = topic_data[k1][2]
        for k2 in all_data[k1]["secondTopics"]:
            all_data[k1]["secondTopics"][k2]["topicName"] = topic_data[k2][0]
            all_data[k1]["secondTopics"][k2]["topicdesc"] = topic_data[k2][1]
            all_data[k1]["secondTopics"][k2]["topicOrd"] = topic_data[k2][2]
            for k3 in all_data[k1]["secondTopics"][k2]["thirdTopics"]:
                all_data[k1]["secondTopics"][k2]["thirdTopics"][k3]["topicName"] = topic_data[k3][0]
                all_data[k1]["secondTopics"][k2]["thirdTopics"][k3]["topicdesc"] = topic_data[k3][1]
                all_data[k1]["secondTopics"][k2]["thirdTopics"][k3]["topicOrd"] = topic_data[k3][2]
                if k3 in topic_problems.keys():
                    all_data[k1]["secondTopics"][k2]["thirdTopics"][k3]["problems"] = topic_problems[k3]
                else:
                    all_data[k1]["secondTopics"][k2]["thirdTopics"][k3]["problems"] = [
                    ]
    return all_data


if __name__ == '__main__':
    print(get_all_data())
