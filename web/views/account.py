# _ author : Administrator
# date : 2020/4/14
from django.shortcuts import render, HttpResponse, redirect
from web.forms import account
from django.http import JsonResponse
from web.forms.account import SendSmsForm
from web import models
from utils import image
from django.db.models import Q
import uuid
import datetime


def register(request):
    '''注册'''
    if request.method == 'GET':
        form = account.RegisterModelForm()
        return render(request, 'web/register.html', {'form': form})
    elif request.method == 'POST':
        # print(request.POST)
        form = account.RegisterModelForm(data=request.POST)
        if form.is_valid():
            # print(1)
            instance = form.save()
            # print(instance)
            policy_object = models.PricePolicy.objects.filter(category=1, title="个人免费版").first()
            # print(policy_object)
            models.Transaction.objects.create(
                status=2,
                order=str(uuid.uuid4()),
                user=instance,
                price_policy=policy_object,
                count=0,
                price=0,
                start_datetime=datetime.datetime.now()
            )
            return JsonResponse({'status': True, 'data': '/login/'})
        return JsonResponse({'status': False, 'error': form.errors})
        # return JsonResponse(**'ok')


def send_sms(request):
    '''发送短信'''
    form = SendSmsForm(request, data=request.GET)
    if form.is_valid():
        print(1)
        return JsonResponse({'status': True})
    return JsonResponse({'status': False, 'error': form.errors})


def login_sms(request):
    '''短信登录'''
    if request.method == 'GET':
        form = account.LoginSms()
        return render(request, 'web/login_sms.html', {'form': form})
    elif request.method == 'POST':
        form = account.LoginSms(data=request.POST)
        # print(form)
        if form.is_valid():
            mobile_phone = form.cleaned_data['mobile_phone']
            # 把用户名写入到session中
            user_object = models.UserInfo.objects.filter(mobile_phone=mobile_phone).first()
            # print(user_object)
            request.session['user_id'] = user_object.id
            request.session.set_expiry(60 * 60 * 24 * 14)

            return JsonResponse({"status": True, 'data': "/index/"})

        return JsonResponse({"status": False, 'error': form.errors})


def login(request):
    '''用户使用密码登录网站'''
    if request.method == 'GET':
        form = account.Login(request)
        return render(request, 'web/login.html', {'form': form})
    elif request.method == 'POST':
        form = account.Login(request, data=request.POST)
        # print(form)
        if form.is_valid():
            # policy_object = models.PricePolicy.objects.filter(category=1, title="个人免费版").first()
            # print(policy_object.id)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # username = request.POST.get('username')
            # print(username)
            # # print(models.UserInfo.objects.all())
            # password = request.POST.get('password')
            obj = models.UserInfo.objects.filter(Q(username=username) | Q(email=username) | Q(mobile_phone=username)). \
                filter(password=password).first()
            # print(type(obj))
            # obj = models.UserInfo.objects.filter(username=username, password=password).count()
            if obj:
                request.session['user_id'] = obj.id
                request.session.set_expiry(60 * 60 * 24 * 14)
                # print(request.session.get('user_id'))
                return redirect('/index/')
            form.add_error('username', '用户名错误')
        return render(request, 'web/login.html', {'form': form})


def img(request):
    '''生成图片验证码'''
    from io import BytesIO
    img_obj, code = image.check_code()
    request.session['image_code'] = code
    request.session.set_expiry(60)  # 主动修改session的过期时间为60s
    stream = BytesIO()
    img_obj.save(stream, 'png')
    return HttpResponse(stream.getvalue())


def logout(request):
    request.session.flush()
    return redirect('/index/')
