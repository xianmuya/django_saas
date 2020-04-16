# _ author : Administrator
# date : 2020/4/16
# -*- coding:utf-8 -*-
'''django认证中间件'''
from django.shortcuts import render, redirect
from django.utils.deprecation import MiddlewareMixin
from web import models
from django_saas import settings
import datetime
class Tracer(object):
    '''将session中对象封装方便日后调用'''
    def __init__(self):
        self.user = None
        self.price_policy = None
        self.project = None

class AuthMiddleware(MiddlewareMixin):

    def process_request(self, request):
        '''用户登录在session中赋值'''
        request.tracer = Tracer()
        # print(1)
        user_id = request.session.get('user_id', 0)
        user_object = models.UserInfo.objects.filter(id=user_id).first()
        request.tracer.user = user_object
        # request.tracer = user_object

        # """
        # 1. 获取当用户访问的URL
        # 2. 检查URL是否在白名单中，如果再则可以继续向后访问，如果不在则进行判断是否已登录
        # """
        # user_url = request.path_info
        # white_url = settings.WHITE_REGEX_URL_LIST
        # if user_url in white_url:
        #     return
        # if not user_object:
        #     return redirect('/login/')
        # 白名单：没有登录都可以访问的URL
        """
        1. 获取当用户访问的URL
        2. 检查URL是否在白名单中，如果再则可以继续向后访问，如果不在则进行判断是否已登录
        """
        if request.path_info in settings.WHITE_REGEX_URL_LIST:
            return

        # 检查用户是否已登录，已登录继续往后走；未登录则返回登录页面。
        if not request.tracer.user:
            return redirect('/login/')

        # 登录成功之后，访问后台管理时：获取当前用户所拥有的额度

        # 方式一：免费额度在交易记录中存储

        # 获取当前用户ID值最大（最近交易记录）
        _object = models.Transaction.objects.filter(user=user_object, status=2).order_by('-id').first()
        # 判断是否已过期
        current_datetime = datetime.datetime.now()
        if _object.end_datetime and _object.end_datetime < current_datetime:
            _object = models.Transaction.objects.filter(user=user_object, status=2, price_policy__category=1).first()

        request.tracer.price_policy = _object.price_policy

        # 方式二：免费的额度存储配置文件
        """
        # 获取当前用户ID值最大（最近交易记录）
        _object = models.Transaction.objects.filter(user=user_object, status=2).order_by('-id').first()

        if not _object:
            # 没有购买
            request.price_policy = models.PricePolicy.objects.filter(category=1, title="个人免费版").first()
        else:
            # 付费版
            current_datetime = datetime.datetime.now()
            if _object.end_datetime and _object.end_datetime < current_datetime:
                request.price_policy = models.PricePolicy.objects.filter(category=1, title="个人免费版").first()
            else:
                request.price_policy = _object.price_policy
        """

