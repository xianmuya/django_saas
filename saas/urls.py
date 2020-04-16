# _ author : Administrator
# date : 2020/4/14
from django.contrib import admin
from django.conf.urls import url, include
from saas import views,tests

urlpatterns = [

    url(r'^saas/send/$', views.send), #反解url时防止多个APP重新 saas：index
    # url(r'^index/$', tests.index),

]
