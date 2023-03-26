from .execute import get_user_sql_result, get_ans
from decimal import Decimal
import importlib
import time
import datetime
import threading
import json

import testresult as tr
from db.conn import trainee_conn
from . import models, judge

semaphores = {'mysql': threading.Semaphore(
    5), 'postgresql': threading.Semaphore(5),
    'opengauss': threading.Semaphore(5)
}


def evaluate_th(sid: int, pid: int, user_sql: str, sql_type, testdb, judge_type, judge_kwargs, exec_user, do_eval, display_anssql, echo_result, save=True):
    semaphores[sql_type].acquire()
    user_result_jsonstr = ''
    result = tr.get_blank()
    try:
        if exec_user:
            try:
                t1 = time.time()
                user_result = get_user_sql_result(user_sql, sql_type, testdb)
                print('user_result:', user_result)
                t2 = time.time()
                delta_t = int((t2-t1)*1000)
                result.time = delta_t
                if echo_result and user_result:
                    resultData = [[str(f) if isinstance(f, Decimal) else
                                   'NULL' if f is None else
                                   str(f) if isinstance(f, datetime.date) else
                                   f for f in row]
                                  for row in user_result['data'][:102]]
                    user_result_jsonstr = json.dumps(
                        {'fieldNames': user_result['header'], 'data': resultData})
                    result.user_result = user_result_jsonstr
                # 需要评测用户SQL的正确性
                if do_eval:
                    stand_result = get_ans(pid, sql_type, testdb)
                    print('user_result:', user_result)
                    print('stand_result:', stand_result)
                    try:
                        ifpass, judgeinfo = judge.judge(
                            user_result, stand_result, judge_type, judge_kwargs, sql_type)
                        if ifpass:
                            result.type = tr.Accepted
                        else:
                            result.type = tr.WRONGANSWER
                            result.info = judgeinfo
                    except Exception as e:
                        result.type = tr.WRONGANSWER
            except TimeoutError:
                result.type = tr.TIMEOUT
            except Exception as e:
                result.type = tr.RUNERR
                result.info = str(e)
        if save:
            models.Submission.objects.filter(sid=sid).update(
                resulttype=result.type, info=result.info, timespent=result.time, user_result=result.user_result)
    except Exception as e:
        print(e)
        result = tr.evalResult(tr.SYSERR, tr.INFO_SYSCON)
        if save:
            models.Submission.objects.filter(sid=sid).update(
                resulttype=result.type, info=result.info, user_result=result.user_result)
    finally:
        semaphores[sql_type].release()
    return result


def evaluate_async(*args):
    threading.Thread(target=evaluate_th, args=args).start()


def evaluate_sync(*args):
    return evaluate_th(*args)


def interpret_solution(pid, user_sql, sql_type, testdb, judge_type):
    result = evaluate_sync(-1, pid, user_sql, sql_type,
                           testdb, judge_type, None, True, False, True, True, False)
    return result


if __name__ == "__main__":
    pass
