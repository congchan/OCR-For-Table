# -*- coding: utf-8 -*-
''' 调用腾讯优图的 行业文档识别-表格识别
    https://cloud.tencent.com/document/product/866/34936
'''

import base64
import glob
import sys
import json
import io
import os
import binascii
import pandas as pd

from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException 
from tencentcloud.ocr.v20181119 import ocr_client, models


def encode_image(filename):
    """ 编码图片
    :param filename: str 本地图片文件名
    :return: str 编码后的字符串
        eg, 开头部分:
        src="data:image/jpeg;base64,/9j/4AAQSkZJ......"
    """
    # 文件后缀
    ext = filename.split(".")[-1]

    with open(filename, "rb") as image_file:
        encoded_data = base64.b64encode(image_file.read()).decode()
    
    # 图片编码字符串拼接
    src = "data:image/{ext};base64,{data}".format(ext=ext, data=encoded_data)
    return src


def write_res2file(decrypted_res, destine_file):
    toread = io.BytesIO()
    toread.write(binascii.a2b_base64(decrypted_res))  # pass your `decrypted_res` string as the argument here
    toread.seek(0)  # reset the pointer
    df = pd.read_excel(toread)  # now read to dataframe
    df.to_excel(destine_file)


def run(SecretId, SecretKey, files):
    ''' 行业文档识别-表格识别, 使用本地图片转换为ImageBase64格式. '''
    try:        
        cred = credential.Credential(SecretId, SecretKey) 
        httpProfile = HttpProfile()
        httpProfile.endpoint = "ocr.tencentcloudapi.com"

        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = ocr_client.OcrClient(cred, "", clientProfile) 

        # 调用接口
        req = models.TableOCRRequest()
        for img_file in files:
            image_base64 = encode_image(img_file)
            params = '{"ImageBase64":"{}"}'.format(image_base64)
            print(params)
            req.from_json_string(params)
            resp = client.TableOCR(req)
            base64_res = resp["Response"]["Data"] # String, Base64 编码后的 Excel 数据
            destine_file = 'output/'+".".join(img_file.split(".")[0: -1])+".xlsx"
            write_res2file(base64_res, destine_file)

    except TencentCloudSDKException as err:
        print(err)


def test():
    test_data = json.load(open('test.json'))['Data']
    write_res2file(test_data, 'test.xlsx')

