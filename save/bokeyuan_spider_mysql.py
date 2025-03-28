# -*- coding: utf-8 -*-
# @Time : 2023/9/14 17:44
# @Author : hktk
# @Email : 1994205679@qq.com
# @File : bokeyuan_spider_mysql.py
# @Project : spider

import requests
from lxml import etree
import json
import pymysql

class CnBlogSpiderDemo(object):
    def __init__(self):
        self.__url = "https://www.cnblogs.com/#p{}"
        self.__headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        }
        self.__db_con = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            password='Huawei12',
            db='big_data',
            charset='utf8'
        )
        self.__cursor = self.__db_con.cursor()

    @property
    def url(self):
        return self.__url

    @property
    def headers(self):
        return self.__headers

    @property
    def db_con(self):
        return self.__db_con

    @property
    def cursor(self):
        return self.__cursor


    def __get_data(self, url, headers, method='GET', data=''):
        '''
        向目标站点获取response
        '''
        if method == "GET":

            return requests.get(url=url, headers=headers)

        else:

            return requests.post(url=url, headers=headers, data=data)

    def get_data(self, url, headers, method='GET', data=''):

        return self.__get_data(self, url, headers, method='GET', data='')

    def __parse_data(self, data):
        """
        根据response响应的html文档的文本内容解析或者提取目标数据
        """
        dom = etree.HTML(data)
        page_res = []

        for artticle in dom.xpath('//div[@id="post_list"]/article'):
            dicts = {}

            dicts['title'] = artticle.xpath('./section[@class="post-item-body"]/div[@class="post-item-text"]/a/text()')[0]
            dicts['link'] = artticle.xpath('./section[@class="post-item-body"]/div[@class="post-item-text"]/a/@href')[0]
            # 数据预处理，先进行拼接，然后\n分开，然后在将分开的合并在次调用join方法，然后调用去除空格strip
            dicts['content'] = ''.join(''.join(artticle.xpath('./section[@class="post-item-body"]/div[@class="post-item-text"]/p[@class="post-item-summary"]/text()')).split('\n')).strip()
            # dicts['content'] = ''.join(artticle.xpath('./section[@class="post-item-body"]/div[@class="post-item-text"]/p[@class="post-item-summary"]/text()')).strip()
            dicts['txt_author'] = artticle.xpath('./section[@class="post-item-body"]/footer/a[@class="post-item-author"]/span/text()')[0]
            dicts['date'] = artticle.xpath('./section[@class="post-item-body"]/footer/span/span/text()')[0]
            dicts['favorite'] = int(artticle.xpath('./section[@class="post-item-body"]/footer/a[@class="post-meta-item btn"]/span/text()')[0])
            dicts['comment'] = int(artticle.xpath('./section[@class="post-item-body"]/footer/a[@class="post-meta-item btn"][1]/span/text()')[0])
            dicts['watch_count'] = int(artticle.xpath('./section[@class="post-item-body"]/footer/a[@class="post-meta-item btn"][2]/span/text()')[0])

            page_res.append(dicts)

        return page_res

    def parse_data(self,data):
        return self.__parse_data(data)

    def data_prossing(self,data):
        """
        将上个版本采集代码中构造的字典结构的采集数据转换为可以写像数据
        """

        save_list = []
        for page in data.values():

            for article in page:
                save_list.append(list(article.values()))
        [print(_) for _ in save_list]
        return save_list



    def sava_data(self,save_data):
        """
        面向mysql的表结构存储
        """
        sql = '''insert into cnblogs_data values (%s,%s,%s,%s,%s,%s,%s,%s,%s);'''

        for index, data in enumerate(save_data):
            self.__cursor.execute(sql, [index + 1] + data)
            print('insert one data....')
        self.__db_con.commit()
        print('持久化完毕')
        self.__cursor.close()
        self.__db_con.close()



    def display(self):

        pages = int(input('请输入您需要采集的博文的页数>>>:'))
        dicts ={}
        for index in range(1, pages + 1):
            url = self.__url.format(index)
            respomes_txt = self.__get_data(url=url, headers=self.__headers).text
            print('开始采集第{}'.format(index))
            # 继续开始数据的解析和提取
            dicts['pages{}'.format(index)] = self.__parse_data(respomes_txt)

        self.sava_data(self.data_prossing(dicts))



def test():
    CnBlogSpiderDemo().display()


if __name__ == '__main__':
    test()