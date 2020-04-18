# _ author : Administrator
# date : 2020/4/17
# -*- coding:utf-8 -*-
from web import models
from django.shortcuts import redirect, render, HttpResponse


def dashboard(request, project_id):
    return render(request, 'web/dashboard.html')
