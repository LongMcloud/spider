#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/6/13 21:15
# @Author  : ML
# @File    : baiDuPictureSpider.py
# @Software: PyCharm

import requests
import json
from urllib.parse import quote

class baiDuPictureSpider(object):
    """
    抓取百度详情页所有照片
    """

    def __init__(self):

        self.__url='https://image.baidu.com/search/acjson?tn=resultjson_com&logid=8493349857777251088&ipn=rj&ct=201326592&is=&fp=result&fr=&word={}&queryWord={}&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=0&hd=&latest=&copyright=&s=&se=&tab=&width=&height=&face=0&istype=2&qc=&nc=1&expermode=&nojc=&isAsync=&pn={}&rn=30&gsm=1e&1686661877022='

        self.__headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        }

    @property
    def url(self):

        return self.__url

    @property
    def headers(self):

        return self.__headers

    def __get_data(self,url,headers,method='GET',data=None,response_type='str'):
        '''
        通用数据请求api
        '''
        if method == 'GET' and response_type == 'str':
            return requests.get(url=url,headers=headers).text

        elif method == 'GET' and response_type =='json':
            return json.loads(requests.get(url=url,headers=headers).text)

        elif method == 'GET' and response_type == 'content':
            return requests.get(url=url,headers=headers).content
        else:
            return requests.post(url=url,headers=headers,data=data)

    def get_data(self,url,headers,method='GET',data=None,response_type='str'):

        return self.__get_data(self,url,headers,method='GET',data=None,response_type='str')

    def __parse_data(self,data):
        xhr_res = []

        for img in data['data'][:-1]:
            img_title = img['fromPageTitleEnc']
            download_url = img['thumbURL']
            print('解析了一张图片数据....')
            xhr_res.append((img_title,download_url))

        return xhr_res

    def display(self):

        queryword = quote(input("请输入要搜索图片的关键字>>>:"))

        pages = int(input('请输入您需要抓取多少组图片资源>>>:'))
        for i in range(30,pages * 30+1,30):
            xhr_url = self.__url.format(queryword,queryword,i)
            xhr_data = self.__get_data(url=xhr_url,headers=self.__headers,response_type='json')
            print(xhr_data)
            print('以获得一组异步接口的完整图片响应.....')
            xhr_res = self.__parse_data(xhr_data)
            for imgs in xhr_res:

                self.__get_data(url=imgs[1],headers=self.__headers,response_type='content')
            with open('images/{}.jpg'.format(imgs[0]),'wb') as f:
                f.write(imgs)



def test():
    baiDuPictureSpider().display()

if __name__ == '__main__':
    test()