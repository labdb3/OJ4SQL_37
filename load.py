import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'OJ4SQL.settings')
django.setup()
from load_utils import load_tables_fn, create_database_fn, drop_database_fn, fixperm_fn
from os.path import join as opj
import argparse
from db.conn import trainee_conn, TeacherConn
import pymysql
from collections import defaultdict
import csv
import pdb
import re
from problem import models


def load_tables(args):
    fpath = os.path.join(os.getcwd(), args.path)
    files = os.listdir(fpath)
    define_files = filter(lambda f: f.endswith('.sql'), files)
    csvs = map(lambda f: os.path.join(fpath, f),
               filter(lambda f: f.endswith('.csv'), files))
    for define_file in define_files:
        define_path = os.path.join(fpath, define_file)
        sqltype = os.path.splitext(define_file)[0]
        if sqltype not in args.engines:
            continue
        with open(define_path) as f:
            define = f.read()
            with TeacherConn(sqltype, multi=True, dbname=args.dbname, schema=args.schema) as c:
                c.execute(define)
        if args.schema:
            load_tables_fn[sqltype](csvs, args.dbname, args.schema)
        else:
            load_tables_fn[sqltype](csvs, args.dbname)


def load_problem(args):
    # ans, desc, judge_type
    problem_dir = args.path
    testdb = args.dbname
    title = os.path.basename(os.path.normpath(problem_dir))
    fs = os.listdir(problem_dir)
    if 'desc' not in fs:
        print('desc not found in '+problem_dir)
        return -1
    with open(os.path.join(problem_dir, 'desc')) as f:
        desc = f.read()
    with open(os.path.join(problem_dir, 'judge_type'))as f:
        judge_type = f.read().strip()
    fs.remove('desc')
    fs.remove('judge_type')
    judge_type = next(
        filter(lambda c: c[1] == judge_type, models.Problem.JudgeType.choices))[0]
    ans = {}
    for name in fs:
        fpath = os.path.join(problem_dir, name)
        ans[name] = open(os.path.join(fpath, 'ans.sql')).read().strip()
    confirm = 'title:{}\ndescription:{}\njudge_type:{}\ntestdb:{}\nans:{}\ngid:{}'
    confirm = confirm.format(title, desc, judge_type, testdb, ans, args.gid)
    if not args.yes:
        print(confirm)
        confirm = input('Confirm and save this problem? [Y/N]')
        if confirm not in ['Y', 'y']:
            print('Aborted.')
            exit(0)
    group = models.Group.objects.get(gid=args.gid)
    problem = models.Problem(
        description=desc, title=title, judge=judge_type, testdb=testdb, gid=group, **ans)
    problem.save()


def get_args():
    description = 'Load problems and data into backend and test database.'
    parser = argparse.ArgumentParser(description=description,
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        '--type', choices=['create', 'load', 'problem', 'drop', 'fixperm'], required=True, nargs='+')
    parser.add_argument('--perm', choices=['readonly', 'write'])
    parser.add_argument('--dbname', required=True)
    parser.add_argument(
        '--engines', choices=['mysql', 'postgresql', 'opengauss'], nargs='+')
    parser.add_argument('--path', help='Path of a folder.')
    parser.add_argument('--schema', help='schema for postgresql')
    parser.add_argument('--gid', type=int, help='Group id that owns problem')
    parser.add_argument('-y', '--yes', action='store_true', default=False,
                        help='Parse files directly without prompt.')
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = get_args()
    for atype in args.type:
        if atype == 'load':
            load_tables(args)
        elif atype == 'create':
            for engine in args.engines:
                create_database_fn[engine](args.dbname, args.perm)
        elif atype == 'drop':
            for engine in args.engines:
                drop_database_fn[engine](args.dbname)
        elif atype == 'problem':
            load_problem(args)
        elif atype == 'fixperm':
            for engine in args.engines:
                fixperm_fn[engine](args.dbname, args.perm)
