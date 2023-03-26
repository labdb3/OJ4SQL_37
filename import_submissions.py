import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'OJ4SQL.settings')
django.setup()
from user.models import User
from problem.models import Submission, Problem
import pickle  as pk

'accountname, pid, code,resulttype, info, timespent, datetime'
with open('./submissions.pk', 'rb') as f:
    submissions = pk.load(f)

submissions = [sub[0] for sub in submissions]
for sub in submissions:
    print(sub[:2])
    accountname, pid, code,resulttype, info, timespent, datetime = sub
    #  u = User.objects.get(accountname=accountname)
    #  p = Problem.objects.get(pid=pid)
    #  sub = Submission(pid=p,uid=u,code=code,resulttype=resulttype,info=info,timespent=timespent,datetime=datetime,lang_type='mysql')
    #  sub.save()
