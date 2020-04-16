# _ author : Administrator
# date : 2020/4/14
# -*- coding:utf-8 -*-
from django.contrib import admin
from django.conf.urls import url, include
from web.views import account, main_page, project_list

urlpatterns = [
    url(r'^register/$', account.register, name='register'),
    url(r'^login/sms/$', account.login_sms, name='login_sms'),
    url(r'^send/sms/$', account.send_sms, name='send_sms'),
    url(r'^login/$', account.login, name='login'),
    url(r'image/$', account.img, name='image'),
    url(r'index/$', main_page.index, name='index'),
    url(r'logout/$', account.logout, name='logout'),
    url(r'project/list$', project_list.project, name='project_list')
]
