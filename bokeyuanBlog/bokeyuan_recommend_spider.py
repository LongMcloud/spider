#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/6/13 11:54
# @Author  : ML
# @File    : bokeyuan_recommend_spider.py
# @Software: PyCharm

import requests
from lxml import etree

class cnBlogRecommed(object):

    def __init__(self):
        self.__url= 'https://news.cnblogs.com/n/recommend?page={}'
        self.__headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        }

    @property
    def url(self):

        return self.__url

    @property
    def headers(self):

        return self.__headers

    def __get_data(self,url,headers,method='GET',data=''):
        """根据目标站点获取response响应对象"""
        if method == 'GET':

            return requests.get(url=url,headers=headers)

        else:

            return requests.post(url=url,headers=headers,data=data)

    def get_data(self,url,headers,method='GET',data=''):

        return self.__get_data(self,url,headers,method='GET',data='')

    def __parse_data(self,data):
        """根据response响应的html文档进行xpath解析"""
        dom = etree.HTML(data)

        pages_res = []

        for news in dom.xpath('//div[@id="news_list"]/div[@class="news_block"]'):
            dicts = {}

            dicts['title'] = news.xpath('./div[@class="content"]/h2[@class="news_entry"]/a/text()')[0]
            dicts['link'] = news.xpath('./div[@class="content"]/h2/a/@href')[0]
            #预处理一下
            dicts['content'] = ''.join(''.join(news.xpath('./div[@class="content"]/div[@class="entry_summary"]/text()')).split('\n')).strip()
            dicts['coment'] = news.xpath('./div[@class="content"]/div[@class="entry_footer"]/span[1]/a/text()')[0]
            dicts['watch_number'] = news.xpath('./div[@class="content"]/div[@class="entry_footer"]/span[2]/text()')[0]
            # dicts['mcn'] = news.xpath('./div[@class="content"]/div[@class="entry_footer"]/span[3]/a/text()')[0]
            # dicts['date'] = news.xpath('./div[@class="content"]/div[@class="entry_footer"]/span[4]/text()')[0]
            pages_res.append(dicts)

        return pages_res

    def parse_data(self,data):
        return self.__parse_data(data)

    def disapply(self):
        page = int(input("请输入要采集的页数>>>:"))
        #拼接url
        dicts={}
        for index in range(1,page+1):
            url = self.__url.format(index)
            response_txt = self.__get_data(url=url,headers=self.__headers).text
            print("正在采集第{}页".format(index))
            # 开始采集
            dicts["page{}".format(index)]=self.__parse_data(response_txt)
        print(dicts)


def test():
    cnBlogRecommed().disapply()

if __name__ == '__main__':
    test()