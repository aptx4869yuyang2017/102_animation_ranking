#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
一个简单的 myanimelist.net 网站爬虫, 用于抓取动漫排名评分等

Anthor: Yu_yang
Version: 0.0.1
Date: 2017-8-28
Language: Python2.7.13
Editor: Atom
Operate: 具体操作请看README.md介绍
"""
import string
import re
import urllib2

import pandas as pd

class AnimationSpider(object) :
    """类的简要说明

    本类主要用于抓取 myanimelist 动漫信息

    Attributes:
        page: 用于表示当前所处的抓取页面
        cur_url: 用于表示当前争取抓取页面的url
        datas: 存储处理好的抓取到的电影名称
        _top_num: 用于记录当前的top号码
    """

    def __init__(self) :
        self.page = 1
        self.cur_url = "https://myanimelist.net/topanime.php?limit={page}"
        self.name = []
        self.rank = []
        self.type = []
        self.eps = []
        self.time = []
        self.mum = []
        self.score = []
        self._top_num = 1
        print "准备就绪, 准备爬取数据..."

    def get_page(self, cur_page) :
        """

        根据当前页码爬取网页HTML

        Args:
            cur_page: 表示当前所抓取的网站页码

        Returns:
            返回抓取到整个页面的HTML(utf-8 编码)

        Raises:
            URLError:url引发的异常
        """
        url = self.cur_url
        try :
            my_page = urllib2.urlopen(url.format(page = (cur_page - 1) * 50)).read().decode("utf-8")
        except urllib2.URLError, e :
            if hasattr(e, "code"):
                print "The server couldn't fulfill the request."
                print "Error code: %s" % e.code
            elif hasattr(e, "reason"):
                print "We failed to reach a server. Please check your url and read the Reason"
                print "Reason: %s" % e.reason
        return my_page


    def find_info(self, my_page) :
        """

        通过返回的整个网页HTML, 正则匹配动画信息


        Args:
            my_page: 传入页面的HTML文本用于正则匹配
        """

        #在Python的正则表达式中，有一个参数为re.S。它表示“.”（不包含外侧双引号，下同）的作用扩展到整个字符串，包括“\n”。

        movie_items = re.findall(r'<a.*?class="hoverinfo_trigger fl-l fs14 fw-b".*?>(.*?)</a>', my_page, re.S)   # 正则解析名字

        movie_info = re.findall(r'<div.*?class="information di-ib mt4".*?>(.*?)<br>(.*?)<br>(.*?)</div>', my_page, re.S) # 正则解析复合信息  返回的是3个元素元组构成的列表

        movie_score = re.findall(r'<span.*?class="text on".*?>(.*?)</span>', my_page, re.S) # 解析评分

        movie_rank = re.findall(r'<span.*?class="lightLink top-anime-rank-text rank.*?>(.*?)</span>', my_page, re.S) # 解析排名

        temp_name = []
        temp_mix_t_e = []
        temp_type = []
        temp_eps = []
        temp_time = []
        temp_mum = []
        temp_scroe = []
        temp_rank = []

        temp_name.extend(movie_items)

        # 将返回的 三元组列表 分成三个列表
        for i in range(50):
            temp_mix_t_e.append(movie_info[i][0].strip('\n').strip())
            temp_time.append(movie_info[i][1].strip('\n').strip())
            mum = re.findall(r'(.*?) members',movie_info[i][2].strip('\n').strip())
            temp_mum.append(mum[0]) # 用正则把 members 过滤掉

        # 将混合的 ”类型（集数）”  信息，利用正则，分成两个列表
        for i in range(50):
            item_mix = re.findall(r'(.*?)\((.*?)\)',temp_mix_t_e[i])
            temp_type.append(item_mix[0][0])
            temp_eps.append(item_mix[0][1])

        temp_scroe.extend(movie_score)
        temp_rank.extend(movie_rank)

        self.name.extend(temp_name)
        self.type.extend(temp_type)
        self.eps.extend(temp_eps)
        self.time.extend(temp_time)
        self.mum.extend(temp_mum)
        self.score.extend(temp_scroe)
        self.rank.extend(temp_rank)

        # for index, item in enumerate(movie_items) :
            # if item.find("&nbsp") == -1 :
                # temp_data.append("Top" + str(self._top_num) + " " + item)
                # self._top_num += 1
        # self.datas.extend(temp_data)

    def start_spider(self) :
        """

        爬虫入口, 并控制爬虫抓取页面的范围
        """
        while self.page <= 1 :
            my_page = self.get_page(self.page)
            print "完成一次页面爬取，页数{}".format(self.page)

            self.find_info(my_page)
            print "完成一次解析，页数{}".format(self.page)
            self.page += 1

def main() :
    print """
        ###############################
            一个简单的 myanimelist 爬虫
            Author: Yu_yang
            Version: 0.0.1
            Date: 2017-8-28
        ###############################
    """
    my_spider = AnimationSpider()
    my_spider.start_spider()

    print "爬取结束，开始构建 scv"

    item_df_dict = {"rank":my_spider.rank, "name":my_spider.name, "type":my_spider.type, "episode":my_spider.eps, "time":my_spider.time, "score":my_spider.score, 'mumbers':my_spider.mum}

    result_dataframe = pd.DataFrame(item_df_dict)

    result_dataframe.to_csv('../data/myanimelist.csv',index=False)


    print "完成csv写入"

    # for item in my_spider.rank :  # 测试各项爬取结果使用
        # print item, "*"

    print "爬取结束..."

if __name__ == '__main__':
    main()
