# -*- coding: utf-8 -*-
# @Time: 2023/11/21 20:08
# @Author: hktk
# @Email: 1994205679@qq.com
# @File: qunaTreavl.py
# @Project: spider

import requests
from lxml import etree
import pymysql

class DongchediSpiderForComment(object):

    def __init__(self):
        self.__url = "https://www.dongchedi.com/auto/series/score/4865-x-S0-x-x-x-{}"
        self.__headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit[/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0"
        }
        self.__db_con = pymysql.connect(
            host='192.168.253.133',
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

    def __get_data(self, url, headers, method='GET', data=' '):
        if method == "GET":
            return requests.get(url=url, headers=headers)
        else:
            return requests.post(url=url, headers=headers, data=data)

    def get_data(self, url, headers, method='GET', data=''):
        return self.__get_data(url, headers, method='GET', data='')

    def __insert_data_into_database(self, data):
        try:
            insert_query = """
                INSERT INTO dongchedi (auther_id, car_time, buyCarTime, buyCarArea, buyCarPrice, youhao, avg_score,
                                            waiguang_score, neishi_score, peizhi_score, kongjian_score, shushixing_score,
                                            caokong_score, dongli_score, comment_num, favorite_num, comment_content)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            self.__cursor.executemany(insert_query, data)
            self.__db_con.commit()

        except Exception as e:
            print(f"Error inserting data into database: {e}")

    def __parse_data(self, data):
        dom = etree.HTML(data)
        for article in dom.xpath('//section[@class="tw-col-span-40 md:tw-col-span-29"]/article'):
            auther_id = article.xpath('./aside/header/div[2]/h2/a/text()')[0]
            car_time = "无" if not article.xpath('./aside/header/div[2]/h3/text()')[0] else article.xpath('./aside/header/div[2]/h3/text()')[0]
            buyCarTime = article.xpath('./aside/section/div[2]/div[1]/div[1]/p[1]/text()')[0]
            buyCarArea = article.xpath('./aside/section/div[2]/div[1]/div[2]/p[1]/text()')[0]
            buyCarPrice = article.xpath('./aside/section/div[2]/div[1]/div[3]/p[1]/text()')[0]
            youhao = article.xpath('./aside/section/div[2]/div[1]/div[4]/p[1]/text()')[0]
            avg_score = article.xpath('./aside/section/div[2]/div[2]/div[1]/p[1]/span/span[2]/text()')[0]
            waiguang_score = article.xpath('./aside/section/div[2]/div[2]/div[2]/p[1]/text()')[0]
            neishi_score = article.xpath('./aside/section/div[2]/div[2]/div[3]/p[1]/text()')[0]
            peizhi_score = article.xpath('./aside/section/div[2]/div[2]/div[4]/p[1]/text()')[0]
            kongjian_score = article.xpath('./aside/section/div/2/div[2]/div[5]/p[1]/text()')[0]
            shushixing_score = article.xpath('./aside/section/div[2]/div[2]/div[6]/p[1]/text()')[0]
            caokong_score = article.xpath('./aside/section/div[2]/div[2]/div[7]/p[1]/text()')[0]
            dongli_score = article.xpath('./aside/section/div[2]/div[2]/div[8]/p[1]/text()')[0]
            comment_num = article.xpath('./section/div[3]/div/button[1]/a/span/text()')[0]
            favorite_num = article.xpath('./section/div[3]/div/button[2]/a/span/text()')[0]
            comment_content = ''.join(article.xpath('./section/p/text()')[0].split("\n"))

            data_tuple = (auther_id, car_time, buyCarTime, buyCarArea, buyCarPrice, youhao, avg_score,
                          waiguang_score, neishi_score, peizhi_score, kongjian_score, shushixing_score,
                          caokong_score, dongli_score, comment_num, favorite_num, comment_content)

            self.__insert_data_into_database((data_tuple,))

    def parse_data(self, data):
        return self.__parse_data(data)

    def display(self):
        pages = int(input("请输入要采集页码的数量:"))

        for i in range(1, pages+1):
            url = self.url.format(pages)
            response_txt = self.get_data(url=url, headers=self.headers).text
            self.parse_data(response_txt)

        self.__cursor.close()
        self.__db_con.close()

if __name__ == '__main__':
    DongchediSpiderForComment().display()
"""
CREATE TABLE IF NOT EXISTS dongchedi (
    id INT AUTO_INCREMENT PRIMARY KEY,
    auther_id VARCHAR(255),
    car_time VARCHAR(255),
    buyCarTime VARCHAR(255),
    buyCarArea VARCHAR(255),
    buyCarPrice VARCHAR(255),
    youhao VARCHAR(255),
    avg_score VARCHAR(255),
    waiguang_score VARCHAR(255),
    neishi_score VARCHAR(255),
    peizhi_score VARCHAR(255),
    kongjian_score VARCHAR(255),
    shushixing_score VARCHAR(255),
    caokong_score VARCHAR(255),
    dongli_score VARCHAR(255),
    comment_num VARCHAR(255),
    favorite_num VARCHAR(255),
    comment_content TEXT
);


"""