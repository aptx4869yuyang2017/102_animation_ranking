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

url = "https://myanimelist.net/topanime.php"

my_page = urllib2.urlopen(url).read() #.decode("utf-8")

my_page2 = urllib2.urlopen(url).read().decode("utf-8")

movie_items1 = re.findall(r'<a.*?class="hoverinfo_trigger fl-l fs14 fw-b".*?>(.*?)</a>', my_page, re.S)   # 正则解析名字

movie_items2 = re.findall(r'<a.*?class="hoverinfo_trigger fl-l fs14 fw-b".*?>(.*?)</a>', my_page2, re.S)   # 正则解析名字




print movie_items1
print "***********"
print movie_items2


# temp_type = []
# temp_time = []
# temp_num = []
#
# for i in range(50):
    # temp_type.append(movie_info[i][0].strip('\n').strip())
    # temp_time.append(movie_info[i][1].strip('\n').strip())
    # temp_num.append(movie_info[i][2].strip('\n').strip())
#
# print temp_num
# print temp_time
