#!/usr/bin/env python
# -*- coding:utf-8 -*-

from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client

secret_id = 'xxxxxx'  # 替换为用户的 secretId
secret_key = 'xxxx'  # 替换为用户的 secretKey

region = 'ap-chengdu'  # 替换为用户的 Region

config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key)

client = CosS3Client(config)

response = client.upload_file(
    Bucket='xxx',
    LocalFilePath='code.png',  # 本地文件的路径
    Key='p1.png'  # 上传到桶之后的文件名
)
print(response['ETag'])
