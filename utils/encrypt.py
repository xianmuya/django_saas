# _ author : Administrator
# date : 2020/4/15
# -*- coding: utf-8 -*-
import hashlib
from django_saas import settings


def md5(string):
    '''md5加密认证'''
    hash_md5 = hashlib.md5(settings.SECRET_KEY.encode('utf-8'))
    hash_md5.update(string.encode('utf-8'))
    return hash_md5.hexdigest()


if __name__ == '__main__':
    print(md5('sadafaa'))
