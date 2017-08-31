#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
测试模仿的爬虫之中 不太清楚的功能

Anthor: Yu_yang
Version: 0.0.1
Date: 2017-8-28
Language: Python2.7.13
Editor: Atom

"""
import string
import re
import urllib2
from lxml import etree

bgm_url = "http://bangumi.tv/anime/browser?sort=rank&page=2"

my_page = urllib2.urlopen(bgm_url).read() #.decode("utf-8")

my_tree = etree.HTML(my_page)

my_li = my_tree.xpath('//li[@class="item odd clearit"]//*|//li[@class="item even clearit"]//*')

print my_li
# for i in my_li:
    # i.xpath('span[@class="rank"]/text()')



    # print i.xpath('//li//span[@class="rank"]/text()')






# list_movie = [movie_name,movie_rank,movie_name_jp,movie_info,movie_score,movie_mum]
