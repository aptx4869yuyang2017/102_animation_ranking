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

movie_info = re.findall(r'<div.*?class="information di-ib mt4".*?>(.*?)<br>(.*?)<br>(.*?)</div>', my_page, re.S)

temp_type = []
temp_time = []
temp_num = []

for i in range(50):
    temp_type.append(movie_info[i][0].strip('\n').strip())
    temp_time.append(movie_info[i][1].strip('\n').strip())
    temp_num.append(movie_info[i][2].strip('\n').strip())

print temp_num
print temp_time
print temp_type
