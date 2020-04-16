from django.test import TestCase

# Create your tests here.

from django.shortcuts import HttpResponse
from django_redis import get_redis_connection
# def index(request):
#     # 去连接池中获取一个连接
#     conn = get_redis_connection("default")
#     conn.set('nickname', "lw", ex=10)
#     value = conn.get('nickname')
#     print(value)
#     return HttpResponse("OK")
# import redis
# from django.shortcuts import HttpResponse
# # 创建redis连接池
# POOL = redis.ConnectionPool(host='127.0.0.1', port=6379, password='a7081919', encoding='utf-8', max_connections=1000)
# def index(request):
#     # 去连接池中获取一个连接
#     conn = redis.Redis(connection_pool=POOL)
#     conn.set('name', "lw", ex=10)
#     value = conn.get('name')
#     print(value)
#     return HttpResponse("ok")