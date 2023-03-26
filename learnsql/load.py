import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'OJ4SQL.settings')
django.setup()

from learnsql.models import User,Problems,ProblemTable,TopicProblem,Tables,Topics
from collections import defaultdict
import csv
import os
from utils.extract_table import *


table_define = {
    "student":['str','str','int','str','str','str'],
    "course":['str','str','str','int'],
    "teacher": ['str', 'str', 'str', 'int', 'str'],
    "department":['str','str','str'],
    "sc":['str','str','int'],
    "tc": ['str', 'str']
}


def reinit_managerdb():
    Problems.objects.all().delete()
    ProblemTable.objects.all().delete()
    TopicProblem.objects.all().delete()
    Tables.objects.all().delete()
    Topics.objects.all().delete()



def parse_comment_sql2(f: str):
    problems = open(f).read().strip().split('\n\n')
    # print(problems[-1])
    problems_sqls = []
    for p in problems:
        desc = []
        sqls = defaultdict(list)
        sqltype = 'mysql'
        for line in p.splitlines():
            line = line.strip()
            if line.startswith('--d'):
                desc.append(line[3:])
            elif line.startswith('--t'):
                sqltype = line[3:].strip()
            else:
                sqls[sqltype].append(line)
        desc = '\n'.join(desc)
        if f == "learnsql/tables/problems/索引定义.sql":
            print(sqls)
        for k, v in sqls.items():
            sqls[k] = '\n'.join(v)
        # 默认全部共享相同的查询sql
        if len(sqls)==1 or len(sqls)==2:
            if "postgresql" not in sqls.keys():
                sqls['postgresql']=sqls['mysql']
            if "opengauss" not in sqls.keys():
                sqls['opengauss']=sqls['mysql']
        problems_sqls.append((desc, sqls))
    return problems_sqls


def parse_comment_sql(f: str, first='sql'):
    return parse_comment_sql2(f)

def load_problems():
    problems_dir = 'learnsql/tables/problems/'
    fs = os.listdir(problems_dir)

    for f in fs:
        topic = os.path.splitext(f)[0]
        fpath = os.path.join(problems_dir, f)
        problems_sqls = parse_comment_sql(fpath)
        # print(problems_sqls)

        for pdesc, sqls in problems_sqls:
            sqltypes = list(sqls.keys())
            anss = list(sqls.values())
            if len(anss)!=3: continue

            tables = extract_tables(anss[0])
            # insert into table Problems
            problem = Problems(ptitle="",pdesc=pdesc,mysql=anss[0],postgresql=anss[1])
            problem.save()
            _topic = Topics.objects.get(topicName=topic)
            topicProblem = TopicProblem(topicID=_topic,pid=problem)
            topicProblem.save()
            for table in tables:
                print(type(table),table)
                _Table = Tables.objects.get(tableName = table)
                problemTable = ProblemTable(pid=problem,tableName=_Table)
                problemTable.save()


def load_tables_mysql(csvs, table_data_dir):
    base_dir = "./learnsql/tables/tableinserts/mysql/"

    for f in csvs:
        with open(base_dir+f,"w") as fwrite:
            fwrite.write('SET FOREIGN_KEY_CHECKS = 0;'+"\n")
            table = os.path.splitext(f)[0]
            fpath = os.path.join(table_data_dir, f)
            cr = csv.reader(open(fpath), delimiter=',')
            header = next(cr)

            s=""
            for i in range(len(header)):
                if f.split(".")[0] in table_define.keys() and table_define[f.split(".")[0]][i] == 'str':
                    s += "'{0["+str(i)+"]}',"
                else:
                    s += "{0["+str(i)+"]},"

            sqltemp = 'insert into {}({}) values({});'.format(
                table, ','.join(header), s[:-1])
            for row in cr:
                row = [None if r == '' else r for r in row]
                # print(sqltemp,row)
                fwrite.write(sqltemp.format(row)+"\n")
            fwrite.write('SET FOREIGN_KEY_CHECKS = 1;'+"\n")


def load_tables_pg(csvs, table_data_dir):
    base_dir = "./learnsql/tables/tableinserts/postgresql/"

    for f in csvs:
        with open(base_dir+f,"w") as fwrite:
            table = os.path.splitext(f)[0]
            fpath = os.path.join(table_data_dir, f)
            cr = csv.reader(open(fpath), delimiter=',')
            header = next(cr)
            s = ""
            for i in range(len(header)):
                if f.split(".")[0] in table_define.keys() and table_define[f.split(".")[0]][i] == 'str':
                    s += "'{0["+str(i)+"]}',"
                else:
                    s += "{0["+str(i)+"]},"

            sqltemp = 'insert into {}({}) values({});'.format(
                table, ','.join(header), s[:-1])
            for row in cr:
                row = [None if r == '' else r for r in row]
                fwrite.write(sqltemp.format(row)+"\n")

def gen_insert_sql():
    table_data_dir = './learnsql/tables/table_data'
    #csvs = os.listdir(table_data_dir)
    csvs = ['client.csv', 'bank_card.csv', 'finances_product.csv', 'insurance.csv', 'fund.csv',
            'department.csv', 'property.csv', 'teacher.csv',  'course.csv', 'student.csv', 'tc.csv',  'sc.csv']
    load_tables_mysql(csvs, table_data_dir)
    load_tables_pg(csvs,table_data_dir)

# load Tables
def load_tables():
    # 在后台管理数据库中增加表格描述
    tables_desc_file = './learnsql/tables/table_desc'
    tables_desc = open(tables_desc_file).read().strip().split('\n\n')
    tables_desc = [e.strip().split('\n', 1) for e in tables_desc]

    for name, desc in tables_desc:
        name = name.strip()
        desc = desc.strip()
        table = Tables(tableName = name,tableDesc = desc)
        table.save()

# load Topics
def load_topics():
    topic_data = 'learnsql/tables/topics.csv'
    cr = csv.reader(open(topic_data), delimiter=',')
    header = next(cr)
    # print(header)
    for row in cr:
        topic = Topics(topicID=row[0], topicName=row[1],
                       topicDesc=row[2], topicOrd=row[3], topicParent=row[4])
        topic.save()


if __name__ == '__main__':
    reinit_managerdb()
    load_tables()
    load_topics()
    load_problems()
    # # gen_insert_sql()

