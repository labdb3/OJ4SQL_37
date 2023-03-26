from django.shortcuts import render

from utils.logger import *
from utils.config import *


def index(request):
    if request.session['is_login']:
        studentid = request.session['studentid']
        sqltype = request.GET.get("sqltype", 'mysql')

        assert sqltype in ['mysql', 'postgresql', 'opengauss']

        url_prefix = "http://" + str(Practise_JupyterHub_IP) + ":" + str(Practise_JupyterHub_PORT) + "/user/" + str(studentid) + "/notebooks/commons/"


        datasets = {
            "mysql":{
                "stock": url_prefix + "stock-mysql.ipynb",
                "titanic": url_prefix + "titanic-mysql.ipynb",
                "超市的购物数据集示例": url_prefix + "超市的购物数据集示例.ipynb",
                "行政区划数据集示例": url_prefix + "行政区划数据集示例.ipynb",
                "世界幸福指标数据集示例": url_prefix + "世界幸福指标数据集示例.ipynb",
                "itemscore数据集示例": url_prefix + "itemscore数据集示例.ipynb",
                "平台使用问题汇总":"https://q8i1hdp55b.feishu.cn/docs/doccnfFMFXU13H2VJtri0KCEt6b"
            },
            "postgresql":{
                "stock": url_prefix + "stock-postgresql.ipynb",
                "titanic": url_prefix + "titanic-postgresql.ipynb",
                "超市的购物数据集示例": url_prefix + "超市的购物数据集示例.ipynb",
                "行政区划数据集示例": url_prefix + "行政区划数据集示例.ipynb",
                "世界幸福指标数据集示例": url_prefix + "世界幸福指标数据集示例.ipynb",
                "itemscore数据集示例": url_prefix + "itemscore数据集示例.ipynb",
                "平台使用问题汇总":"https://q8i1hdp55b.feishu.cn/docs/doccnfFMFXU13H2VJtri0KCEt6b"
            }
        }
        print(sqltype)
        return render(request, "practise/index.html", {
            "datasets":datasets[sqltype],
            "sqltype":sqltype
        })
