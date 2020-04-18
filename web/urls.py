# _ author : Administrator
# date : 2020/4/14
# -*- coding:utf-8 -*-
from django.contrib import admin
from django.conf.urls import url, include
from web.views import account, main_page, project_list
from web.views import statistics
from web.views import wiki
from web.views import file
from web.views import setting
from web.views import issues
from web.views import dashboard

urlpatterns = [
    url(r'^register/$', account.register, name='register'),
    url(r'^login/sms/$', account.login_sms, name='login_sms'),
    url(r'^send/sms/$', account.send_sms, name='send_sms'),
    url(r'^login/$', account.login, name='login'),
    url(r'image/$', account.img, name='image'),
    url(r'index/$', main_page.index, name='index'),
    url(r'logout/$', account.logout, name='logout'),
    # saas项目url映射
    url(r'project/list$', project_list.project, name='project_list'),
    # 添加星标
    url(r'^project/star/(?P<project_type>\w+)/(?P<project_id>\d+)/$', project_list.project_star, name='project_star'),
    # 取消星标
    url(r'^project/unstar/(?P<project_type>\w+)/(?P<project_id>\d+)/$', project_list.project_unstar,
        name='project_unstar'),
    # include分发第二种方法
    url(r'manage/(?P<project_id>\w+)/', include([
        url(r'^wiki/$', wiki.wiki, name='wiki'),
        url(r'^wiki/add/$', wiki.wiki_add, name='wiki_add'),
        url(r'^file/$', file.file, name='file'),
        url(r'^setting/$', setting.setting, name='setting'),
        url(r'^issues/$', issues.issues, name='issues'),
        url(r'^dashboard/$', dashboard.dashboard, name='dashboard'),
        url(r'^statistics/$', statistics.statistics, name='statistics'),
    ], None, None)),
]
