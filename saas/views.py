from django.shortcuts import render, HttpResponse, redirect

# Create your views here.
from utils.tencent import sms
def send(request):
    """基于腾讯云发送短信服务"""
    return HttpResponse('ok')
