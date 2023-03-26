import json
import timeout_decorator
from .models import Problem
from db.conn import trainee_conn
from redis import StrictRedis
import pickle as pk
redis = StrictRedis(host='localhost', port='6380', db=1)
redis.execute_command('config set maxmemory 1000MB')


def get_ans(pid: int, sql_type: str, testdb):
    k = str(pid)+sql_type
    v = redis.get(k)
    if v is None:
        ans_sql = Problem.objects.get(pid=pid).__dict__[sql_type]
        with trainee_conn(sql_type, testdb) as c:
            data = execute_sql(c, ans_sql)
            redis.set(k, pk.dumps(data))
            return data
    else:
        data = pk.loads(v)
        return data


def execute_sql(c, sql):
    c.execute(sql)
    row_headers = [x[0]
                   for x in c.description]  # this will extract row headers
    data = c.fetchall()
    return {'header': row_headers, 'data': data}


@timeout_decorator.timeout(6, use_signals=False, timeout_exception=TimeoutError)
def execute_user_sql(c, sql):
    result = execute_sql(c, sql)
    return result


def get_user_sql_result(user_sql, sql_type, testdb):
    with trainee_conn(sql_type, testdb) as c:
        return execute_user_sql(c, user_sql)
