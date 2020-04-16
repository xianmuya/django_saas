# _ author : Administrator
# date : 2020/4/15
# -*- coding:utf-8 -*-


class Bootstarp(object):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = '请输入%s' % (field.label,)



