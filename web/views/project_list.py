# _ author : Administrator
# date : 2020/4/16
# -*- coding:utf-8 -*-
from django.shortcuts import redirect, render, HttpResponse
from web.forms import project_auth
from django.http import JsonResponse
from web import models


def project(request):
    if request.method == 'GET':
        '''get请求项目展示'''
        """
                1. 从数据库中获取两部分数据
                    我创建的所有项目：已星标、未星标
                    我参与的所有项目：已星标、未星标
                2. 提取已星标
                    列表 = 循环 [我创建的所有项目] + [我参与的所有项目] 把已星标的数据提取

                得到三个列表：星标、创建、参与
                """
        project_dict = {'star': [], 'my': [], 'join': []}

        my_project_list = models.Project.objects.filter(creator=request.tracer.user)
        for row in my_project_list:
            if row.star:
                project_dict['star'].append({"value": row, 'type': 'my'})
            else:
                project_dict['my'].append(row)

        join_project_list = models.ProjectUser.objects.filter(user=request.tracer.user)
        for item in join_project_list:
            if item.star:
                project_dict['star'].append({"value": item.project, 'type': 'join'})
            else:
                project_dict['join'].append(item.project)

        form = project_auth.ProjectList(request)
        return render(request, 'web/project_list.html', {'form': form, 'project_dict': project_dict})

        # form = project_auth.ProjectList(request)
        # return render(request, 'web/project_list.html', {'form': form})
    elif request.method == 'POST':
        '''ajax提交项目逻辑'''
        form = project_auth.ProjectList(request, data=request.POST)
        if form.is_valid():
            form.instance.creator = request.tracer.user
            form.save()
            # print(1)
            return JsonResponse({'status': True})
        return JsonResponse({'status': False, 'error': form.errors})


def project_star(request, project_type, project_id):
    """ 星标项目 """
    if project_type == 'my':
        models.Project.objects.filter(id=project_id, creator=request.tracer.user).update(star=True)
        return redirect('project_list')

    if project_type == 'join':
        models.ProjectUser.objects.filter(project_id=project_id, user=request.tracer.user).update(star=True)
        return redirect('project_list')

    return HttpResponse('请求错误')


def project_unstar(request, project_type, project_id):
    """ 取消星标 """
    if project_type == 'my':
        models.Project.objects.filter(id=project_id, creator=request.tracer.user).update(star=False)
        return redirect('project_list')

    if project_type == 'join':
        models.ProjectUser.objects.filter(project_id=project_id, user=request.tracer.user).update(star=False)
        return redirect('project_list')

    return HttpResponse('请求错误')
