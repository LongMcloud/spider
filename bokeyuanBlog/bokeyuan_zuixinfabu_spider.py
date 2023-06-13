#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/6/12 20:39
# @Author  : ML
# @File    : bokeyuan_zuixinfabu_spider.py
# @Software: PyCharm

import requests
from lxml import etree

class cnBlogNews (object):

    def __init__(self):
        self.__url = 'https://news.cnblogs.com/n/page/{}/'
        self.__headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        }

    @property
    def url(self):
        return self.__url

    @property
    def headers(self):
        return self.__headers

    def __getdata(self,url,headers,method='GET',data=''):

        if method == "GET":

            return requests.get(url=url,headers=headers)

        else:

            return requests.post(url=url,headers=headers,data=data)

    def getdata(self, url, headers, method='GET',data=''):

        return self.__getdata()

    def __parsedata(self,data):
        '''
        根据response响应的数据进行解析
        '''

        dom = etree.HTML(data)
        page_res = []

        for news in dom.xpath('//div[@id="news_list"]/div[@class="news_block"]'):
            dicts = {}

            dicts['title'] = news.xpath('./div[@class="content"]/h2/a/text()')[0]
            dicts['link'] = news.xpath('./div[@class="content"]/h2/a/@href')[0]
            #预处理一下
            dicts['content'] = ''.join(''.join(news.xpath('./div[@class="content"]/div[@class="entry_summary"]/text()')).split('\n')).strip()
            dicts['coment'] = news.xpath('./div[@class="content"]/div[@class="entry_footer"]/span[1]/a/text()')[0]
            dicts['watch_number'] = news.xpath('./div[@class="content"]/div[@class="entry_footer"]/span[2]/text()')[0]
            if news.xpath('./div[@class="content"]/div[@class="entry_footer"]/span[@class="tag"]/a[@class="gray"]/text()')[0] == ' ':
                return ' '
            else:
                dicts['mcn'] = news.xpath(
                    './div[@class="content"]/div[@class="entry_footer"]/span[@class="tag"]/a[@class="gray"]/text()')[0]
                return dicts['mcn']
            dicts['date'] = news.xpath('./div[@class="content"]/div[@class="entry_footer"]/span[@class="gray"]/text()')[0]

            page_res.append(dicts)

        return page_res

    def parsedata(self,data):

        return self.__parsedata(data)


    def display(self):
        dicts = {}
        pages = int(input("请输入要采集的博文页数:"))
        for index in range(1, pages + 1):
            url = self.__url.format(index)
            respones_txt = self.__getdata(url=url,headers=self.__headers).text
            print('当前采集的是第{}'.format(index))
            #解析和开始采集数据
            dicts['page{}'.format(index)] = self.__parsedata(respones_txt)

        print(dicts)

def test():
    cnBlogNews().display()


if __name__ == '__main__':
    test()