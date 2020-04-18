# _ author : Administrator
# date : 2020/4/17
# -*- coding:utf-8 -*-
from web import models
from django.shortcuts import redirect, render, HttpResponse
from django.urls import reverse
from web.forms.wiki import WikiModelForm


def wiki(request, project_id):
    """ wiki的首页 """
    wiki_id = request.GET.get('wiki_id')
    if not wiki_id or not wiki_id.isdecimal():
        return render(request, 'web/wiki.html')

    wiki_object = models.Wiki.objects.filter(id=wiki_id, project_id=project_id).first()

    return render(request, 'web/wiki.html', {'wiki_object': wiki_object})


def wiki_add(request, project_id):
    '''添加文档'''
    if request.method == 'GET':
        form = WikiModelForm(request)
        return render(request, 'web/wiki_add.html', {'form': form})
    form = WikiModelForm(request, data=request.POST)
    if form.is_valid():
        # 判断用户是否已经选择父文章
        if form.instance.parent:
            form.instance.depth = form.instance.parent.depth + 1
        else:
            form.instance.depth = 1
        form.instance.project = request.tracer.project
        form.save()
        url = reverse('wiki', kwargs={'project_id': project_id})
        return redirect(url)
    return render(request, 'web/wiki_add.html', {'form': form.errors})
