# _ author : Administrator
# date : 2020/4/14
''' 用户登录验证，注册，重置密码，注销等功能表单验证'''
from django.shortcuts import render, HttpResponse
import random
from utils.tencent.sms import send_sms_single
from django.conf import settings
from django_redis import get_redis_connection
from utils import encrypt
from web.forms.bootstrap import Bootstarp

# def send_sms(request):
#     """ 发送短信
#         ?tpl=login  -> 578869
#         ?tpl=register -> 578863
#     """
#     tpl = request.GET.get('tpl')
#     template_id = settings.TENCENT_SMS_TEMPLATE.get(tpl)
#     if not template_id:
#         return HttpResponse('模板不存在')
#
#     code = random.randrange(1000, 9999)
#     res = send_sms_single('15131289', template_id, [code, ])
#     if res['result'] == 0:
#         return HttpResponse('成功')
#     else:
#         return HttpResponse(res['errmsg'])


from django import forms
from web import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError


# 用户注册相关验证
class RegisterModelForm(Bootstarp, forms.ModelForm):
    mobile_phone = forms.CharField(label='手机号', validators=[RegexValidator(r'^(1[3|4|5|6|7|8|9])\d{9}$', '手机号格式错误'), ])
    password = forms.CharField(
        # min_length=32,
        label='密码',
        widget=forms.PasswordInput())

    confirm_password = forms.CharField(
        label='重复密码',
        widget=forms.PasswordInput())
    code = forms.CharField(
        label='验证码',
        widget=forms.TextInput())

    class Meta:
        model = models.UserInfo
        fields = ['username', 'email', 'password', 'confirm_password', 'mobile_phone', 'code']

    def clean_username(self):
        username = self.cleaned_data['username']
        exist = models.UserInfo.objects.filter(username=username).exists()
        if exist:
            raise ValidationError('用户名已存在')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        exist = models.UserInfo.objects.filter(email=email).exists()
        if exist:
            raise ValidationError('邮箱已存在')
        return email

    def clean_password(self):
        password = self.cleaned_data['password']
        return encrypt.md5(password)

    def clean_confirm_password(self):
        password = self.cleaned_data['password']
        confirm_password = encrypt.md5(self.cleaned_data['confirm_password'])
        if password != confirm_password:
            raise ValidationError('两次输入密码不一样，请重新输入')
        return confirm_password

    def clean_mobile_phone(self):
        mobile_phone = self.cleaned_data['mobile_phone']
        exists = models.UserInfo.objects.filter(mobile_phone=mobile_phone).exists()
        if exists:
            raise ValidationError('手机号已注册')
        return mobile_phone

    def clean_code(self):
        code = self.cleaned_data['code']
        mobile_phone = self.cleaned_data.get('mobile_phone')
        if not mobile_phone:
            return code
        conn = get_redis_connection()
        redis_code = conn.get(mobile_phone)
        if not redis_code:
            raise ValidationError('验证码失效或未发送，请重新发送')
        redis_str_code = redis_code.decode('utf-8')
        if code.strip() != redis_str_code:
            raise ValidationError('验证码错误，请重新输入')
        return code


# 用户发送短信相关验证
class SendSmsForm(forms.Form):
    mobile_phone = forms.CharField(label='手机号', validators=[RegexValidator(r'^(1[3|4|5|6|7|8|9])\d{9}$', '手机号格式错误'), ])

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    def clean_mobile_phone(self):
        """ 手机号校验的钩子 """
        mobile_phone = self.cleaned_data['mobile_phone']

        # 判断短信模板是否有问题
        tpl = self.request.GET.get('tpl')
        template_id = settings.TENCENT_SMS_TEMPLATE.get(tpl)
        if not template_id:
            # self.add_error('mobile_phone','短信模板错误')
            raise ValidationError('短信模板错误')

        exists = models.UserInfo.objects.filter(mobile_phone=mobile_phone).exists()
        if tpl == 'login':
            if not exists:
                raise ValidationError('手机号不存在')
        else:
            # 校验数据库中是否已有手机号
            if exists:
                raise ValidationError('手机号已存在')

        code = random.randrange(1000, 9999)

        # 发送短信
        sms = send_sms_single(mobile_phone, template_id, [code, ])
        if sms['result'] != 0:
            raise ValidationError("短信发送失败，{}".format(sms['errmsg']))

        # 验证码 写入redis（django-redis）
        conn = get_redis_connection()
        conn.set(mobile_phone, code, ex=60)

        return mobile_phone


# 用户通过短信登录验证
class LoginSms(Bootstarp, forms.Form):
    mobile_phone = forms.CharField(label='手机号', validators=[RegexValidator(r'^(1[3|4|5|6|7|8|9])\d{9}$', '手机号格式错误'), ])
    code = forms.CharField(
        label='验证码',
        widget=forms.TextInput())

    def clean_mobile_phone(self):
        mobile_phone = self.cleaned_data['mobile_phone']
        exists = models.UserInfo.objects.filter(mobile_phone=mobile_phone).exists()
        # user_object = models.UserInfo.objects.filter(mobile_phone=mobile_phone).first()
        if not exists:
            raise ValidationError('手机号不存在')

        return mobile_phone

    def clean_code(self):
        code = self.cleaned_data['code']
        mobile_phone = self.cleaned_data.get('mobile_phone')

        # 手机号不存在，则验证码无需再校验
        if not mobile_phone:
            return code

        conn = get_redis_connection()
        redis_code = conn.get(mobile_phone)  # 根据手机号去获取验证码
        if not redis_code:
            raise ValidationError('验证码失效或未发送，请重新发送')

        redis_str_code = redis_code.decode('utf-8')

        if code.strip() != redis_str_code:
            raise ValidationError('验证码错误，请重新输入')

        return code


# 用户通过账号登录验证
class Login(Bootstarp, forms.Form):
    username = forms.CharField(label='用户名或邮箱或者手机号')
    password = forms.CharField(label='密码', widget=forms.PasswordInput(render_value=True))#页面刷新仍然保留密码
    code = forms.CharField(label='验证码')

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request
    #
    # def clean_username(self):
    #     username = self.cleaned_data['username']
    #     exists = models.UserInfo.objects.filter(username=username).exists()
    #     if not exists:
    #         raise ValidationError('用户名不存在')
    #     return username

    def clean_password(self):
        #md5对输入密码加密
        password = encrypt.md5(self.cleaned_data.get('password'))
        return password

    def clean_code(self):
        code = self.cleaned_data['code']
        session_code = self.request.session.get('image_code')
        if not session_code:
            raise ValidationError('验证码已过期，请重新输入')
        if code.strip().upper() != session_code.strip().upper():
            raise ValidationError('验证码输入不正确，请重新输入')
        return code
