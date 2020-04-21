#!/usr/bin/env python
# _ author : Administrator
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client

secret_id = 'xxx'  # 替换为用户的 secretId
secret_key = 'xx'  # 替换为用户的 secretKey

region = 'ap-chengdu'  # 替换为用户的 Region

config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key)

client = CosS3Client(config)

response = client.create_bucket(
    Bucket='test-1301848135',
    ACL="public-read"  #  private  /  public-read / public-read-write
)