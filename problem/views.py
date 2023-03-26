import datetime
import time
import json
import math

from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render, reverse, get_object_or_404

from django.forms.models import model_to_dict
from .evaluate import evaluate_async, interpret_solution
from testresult import NAME_resulttype
from . import models
from .models import Problem
from user.models import User
from django.template.loader import render_to_string
from django.db.models import F, Q, When, Count, FilteredRelation


# Create your views here.
def problem_list(request, gid, pno):
    # 查询题目列表，一次返回page_limit条题目和总共的页数

    # 每页显示page_limit条
    page_limit = 50
    display_limit = 5
    group = get_object_or_404(models.Group, gid=gid)
    num_of_problems = models.Problem.objects.filter(gid=gid).count()
    num_of_pages = math.ceil(num_of_problems / page_limit)
    page_numbers = get_page_number(pno, display_limit, num_of_pages)
    start_id = (pno - 1) * page_limit
    query = Problem.objects.annotate(s=FilteredRelation(
        'submission')).filter(Q(gid=gid) & Q(invisible=False))\
        .order_by('pid')\
        .annotate(totalsubmit=Count('s'), totalpass=Count('s', filter=Q(s__resulttype=1))
                  ).values('pid', 'totalsubmit', 'totalpass')
    total_states = query[start_id:start_id+page_limit].values()
    if 'uid' in request.session:
        uid = request.session['uid']
        # TODO: 权限过滤
        query = Problem.objects.annotate(s=FilteredRelation(
            'submission', condition=Q(submission__uid=uid)
        )).filter(Q(gid=gid) & Q(invisible=False) & (Q(s__isnull=True) | Q(s__uid=uid)))\
            .order_by('pid')\
            .annotate(totalsubmit=Count('s'), totalpass=Count('s', filter=Q(s__resulttype=1))
                      ).values('pid', 'title', 'difficulty', 'totalsubmit', 'totalpass')
        result = query[start_id:start_id+page_limit]
    else:
        result = models.Problem.objects.filter(gid=gid, invisible=False).order_by('pid')[
            start_id:start_id+page_limit]
    #  problems = [[r.pid, r.title] for r in result]
    problems = result.values()
    for p, s in zip(problems, total_states):
        if s['totalsubmit'] <= 0:
            p['passrate'] = '--'
        else:
            p['passrate'] = '{:.1f}%'.format(
                100*s['totalpass']/s['totalsubmit'])

    page = {'page_numbers': page_numbers,
            'num_of_pages': num_of_pages}
    group = model_to_dict(group)
    return render(request, 'problem/problem_list.html',
                  {'gid': gid, 'pno': pno, 'group': group,
                      'problems': problems, 'page': page,
                   })


def supported_sql_types(problem):
    sql_types = []
    if problem.mysql:
        sql_types.append('mysql')
    if problem.postgresql:
        sql_types.append('postgresql')
    if problem.postgresql:
        sql_types.append('opengauss')
    return sql_types


def problem_content_description(request, pid):
    # get problem_content_description by id
    problem = get_object_or_404(models.Problem, pid=pid)
    sql_types = supported_sql_types(problem)
    print(problem.gid.basedescription+problem.description)
    rd = {'description': problem.gid.basedescription+problem.description,
          'pid': problem.pid, 'title': problem.title, 'sql_types': sql_types}
    return render(request, 'problem/problem_content_description.html', rd)


def problem_content_submission(request, pid, pno):
    # get problem_content_submission by uid and problem_id
    # Pending & Judging : You solution will be judged soon, please wait for result.
    # Compile Error : Failed to compile your source code. Click on the link to see compiler's output.
    # Accepted : Congratulations. Your solution is correct.
    # Wrong Answer : Your program's output doesn't match judger's answer.
    # Runtime Error : Your program terminated abnormally. Possible reasons are: segment fault, divided by zero or exited with code other than 0.
    # Time Limit Exceeded : The CPU time your program used has exceeded limit.
    # Memory Limit Exceeded : The memory your program actually used has exceeded limit.
    # System Error : Oops, something has gone wrong with the judger. Please report this to administrator.
    if 'uid' not in request.session:
        return HttpResponse("login first!")
    uid = request.session['uid']
    title = get_object_or_404(models.Problem, pid=pid).title

    # 每页显示page_limit条
    page_limit = 10
    display_limit = 5

    nums_of_row = models.Submission.objects.filter(uid=uid, pid=pid).count()

    nums_of_pages = math.ceil(nums_of_row / page_limit)
    page_numbers = get_page_number(pno, display_limit, nums_of_pages)
    start_id = (pno - 1) * page_limit

    rows = models.Submission.objects.filter(
        uid=uid, pid=pid).order_by('-sid')[start_id:start_id+page_limit]
    submissions = [{'sid': r.sid, 'resulttype': NAME_resulttype[r.resulttype], 'info': r.info, 'timespent': r.timespent, 'datetime': r.datetime, 'lang_type':r.lang_type}
                   for r in rows]
    rd = {'submissions': submissions, 'pid': pid, 'page_numbers': page_numbers, 'pno': pno,
          'nums_of_pages': nums_of_pages, 'title': title}
    return render(request, 'problem/problem_content_submission.html', rd)


