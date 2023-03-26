from django.urls import path

from . import views

urlpatterns = [
    path('nav', views.nav, name='nav'),
    path('nav_second/<int:firstTopicID>', views.nav_second, name='nav_second'),
    path("topic/<int:thirdTopicID>",views.topic,name="topic"),
    path("submitsql/<int:pid>",views.submitsql,name="submitsql")
]
