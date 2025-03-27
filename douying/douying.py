# -*- coding: utf-8 -*-
# @Time : 2023/11/26 15:26
# @Author : hktk
# @Email : 1994205679@qq.com
# @File : douying.py
# @Project : spider

import requests
import time

from lxml import etree
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from urllib import parse
# from mouse import click,move

class DouYingSpider(object):
    def __init__(self):
        self.__headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0"
        }
        # 6
        self.broswer = self.__create_driver()


    @property
    def headers(self):

        return self.__headers


    def __create_driver(self):
        """
        创建一个chrome driver驱动对象
        """
        # 2 初始化chrome浏览器驱动对象的配置参数对象
        self.chrome_option = Options()

        # 3 为driver驱动设置一些参数
        self.chrome_option.add_argument('--disable-extensions')

        # 4 当前driver驱动对象设置连接当前已经开启了调试模式的chrome浏览器
        self.chrome_option.add_experimental_option('debuggerAddress','127.0.0.1:9222')

        # 5 使用上述配置信息创建一个chrome driver驱动对象
        driver = webdriver.Chrome(executable_path='D:\pycharm\spider\driver\chromedriver.exe', chrome_options=self.chrome_option)

        return driver

    def get_search_pages(self,url):
        """
        先请求都有搜索页
        """
        # 8 传入抖音视频搜索页的具体URL，请求该页面
        self.broswer.get(url)

        return  self.broswer.page_source






    def main(self):
        # 1.分析url
        url = 'https://www.douyin.com/search/{}?publish_time=0&sort_type=0&source=switch_tab&type=video'.format(parse.quote(input("请输入您需要查询视频的关键字：")))

if __name__ == '__main__':

    DouYingSpider().main()