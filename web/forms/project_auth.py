#!/usr/bin/env python
# _ author : Administrator
# -*- coding: utf-8 -*-
from web import models
from django import forms
from web.forms.bootstrap import Bootstarp
from django.core.exceptions import ValidationError
from web.forms.widgets import ColorRadioSelect



class ProjectList(Bootstarp, forms.ModelForm):
    '''新建项目字段验证'''
    bootstrap_class_exclude = ['color']
    # desc = forms.CharField(widget=forms.Textarea, label='项目描述')
    class Meta:
        model = models.Project
        fields = ['name', 'color', 'desc']
        widgets = {
            'desc': forms.Textarea,
            'color': ColorRadioSelect(attrs={'class': 'color-radio'})# modelform下可以直接定制widgets插件，可以不用重写字段
        }

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    def clean_name(self):
        '''验证用户输入项目是否符合要求'''
        # 1获取当前用户名
        # 2验证数据库是否存在
        # 3验证当前用户可以创建项目的数量
        project_name = self.cleaned_data['name']
        user_obj = self.request.tracer.user
        exists = models.Project.objects.filter(name=project_name, creator=user_obj).exists()
        if exists:
            raise ValidationError('项目已存在请重新输入')
        project_number = models.Project.objects.filter(creator=user_obj).count()
        max_project = self.request.tracer.price_policy.project_num
        if project_number >= max_project:
            raise ValidationError('您当前套餐已不能在创建新的项目，若想继续使用该功能，请选择新的套餐')
        return project_name

    def __str__(self):
        return self.name
