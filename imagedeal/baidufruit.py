import cv2
import requests
import base64

'''
细粒度图像识别
'''
kkk2=''

def baidusearch(yourimage):
    global kkk2
    # client_id 为官网获取的AK， client_secret 为官网获取的SK
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=pumG6rAk5VPEDCIiGcMS4n5O&client_secret=z9MLGXtSeTGzcP4gPns4sd7G94fNWYUq'
    response = requests.get(host)
    if response:
       print(response.json())

    request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/classify/ingredient"
    # 二进制方式打开图片文件
    yourimage = cv2.cvtColor(yourimage, cv2.COLOR_BGR2RGB)
    cv2.imwrite("temp.png",yourimage)
    f = open('temp.png', 'rb')

    img = base64.b64encode(f.read())

    params = {"image": img}
    access_token = '24.0178c15df5b57c9c16d4bc272d7cd717.2592000.1675936875.282335-28876133'

    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    if response:
        print(response.json())

    kkk2=str(response.json())
    return kkk2
