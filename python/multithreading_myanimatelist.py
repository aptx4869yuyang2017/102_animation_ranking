#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
myanimelist.net 多线程爬虫, 用于抓取动漫排名评分等

Anthor: Yu_yang
Version: 0.0.1
Date: 2017-8-29
Language: Python2.7.13
Editor: Atom
Operate: 具体操作请看README.md介绍
"""

import urllib2, re, string
import threading, Queue, time
import sys

reload(sys)
sys.setdefaultencoding('utf8')
_DATA = []
FILE_LOCK = threading.Lock()
SHARE_Q = Queue.Queue()  #构造一个不限制大小的的队列
_WORKER_THREAD_NUM = 6  #设置线程的个数

class MyThread(threading.Thread) :

    def __init__(self, func) :
        super(MyThread, self).__init__()  #调用父类的构造函数
        self.func = func  #传入线程函数逻辑

    def run(self) :
        self.funcasdf

def worker() :
    global SHARE_Q
    while not SHARE_Q.empty():
        url = SHARE_Q.get() #获得任务
        print "{}开始解析{}".format(threading.currentThread())
        my_page = get_page(url)
        find_title(my_page)  #获得当前页面的电影名
        #write_into_file(temp_data)
        print "{}解析结束".format(threading.currentThread())
        time.sleep(1)
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
        my_page = urllib2.urlopen(url).read().decode("utf-8")
    except urllib2.URLError, e :
        if hasattr(e, "code"):
            print "The server couldn't fulfill the request."
            print "Error code: %s" % e.code
        elif hasattr(e, "reason"):
            print "We failed to reach a server. Please check your url and read the Reason"
            print "Reason: %s" % e.reason
    return my_page

def find_title(my_page) :
    """

    通过返回的整个网页HTML, 正则匹配前100的电影名称


    Args:
        my_page: 传入页面的HTML文本用于正则匹配
    """
    temp_data = []
    movie_items = re.findall(r'<a.*?class="l".*?>(.*?)</a>', my_page, re.S)

    for item in movie_items:
        temp_data.append(item)


    # for index, item in enumerate(movie_items) :
        # if item.find("&nbsp") == -1 :
            #print item,
            # temp_data.append(item)

    _DATA.extend(temp_data)



def main() :
    global SHARE_Q
    threads = []
    bgm_url = "http://bangumi.tv/anime/browser?sort=rank&page={page}"
    #向队列中放入任务, 真正使用时, 应该设置为可持续的放入任务
    for index in xrange(48) :
        SHARE_Q.put(bgm_url.format(page = index))
    for i in xrange(_WORKER_THREAD_NUM) :
        thread = MyThread(worker)
        thread.start()  #线程开始处理任务
        threads.append(thread)
    for thread in threads :
        thread.join()
    SHARE_Q.join()


    with open("movie.txt", "w+") as my_file :
        for page in _DATA :
            for movie_name in page:
                my_file.write(movie_name + "\n")
    print "Spider Successful!!!"

if __name__ == '__main__':
    main()
