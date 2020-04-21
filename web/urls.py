# _ author : Administrator
# -*- coding:utf-8 -*-
# from django.contrib import admin
from django.conf.urls import url, include
from web.views import account, main_page, project_list
from web.views import statistics
from web.views import wiki
from web.views import file
from web.views import setting
from web.views import issues
from web.views import dashboard
from web.views import main_page

urlpatterns = [
    url(r'^register/$', account.register, name='register'),
    url(r'^login/sms/$', account.login_sms, name='login_sms'),
    url(r'^send/sms/$', account.send_sms, name='send_sms'),
    url(r'^login/$', account.login, name='login'),
    url(r'image/$', account.img, name='image'),
    url(r'index/$', main_page.index, name='index'),
    url(r'logout/$', account.logout, name='logout'),
    url(r'^price/$', main_page.price, name='price'),
    url(r'^payment/(?P<policy_id>\d+)/$', main_page.payment, name='payment'),
    url(r'^pay/$', main_page.pay, name='pay'),
    url(r'^pay/notify/$', main_page.pay_notify, name='pay_notify'),
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
        url(r'^wiki/catalog/$', wiki.wiki_catalog, name='wiki_catalog'),
        url(r'^wiki/delete/(?P<wiki_id>\d+)/$', wiki.wiki_delete, name='wiki_delete'),
        url(r'^wiki/edit/(?P<wiki_id>\d+)/$', wiki.wiki_edit, name='wiki_edit'),
        url(r'^wiki/upload/$', wiki.wiki_upload, name='wiki_upload'),

        url(r'^file/$', file.file, name='file'),
        url(r'^file/delete/$', file.file_delete, name='file_delete'),
        url(r'^cos/credential/$', file.cos_credential, name='cos_credential'),
        url(r'^file/post/$', file.file_post, name='file_post'),
        url(r'^file/download/(?P<file_id>\d+)/$', file.file_download, name='file_download'),

        url(r'^setting/$', setting.setting, name='setting'),
        url(r'^setting/delete/$', setting.delete, name='setting_delete'),

        url(r'^issues/$', issues.issues, name='issues'),
        url(r'^issues/detail/(?P<issues_id>\d+)/$', issues.issues_detail, name='issues_detail'),
        url(r'^issues/record/(?P<issues_id>\d+)/$', issues.issues_record, name='issues_record'),
        url(r'^issues/change/(?P<issues_id>\d+)/$', issues.issues_change, name='issues_change'),
        url(r'^issues/invite/url/$', issues.invite_url, name='invite_url'),

        url(r'^dashboard/$', dashboard.dashboard, name='dashboard'),
        url(r'^dashboard/issues/chart/$', dashboard.issues_chart, name='issues_chart'),
        url(r'^statistics/$', statistics.statistics, name='statistics'),
        url(r'^statistics/priority/$', statistics.statistics_priority, name='statistics_priority'),
        url(r'^statistics/project/user/$', statistics.statistics_project_user, name='statistics_project_user'),
    ], None, None)),
    url(r'^invite/join/(?P<code>\w+)/$', issues.invite_join, name='invite_join'),
]