def problem_content_submission_details(request, sid):
    if 'uid' not in request.session:
        return HttpResponse("login first!")
    _uid = request.session['uid']
    submission = get_object_or_404(models.Submission, sid=sid)
    uid = submission.uid.uid
    if _uid != uid:
        return HttpResponse('无法查看')
    rd = model_to_dict(submission)
    rd['resulttype'] = NAME_resulttype[submission.resulttype]
    rd['pid'] = submission.pid.pid
    rd['title'] = submission.pid.title
    rd['exec_user'] = submission.pid.gid.exec_user
    rd['do_eval'] = submission.pid.gid.do_eval
    rd['display_anssql'] = submission.pid.gid.display_anssql
    rd['echo_result'] = submission.pid.gid.echo_result
    if len(rd['user_result']) > 0:
        rd['user_result'] = json.loads(rd['user_result'])
    else:
        rd['user_result'] = None
    print(submission.pid.gid.display_anssql)
    if submission.pid.gid.display_anssql:
        if submission.lang_type == 'mysql':
            rd['anssql'] = submission.pid.mysql
        elif submission.lang_type == 'postgresql':
            rd['anssql'] = submission.pid.postgresql
        elif submission.lang_type == 'opengauss':
            rd['anssql'] = submission.pid.opengauss
        else:
            print(submission.lang_type)
    return render(request, 'problem/problem_content_submission_details.html', rd)

def problem_content_solution(request, pno):
    # TODO: get problem_content_submission by uid and problem_id
    return HttpResponse("没有题解")


def problem_content_interpret_solution(request, pid):
    if request.method == 'POST':
        if 'uid' not in request.session:
            return JsonResponse({})
        uid = request.session['uid']
        code = request.POST.get('code_submit')
        sql_type = request.POST.get('sql_type')
        print(request.POST)
        problem = get_object_or_404(models.Problem, pid=pid)
        if sql_type not in supported_sql_types(problem):
            return JsonResponse({'msg': '此题不支持'+sql_type})
        if len(code.strip()) == 0:
            return JsonResponse({'msg': 'code is empty!'})
        #  exec_user = problem.gid.do_eval
        #  do_eval = problem.gid.do_eval
        #  display_anssql = problem.gid.display_anssql
        #  echo_result = problem.gid.echo_result
        t1 = time.time()
        result = interpret_solution(
            pid, code, sql_type, problem.testdb, problem.judge)
        print('time for interpret_solution:', time.time()-t1)
        rd = result.to_dict()
        if len(rd['user_result']) > 0:
            rd['user_result'] = json.loads(rd['user_result'])
        else:
            rd['user_result'] = None
        rd = render_to_string('problem/interpret_solution.html', rd)
        return JsonResponse({'interpret_result': rd})


def problem_code_submit(request, pid):
    if request.method == 'POST':
        if 'uid' not in request.session:
            return HttpResponse("login first!")
        uid = request.session['uid']
        code = request.POST.get('code_submit')
        sql_type = request.POST.get('sql_type')
        problem = get_object_or_404(models.Problem, pid=pid)
        if sql_type not in supported_sql_types(problem):
            return HttpResponse('此题不支持'+sql_type)
        if len(code.strip()) == 0:
            return HttpResponse("code is empty!")
        # uid,pid,code,resulttype,info,timespent,datetime
        dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        user = User.objects.get(uid=uid)
        submission = models.Submission(
            uid=user, pid=problem, code=code, datetime=dt, lang_type=sql_type)
        submission.save()
        sid = submission.pk
        exec_user = problem.gid.do_eval
        do_eval = problem.gid.do_eval
        display_anssql = problem.gid.display_anssql
        echo_result = problem.gid.echo_result
        evaluate_async(sid, pid, code, sql_type, problem.testdb,
                       problem.judge, problem.judge_kwargs, exec_user, do_eval, display_anssql, echo_result)
        return redirect(reverse('problem:problem_content_submission_details', kwargs={'sid': sid}))


def get_page_number(pno, display_limit, nums_of_pages):
    page_numbers = []

    if nums_of_pages < display_limit:
        for i in range(nums_of_pages):
            page_numbers.append(i + 1)
    elif nums_of_pages - pno <= 2:
        for i in range(nums_of_pages - 4, nums_of_pages + 1, 1):
            page_numbers.append(i)
    elif pno <= 3:
        for i in range(1, 6, 1):
            page_numbers.append(i)
    else:
        for i in range(pno - 2, pno + 3, 1):
            page_numbers.append(i)

    return page_numbers
