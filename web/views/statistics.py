# _ author : Administrator
# date : 2020/4/17
# -*- coding:utf-8 -*-
from web import models
from django.shortcuts import redirect, render, HttpResponse


def statistics(request, project_id):
    return render(request, 'web/statistics.html')
