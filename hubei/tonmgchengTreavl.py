

# https://so.ly.com/scenery/newsearchlist_hot.aspx?&action=getlist&page=5&q=%E6%B9%96%E5%8C%97%E7%9C%81&pid=0&c=0&cyid=0&sort=&isnow=0&spType=&lbtypes=&IsNJL=0&classify=&grade=&dctrack=1%CB%871712286133607836%CB%871%CB%872%CB%873574322547030929%CB%870&iid=0.7181492559358951
# https://so.ly.com/scenery/newsearchlist_hot.aspx?&action=getlist&page={}&q=%E6%B9%96%E5%8C%97%E7%9C%81&pid=0&c=0&cyid=0&sort=&isnow=0&spType=&lbtypes=&IsNJL=0&classify=&grade=&dctrack=1%CB%871712286133607836%CB%871%CB%872%CB%873574322547030929%CB%870&iid=0.737373674192263

import requests
from lxml import etree
import pymysql


class WuHanSpiderForSpot(object):

    # 准备工作，分析url，准备User-Agent
    def __init__(self):
        self.__url = "https://you.ctrip.com/sightlist/wuhan145/s0-p{}.html"
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

    def __parse_data(self, data):

        dom = etree.HTML(data)
        spot_data = []

        for article in dom.xpath('//div[@class="list_wide_mod2"]/div[@class="list_mod2"]'):
            # 景点名称
            spot_name = article.xpath('./div[2]/dl/dt/a[1]/text()')[0]
            spot_adress = '无' if not ''.join(article.xpath('./div[2]/dl/dd/text()')[0].split()) else ''.join(article.xpath('./div[2]/dl/dd/text()')[0].split())
            spot_hot_score = article.xpath('./div[2]/dl/dt/a[2]/b[2]/text()')[0]
            spot_comment_score = '无' if not ''.join(article.xpath('./div[2]/ul/li[1]/a/strong/text()')[0].split()) else ''.join(article.xpath('./div[2]/ul/li[1]/a/strong/text()')[0].split())
            # qty = article.xpath('./div[2]/ul/li[3]/a')
            spot_data.append((spot_name, spot_adress, spot_hot_score, spot_comment_score))
        return spot_data

    def sava_data(self, data):
        """
        存储数据到数据库
        """
        sql = '''INSERT INTO spots (spot_name, spot_address, spot_hot_score, spot_comment_score) VALUES (%s, %s, %s, %s);'''

        try:
            for spot in data:
                print(spot)
                self.cursor.execute(sql, spot)
            self.db_con.commit()
            print("数据存储成功！")
        except Exception as e:
            print("数据存储失败:", str(e))
            self.db_con.rollback()


    # 调用方法执行
    def display(self):

        pages = int(input("请输入要采集页码的数量:"))

        for i in range(1,pages+1):
            url = self.url.format(pages)
            # 获取相应对象
            response_txt = self.get_data(url=url,headers=self.headers).text
            # print(response_txt)
            # 解析数据
            spot_data = self.__parse_data(response_txt)
            print(spot_data)

            self.sava_data(spot_data)

if __name__ == '__main__':
    WuHanSpiderForSpot().display()















