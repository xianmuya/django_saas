# _ author : Administrator
# date : 2020/4/16
# -*- coding:utf-8 -*-
from django.shortcuts import redirect, render, HttpResponse
from web.forms import project_auth
from django.http import JsonResponse


def project(request):
    if request.method == 'GET':
        form = project_auth.ProjectList(request)
        return render(request, 'web/project_list.html', {'form': form})
    elif request.method == 'POST':
        form = project_auth.ProjectList(request, data=request.POST)
        if form.is_valid():
            form.instance.creator = request.tracer.user
            form.save()
            # print(1)
            return JsonResponse({'status': True})
        return JsonResponse({'status': False, 'error': form.errors})
