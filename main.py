#!/usr/bin/python
# -*- coding:utf-8 -*-

from proxyspider import zdaye, goubanjia, kuaidaili, xici, cn66, ip89cn
from proxyspider import ip3366, data5u, ip181com, yaoyaodaili, kaixindaili, xdailicn
from proxytest import proxytest
import threading
import Queue

def spidermain():
    zdayefree = zdaye()
    zdayefree.zdylist()
    goubanjiafree = goubanjia()
    goubanjiafree.proxyre()
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
    ip181 = ip181com()
    ip181.proxyre()
    yaoyao = yaoyaodaili()
    yaoyao.proxyre()
    kxdl = kaixindaili()
    kxdl.proxyre()
    xundaili = xdailicn()
    xundaili.proxyre()
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
        last_part = part * 4 + ipaddr_length % num

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



if __name__ == "__main__":
    #spidermain()
    proxy_test()

