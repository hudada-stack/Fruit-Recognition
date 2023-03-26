
# encoding:utf-8
import requests

import base64
import json
# client_id 为官网获取的AK， client_secret 为官网获取的SK
host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=UxPGqSLopO89vbOwQhV3C6Eo&client_secret=GOiAePqiNuCXju2uD6cILolH7wdVVGU0'
response = requests.get(host)
if response:
    print(response.json())


# encoding:utf-8


'''
图像清晰度增强
'''

request_url = "https://aip.baidubce.com/rest/2.0/image-process/v1/image_definition_enhance"
# 二进制方式打开图片文件
f = open('C:\\Users\\hudada\\Desktop\\111.jpg', 'rb')
img = base64.b64encode(f.read())

params = {"image":img}
access_token = '24.454a5d934fa0eac87263f89fec121a96.2592000.1678608683.282335-30317815'
request_url = request_url + "?access_token=" + access_token
headers = {'content-type': 'application/x-www-form-urlencoded'}
response = requests.post(request_url, data=params, headers=headers)
if response:
    result=response.json()
    #print (result)
    #print(json.dumps(result))
    #result2=json.loads(result)
    print(result['image'])
    imginfo=result['image']

    with open('testimg.png', 'wb') as f:
        f.write(base64.b64decode(imginfo))

