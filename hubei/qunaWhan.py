import requests
from lxml import etree
import pymysql

# 全国景点spot列表
# https://you.ctrip.com/sightlist/taipeicity360/s0-p2.html

# 武汉景点spot
# https://you.ctrip.com/sightlist/wuhan145.html
# https://you.ctrip.com/sightlist/wuhan145/s0-p2.html
# https://you.ctrip.com/sightlist/wuhan145/s0-p3.html

# https://m.ctrip.com/restapi/soa2/13444/json/getCommentCollapseList?_fxpcqlniredt=09031076312993527206&x-traceID=09031076312993527206-1712284583546-46307
# https://m.ctrip.com/restapi/soa2/13444/json/getCommentCollapseList?_fxpcqlniredt=09031076312993527206&x-traceID=09031076312993527206-1712284642717-4019647
# https://m.ctrip.com/restapi/soa2/13444/json/getCommentCollapseList?_fxpcqlniredt=09031076312993527206&x-traceID=09031076312993527206-1712284706946-5030458
# https://m.ctrip.com/restapi/soa2/13444/json/getCommentCollapseList?_fxpcqlniredt=09031076312993527206&x-traceID=09031076312993527206-1712285076889-6643578
# https://m.ctrip.com/restapi/soa2/13444/json/getCommentCollapseList?_fxpcqlniredt=09031076312993527206&x-traceID=09031076312993527206-1712285099893-3153043

class WuHanSpiderForSpot(object):

    # 准备工作，分析url，准备User-Agent
    def __init__(self):
        self.__url = "https://travel.qunar.com/p-cs300133-wuhan-jingdian-1-{}"
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

        for article in dom.xpath('//div[@class="listbox"]/ul[@class="list_item clrfix"]/li[@class="item"]'):
            # 景点名称
            spot_name = article.xpath('./div/div[1]/a')[0]

            print(spot_name)
        return spot_data

    # def sava_data(self, data):
    #     """
    #     存储数据到数据库
    #     """
    #     sql = '''INSERT INTO spots (spot_name, spot_address, spot_hot_score, spot_comment_score) VALUES (%s, %s, %s, %s);'''
    #
    #     try:
    #         for spot in data:
    #             print(spot)
    #             self.cursor.execute(sql, spot)
    #         self.db_con.commit()
    #         print("数据存储成功！")
    #     except Exception as e:
    #         print("数据存储失败:", str(e))
    #         self.db_con.rollback()


    # 调用方法执行
    def display(self):

        pages = int(input("请输入要采集页码的数量:"))

        for i in range(1,pages+1):
            url = self.url.format(i)
            print(url)
            # 获取相应对象
            response_txt = self.get_data(url=url,headers=self.headers).text
            # print(response_txt)
            # 解析数据
            spot_data = self.__parse_data(response_txt)


            # self.sava_data(spot_data)

if __name__ == '__main__':
    WuHanSpiderForSpot().display()




