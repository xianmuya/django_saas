#!/usr/bin/env python
# _ author : Administrator
# -*- coding: utf-8 -*-
import hashlib
from django_saas import settings
import uuid

def md5(string):
    '''md5加密认证'''
    hash_md5 = hashlib.md5(settings.SECRET_KEY.encode('utf-8'))
    hash_md5.update(string.encode('utf-8'))
    return hash_md5.hexdigest()


def uid(string):
    data = "{}-{}".format(str(uuid.uuid4()), string)
    return md5(data)


if __name__ == '__main__':
    print(md5('sadafaa'))
