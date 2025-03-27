
# https://piao.qunar.com/ticket/detailLight/sightCommentList.json?sightId=26805&index={}&page=3&pageSize=10&tagType=0

import requests
import json
from urllib.parse import quote

class baiDuPictureSpider(object):
    """
    异步
    """

    def __init__(self):

        self.__url='https://piao.qunar.com/ticket/detailLight/sightCommentList.json?sightId=26805&index={}&page=3&pageSize=10&tagType=0'

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

        for content in data['data']['commentList']:
            author = content['author']
            con = content['content']
            data = content['date']
            cityName = content['cityName'] if content['cityName'] else '无'
            print(author, con, data,cityName,end=',')
            print()


    def display(self):

        pages = int(input('请输入您需要抓取多少组资源>>>:'))
        for i in range(1,pages+1):
            xhr_url = self.url.format(i)
            xhr_data = self.__get_data(url=xhr_url,headers=self.__headers,response_type='json')
            # print(xhr_data)
            xhr_res = self.__parse_data(xhr_data)



def test():
    baiDuPictureSpider().display()

test()

