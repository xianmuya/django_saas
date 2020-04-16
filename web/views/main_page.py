# _ author : Administrator
# date : 2020/4/15
# -*- coding:utf-8 -*-
from django.shortcuts import render, HttpResponse, redirect
from web import models
from django_saas import settings
from django.http import JsonResponse
def index(request):
    return render(request, 'web/index.html')
