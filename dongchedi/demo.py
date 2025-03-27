# -*- coding: utf-8 -*-
# @Time : 2023/11/21 20:08
# @Author : hktk
# @Email : 1994205679@qq.com
# @File : qunaTreavl.py
# @Project : spider

import requests
from lxml import etree
import pymysql
# 分析url
# https://www.dongchedi.com/auto/series/score/4865-x-S0-x-x-x-x
# https://www.dongchedi.com/auto/series/score/4865-x-S0-x-x-x-2
# https://www.dongchedi.com/auto/series/score/4865-x-S0-x-x-x-3

class DongchediSpiderForComment(object):

    # 准备工作，分析url，准备User-Agent
    def __init__(self):
        self.__url = "https://www.dongchedi.com/auto/series/score/4865-x-S0-x-x-x-{}"
        self.__headers = {
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0"
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

    # 私有属性，封装为只读,
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

    # 定义request方法获取相应response对象
    def __get_data(self, url, headers, method='GET', data=' '):
        """
        向目标站点获取response
        """
        if method == "GET":

            return requests.get(url=url,headers=headers)

        else:

            return requests.post(url=url,headers=headers,data=data)

    # 封装request方法，获取数据
    def get_data(self, url, headers, method='GET', data=''):

        return self.__get_data(url, headers, method='GET', data='')

    # 使用xpath解析相应response对象
    def __parse_data(self,data):
        """
        data:为相应的html文件，用xpath进行解析
        """
        dom = etree.HTML(data)
        # a = dom.xpath('//*[@id="__next"]/div[1]/div[2]/div[3]/section/section[1]/article')
        # print(a)
        for article in dom.xpath('//section[@class="tw-col-span-40 md:tw-col-span-29"]/article'):
            #  用户id
            auther_id = article.xpath('./aside/header/div[2]/h2/a/text()')[0]
            # 车龄时间
            car_time = "无" if not article.xpath('./aside/header/div[2]/h3/text()')[0] else article.xpath('./aside/header/div[2]/h3/text()')[0]
            # 匹配购车时间
            buyCarTime = article.xpath('./aside/section/div[2]/div[1]/div[1]/p[1]/text()')[0]
            # 购车地点
            buyCarArea = article.xpath('./aside/section/div[2]/div[1]/div[2]/p[1]/text()')[0]
            # 购车价格
            buyCarPrice = article.xpath('./aside/section/div[2]/div[1]/div[3]/p[1]/text()')[0]
            # 匹配油耗或者续航
            youhao = article.xpath('./aside/section/div[2]/div[1]/div[4]/p[1]/text()')[0]

            # 匹配综合评分
            avg_score = article.xpath('./aside/section/div[2]/div[2]/div[1]/p[1]/span/span[2]/text()')[0]
            # 外观评分
            waiguang_score = article.xpath('./aside/section/div[2]/div[2]/div[2]/p[1]/text()')[0]
            # 内饰评分
            neishi_score = article.xpath('./aside/section/div[2]/div[2]/div[3]/p[1]/text()')[0]
            # 配置评分
            peizhi_score = article.xpath('./aside/section/div[2]/div[2]/div[4]/p[1]/text()')[0]
            # 空间评分
            kongjian_score = article.xpath('./aside/section/div[2]/div[2]/div[5]/p[1]/text()')[0]
            # 舒适性评分
            shushixing_score = article.xpath('./aside/section/div[2]/div[2]/div[6]/p[1]/text()')[0]
            # 操控评分
            caokong_score = article.xpath('./aside/section/div[2]/div[2]/div[7]/p[1]/text()')[0]
            #动力评分
            dongli_score = article.xpath('./aside/section/div[2]/div[2]/div[8]/p[1]/text()')[0]
            # 匹配评论数
            comment_num = article.xpath('./section/div[3]/div/button[1]/a/span/text()')[0]
            # 匹配点赞数
            favorite_num = article.xpath('./section/div[3]/div/button[2]/a/span/text()')[0]
            # 匹配评论
            comment_content = ''.join(article.xpath('./section/p/text()')[0].split("\n"))
            # 用户评论
            print(auther_id,car_time,buyCarTime,buyCarArea,buyCarPrice,youhao,avg_score,waiguang_score,neishi_score,peizhi_score,kongjian_score,shushixing_score,caokong_score,dongli_score,comment_num,favorite_num,comment_content)


    def parse_data(self,data):

        return self.__parse_data(data)



    # 调用方法执行
    def display(self):

        pages = int(input("请输入要采集页码的数量:"))

        for i in range(1,pages+1):
            url = self.url.format(pages)
            # 获取相应对象
            response_txt = self.get_data(url=url,headers=self.headers).text
            # print(response_txt)
            # 解析数据
            self.parse_data(response_txt)


if __name__ == '__main__':
    DongchediSpiderForComment().display()