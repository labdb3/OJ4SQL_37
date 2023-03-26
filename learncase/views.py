from django.shortcuts import render

from utils.logger import *
from utils.config import *


def index(request):
    if request.session['is_login']:
        studentid = request.session['studentid']

        return render(request, "learncase/index.html",{
            "url_1": "http://" + str(Learncase_JupyterHub_IP) + ":" + str(Learncase_JupyterHub_PORT) +  "/user/" + str(studentid) + "/notebooks/commons/Python基础.ipynb",
            "url_2": "http://" + str(Learncase_JupyterHub_IP) + ":" + str(Learncase_JupyterHub_PORT) + "/user/" + str(studentid) + "/notebooks/commons/银行案例.ipynb",
            "url_3": "http://" + str(Learncase_JupyterHub_IP) + ":" + str(Learncase_JupyterHub_PORT) + "/user/" + str(studentid) + "/notebooks/commons/数据库接口技术.ipynb",
            "url_4": "http://" + str(Learncase_JupyterHub_IP) + ":" + str(Learncase_JupyterHub_PORT) +  "/user/" + str(studentid) + "/notebooks/commons/隔离型级别.ipynb"
            })


