import re
from django.contrib.auth.hashers import check_password, make_password
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render, reverse
from . import models
from utils.jupyterhub import changePasswd
from utils.logger import *

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember = request.POST.get('remember')
        login_from = request.POST.get('login_from')
        print("login_from: ", login_from)
        try:
            user = models.User.objects.get(accountname=username)
            if user.isright(password):
                request.session['is_login'] = True
                request.session['username'] = username
                request.session['nickname'] = user.nickname
                request.session['uid'] = user.uid
                request.session['studentid'] = user.studentid
                
                if not remember:
                    request.session.set_expiry(0)
            else:
                request.session.set_expiry(None)
            return HttpResponseRedirect(login_from)
        except models.User.DoesNotExist:
            return redirect(reverse('index:index'))


def logout(request):
    try:
        request.session.clear()  # 清除所有会话
        request.session.flush()  # 删除当前的会话数据并删除会话的Cookie
    except KeyError:
        pass
    return redirect(reverse('index:index'))


def change_password(request):
    if request.method == 'POST':
        username = request.session['username']
        cur_password = request.POST.get('cur_password')
        new_password = request.POST.get('new_password')
        re_password = request.POST.get('re_password')
        from_url = request.POST.get('from_url')
        studentid = request.session['studentid']
        try:
            user = models.User.objects.get(accountname=username)
        except models.User.DoesNotExist:
            return redirect(reverse('index'))
        if user.isright(cur_password):
            user.passwd = make_password(new_password)
            user.save()
            changePasswd(studentid,new_password)
            logger.info("user {} password changed to {}".format(studentid,new_password))
            return HttpResponseRedirect(from_url)
        return redirect(reverse('index'))
