#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
myanimelist.net 多线程爬虫, 用于抓取动漫排名评分等

Anthor: Yu_yang
Version: 0.0.1
Date: 2017-8-29
Language: Python2.7.13
Editor: Atom

"""

import urllib2, re, string
import threading, Queue, time
import sys
import pandas as pd
from lxml import etree

from collections import OrderedDict

reload(sys)
sys.setdefaultencoding('utf8')
_DATA = []

# 作为记录数据的主要变量 _DATA_DICT ，利用了 Python 内建模块 collections 的 有序字典 OrderedDict，这样在写入 csv 的过程中就能按照排定的顺序构建 Dataframe
_DATA_DICT = OrderedDict([('rank', []), ('name', []), ('score', []),  ('mumbers',[])])


lock = threading.Lock() # 线程锁，放在了
SHARE_Q = Queue.Queue()  #构造一个不限制大小的的队列
_WORKER_THREAD_NUM = 6  #设置线程的个数

# 预先编译正则表达式，这样减少出错几率，提高检索效率
global name_cpl, rank_cpl, score_cpl, mumbers_cpl

name_cpl = re.compile(r'<a href="/subject/.*?class="l".*?>(.*?)</a>')
score_cpl = re.compile(r'<small class="fade".*?>(.*?)</small>')
mumbers_cpl = re.compile(r'<span class="tip_j">\((.*?)人评分\)</span>')

# 构建多线程的 CLass
class MyThread(threading.Thread) :

    def __init__(self, func, name) :
        super(MyThread, self).__init__()  #调用父类的构造函数
        self.func = func  #传入线程函数逻辑
        self.name = "thread{}".format(name)

    def run(self) :
        self.func()


def worker() :
    """
    这个就是每个线程执行的函数。主要调配 函数 get_page 和 find_info 协同处理网页，返回的信息写入 全局变量 SHARE_Q

    get_page : 线程锁放在了这个层级， get_page 是 IO 密集任务，并行处理的，所以没有加锁。

    find_info : 由于 find_info 是 cpu 密集任务，共同操作 全局变量 SHARE_Q 所以加了 lock。

    """
    global SHARE_Q
    while not SHARE_Q.empty():
        url = SHARE_Q.get() #获得任务

        print "{}开始解析{}".format(url, threading.currentThread().name)

        my_page = get_page(url)

        lock.acquire()

        try:
            find_info(my_page)  #获得当前页面的电影名
        finally:
            lock.release()

        SHARE_Q.task_done()



def get_page(url) :
    """

    根据所给的url爬取网页HTML

    Args:
        url: 表示当前要爬取页面的url

    Returns:
        返回抓取到整个页面的HTML(unicode编码)

    Raises:
        URLError:url引发的异常
    """
    try :
        my_page = urllib2.urlopen(url).read()  # .decode("utf-8")

    except urllib2.URLError, e :
        if hasattr(e, "code"):
            print "The server couldn't fulfill the request."
            print "Error code: %s" % e.code
        elif hasattr(e, "reason"):
            print "We failed to reach a server. Please check your url and read the Reason"
            print "Reason: %s" % e.reason

    time.sleep(1)
    return my_page


def find_info(my_page):
    """

    通过返回的整个网页HTML


    Args:
        my_page: 传入页面的HTML文本用于提取信息

    PS : 用了各种方法还是没有解决爬取时候 有的没有日文名字的问题，我也很无奈不想上 BS4 所以就这样吧。
    """
    my_tree = etree.HTML(my_page) # 日文名 排名  和 动画信息 正则搞不定  所以上了 lxml

    movie_rank = my_tree.xpath('//span[@class="rank"]/text()')

    # 下面是用的正则匹配的
    movie_name = name_cpl.findall(my_page, re.S)
    movie_score = score_cpl.findall(my_page, re.S)
    movie_mum = mumbers_cpl.findall(my_page, re.S)

    # 写入全局变量
    _DATA_DICT['name'].extend(movie_name)
    _DATA_DICT['rank'].extend(movie_rank)
    _DATA_DICT['score'].extend(movie_score)
    _DATA_DICT['mumbers'].extend(movie_mum)


def main() :
    """


    """

    global SHARE_Q
    threads = []
    bgm_url = "http://bangumi.tv/anime/browser?sort=rank&page={page}"
    #向队列中放入任务, 真正使用时, 应该设置为可持续的放入任务
    for index in xrange(1,51) :
        SHARE_Q.put(bgm_url.format(page = index))
    for i in xrange(_WORKER_THREAD_NUM) :
        thread = MyThread(worker,name=i)
        thread.start()  #线程开始处理任务
        threads.append(thread)
    for thread in threads :
        thread.join()
    SHARE_Q.join()

    print len(_DATA_DICT['name'])
    print len(_DATA_DICT['rank'])
    print len(_DATA_DICT['score'])
    #print len(_DATA_DICT['name_jp'])
    print len(_DATA_DICT['mumbers'])


    print "开始构建 dataframe"
    result_dataframe = pd.DataFrame(_DATA_DICT)
#
    print "开始写入 csv"
    result_dataframe.to_csv('../data/multithread_myanimelist.csv',index=False)

    print "Spider Successful!!!"

if __name__ == '__main__':
    main()
