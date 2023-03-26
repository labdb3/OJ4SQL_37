from django.shortcuts import render


def index(request):
    return render(request, 'index/index.html')


def index_judge(request):
    return render(request, 'index/index_judge.html')
