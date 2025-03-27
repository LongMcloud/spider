"""
分析url

https://movie.douban.com/j/chart/top_list?type=5&interval_id=100%3A90&action=&start=0&limit=20
https://movie.douban.com/j/chart/top_list?type=5&interval_id=100%3A90&action=&start=20&limit=20
https://movie.douban.com/j/chart/top_list?type=5&interval_id=100%3A90&action=&start=40&limit=20
"""

import requests
import json


class DoubanMovieSpider(object):
    '''
    抓取豆瓣电影排行榜榜单数据信息
    '''

    def __init__(self):

        self.__url = 'https://movie.douban.com/j/chart/top_list?type={}&interval_id=100%3A90&action=&start={}&limit=20'

        self.__headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        }

        self.__moves = {
            "剧情": 11,
            "喜剧": 24,
            "动作": 5
            # 爱情
            # 科幻
            # 动画
            # 悬疑
            # 惊悚
            # 恐怖
            # 纪录片
            # 短片
            # 情色
            # 音乐
            # 歌舞
            # 家庭
            # 儿童
            # 传记
            # 历史
            # 战争
            # 犯罪
            # 西部
            # 奇幻
            # 冒险
            # 灾难
            # 武侠
            # 古装
            # 运动
            # 黑色电影
        }

    @property
    def url(self):

        return self.__url

    @property
    def headers(self):

        return self.__headers

    def get_data(self, url='', headers=None, method='GET', data=None, response_type='str'):
        '''
        通用数据请求api
        '''
        if method == 'GET' and response_type == 'str':
            return requests.get(url=url, headers=headers).text

        elif method == 'GET' and response_type == 'json':
            return json.loads(requests.get(url=url, headers=headers).text)

        elif method == 'GET' and response_type == 'content':
            return requests.get(url=url, headers=headers).content
        else:
            return requests.post(url=url, headers=headers, data=data)


    def parse_data(self,data):
        """
        解析目标数据
        """
        xhr_res = []

        for movie in data:

            dicts = {}

            dicts['name'] = movie['title']
            dicts['actors'] = ','.join(movie['actors'])
            dicts['release_date'] = movie['release_date']
            dicts['score'] = movie['score']
            dicts['types'] = '/'.join(movie['types'])
            dicts['vote_count'] = movie['vote_count']

            xhr_res.append(dicts)
        return xhr_res

    def display(self):
        # movie_types = input("请输入您需要查看排行榜的电影分类名词>>>:")
        type_nums = int(input("请输入您需要查看多少批电影排行数据>>>:"))

        dicts = {}

        for key in self.__moves.keys():

            type_res = []

            for i in range(0, 20 * type_nums + 1, 20):

                xhr_url = self.__url.format(self.__moves[key], i)

                response_josn = self.get_data(url=xhr_url, headers=self.__headers, response_type='json')
                for x in self.parse_data(response_josn):
                    type_res.append(x)
            dicts[key]=type_res

        print(dicts)

def test():
    DoubanMovieSpider().display()


if __name__ == '__main__':
    test()


'''
create table cnblogs_data(
    id int primary key auto_increment,
    title varchar(50) not null,
    link varchar(100) not null ,
    content text not null ,
    auther_name varchar(20) not null ,
    dates varchar(30) not null ,
    favorite_nums int unsigned,
    comments_num int unsigned,
    reads_num int unsigned
);
create database bigdata;
'''