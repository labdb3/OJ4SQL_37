from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('oj', views.index_judge, name='index_judge'),
]
