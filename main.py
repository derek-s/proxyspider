#!/usr/bin/python
# -*- coding:utf-8 -*-

from proxyspider import kuaidaili, xici, cn66, ip89cn
from proxyspider import ip3366, data5u, coderbusy, horocn
from proxytest import proxytest
import threading
import Queue
from optparse import OptionParser
from model import sqlite

parser = OptionParser()
parser.add_option("-r", "--reload", action="store_true", dest="repp", help="empty ProxyPool table reload")
parser.add_option("-s", "--spider", action="store_true", dest="sppool", help="spider ProxyPool")
parser.add_option("-t", "--test", action="store_true", dest="test", help="Test Proxy")
parser.add_option("-a", "--anonymity", action="store_true", dest="anonymity", help="Test Anonymity")
opts, args = parser.parse_args()


def spidermain():
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

def proxy_test():
    test = proxytest()
    ip_list = test.ip_pool_list()
    start_thread(8, ip_list)


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
        proxy_test()
    elif opts.anonymity:
        if args[0] == 'http':
            Anonymity_thread(12, db.http_pool(), "Proxy_HTTP")
        elif args[0] == 'https':
            Anonymity_thread(12, db.https_pool(), "Proxy_HTTPS")
    #proxy_test()

