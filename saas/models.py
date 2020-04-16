from django.db import models

# Create your models here.


class UserInfo(models.Model):
    username = models.CharField(max_length=32, verbose_name='用户名')
    password = models.CharField(max_length=32, verbose_name='用户密码')
    email = models.EmailField(max_length=32, verbose_name='用户邮箱')
    phone_number = models.CharField(max_length=32, verbose_name='用户手机号')