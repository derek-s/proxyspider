#!/usr/bin/python
# -*- coding:utf-8 -*-

from proxyspider import kuaidaili, xici, cn66, ip89cn
from proxyspider import ip3366, data5u, coderbusy, horocn
from proxytest import proxytest
import threading
import Queue
from optparse import OptionParser
from model import sqlite


# 增加交互命令行
parser = OptionParser()
parser.add_option("-r", "--reload", action="store_true", dest="repp", help="empty ProxyPool table reload")
parser.add_option("-s", "--spider", action="store_true", dest="sppool", help="spider ProxyPool")
parser.add_option("-t", "--test", action="store_true", dest="test", help="Test Proxy")
parser.add_option("-a", "--anonymity", action="store_true", dest="anonymity", help="Test Anonymity")
opts, args = parser.parse_args()


def spidermain():
    """
    免费代理爬虫
    :return:
    """
    kdaili = kuaidaili()
    kdaili.inhaproxyre()
    xicispider = xici()
    xicispider.wtproxyre()
    cn66spider = cn66()
    cn66spider.proxyre()
    cn89spider = ip89cn()
    cn89spider.proxyre()
    ip36ydl = ip3366()
    ip36ydl.proxyre()
    data5uc = data5u()
    data5uc.proxyre()
    coderbusydaili = coderbusy()
    coderbusydaili.proxyre()
    horocnproxy = horocn()
    horocnproxy.proxyre()

    print "spider done"


# 连通性测试代码
def ip_pool_test():
    """
    ip_pool表测试
    :return: None
    """
    proxt_test = proxytest()
    ip_pool_count = len(proxt_test.ip_pool_list()) # 获取ip_pool表内数据总量
    # 开启的县城数量
    thread_quantity = 8
    each_piece = ip_pool_count / thread_quantity
    # 计算分片后最后一片的大小
    if ip_pool_count % thread_quantity != 0:
        last_part = each_piece * thread_quantity + ip_pool_count % thread_quantity
    else:
        last_part = ip_pool_count
    print(ip_pool_count)

    # 确定分片范围
    for thread_one in range(thread_quantity):
        if thread_one == 0:
            start_part = 0
            end_part = each_piece
        elif thread_one > 0 and thread_one != thread_quantity - 1:
            start_part = each_piece * thread_one + 1
            end_part = each_piece * (thread_one + 1)
        elif thread_one == thread_quantity -1:
            start_part = each_piece * thread_one + 1
            end_part = last_part

        # 设置线程并启动
        each_thread = threading.Thread(
            target=proxt_test.connectTest, kwargs={'start_part': start_part, 'end_part': end_part}
            )
        each_thread.setDaemon(True)
        each_thread.start()

    # 主线程等待
    main_thread = threading.current_thread()
    for t in threading.enumerate():
        if t is main_thread:
            continue
        t.join()



def start_thread(num, iplist):
    """
    start thread
    :param num: thread quantity
    :return: None
    """
    testing = proxytest()
    ipaddr_length = len(iplist)
    part = ipaddr_length / num
    if ipaddr_length % num != 0:
        last_part = part * num + ipaddr_length % num
    else:
        last_part = ipaddr_length

    print len(iplist)

    for i in range(num):
        if i == 0:
            start = 0
            end = part
        elif i > 0 and i != num -1 :
            start = part * i + 1
            end = part * (i + 1)
        elif i == num - 1:
            start = part * i + 1
            end = last_part

        t = threading.Thread(target=testing.http_test, kwargs={'start':start, 'end':end})
        t.setDaemon(True)
        t.start()

    main_thread = threading.current_thread()
    for t in threading.enumerate():
        if t is main_thread:
            continue
        t.join()


def Anonymity_thread(num, iplist, table):
    """
    Anonymity Test Func
    :param num: Thread num
    :param iplist: iplist
    :return: None
    """
    testing = proxytest()
    ipaddr_length = len(iplist)
    part = ipaddr_length / num
    if ipaddr_length % num != 0:
        last_part = part * num + ipaddr_length % num
    print len(iplist)
    for i in range(num):
        if i == 0:
            start = 0
            end = part
        elif i > 0 and i != num -1 :
            start = part * i + 1
            end = part * (i + 1)
        elif i == num - 1:
            start = part * i + 1
            end = last_part

        t = threading.Thread(target=testing.anonymity_test, kwargs={'table':table, 'iplist':iplist, 'start':start, 'end':end})
        t.setDaemon(True)
        t.start()

    main_thread = threading.current_thread()
    for t in threading.enumerate():
        if t is main_thread:
            continue
        t.join()

if __name__ == "__main__":
    db = sqlite()
    if opts.repp:
        print "empty Proxy Pool table"
        db.emtrypool()
        db.commit()
        db.closedb()
        print "done"
    elif opts.sppool:
        print "spider start"
        spidermain()
    elif opts.test:
        ip_pool_test()
    elif opts.anonymity:
        if args[0] == 'http':
            Anonymity_thread(12, db.http_pool(), "Proxy_HTTP")
        elif args[0] == 'https':
            Anonymity_thread(12, db.https_pool(), "Proxy_HTTPS")
    #proxy_test()

