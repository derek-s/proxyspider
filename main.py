#!/usr/bin/python
# -*- coding:utf-8 -*-

from proxyspider import zdaye, goubanjia, kuaidaili, xici, cn66, ip89cn
from proxyspider import ip3366, data5u, ip181com, yaoyaodaili, kaixindaili, xdailicn


def spidermain():
    #zdayefree = zdaye()
    #zdayefree.zdylist()
    #goubanjiafree = goubanjia()
    #goubanjiafree.proxyre()
    #kdaili = kuaidaili()
    #kdaili.inhaproxyre()
    #xicispider = xici()
    #xicispider.wtproxyre()
    #cn66spider = cn66()
    #cn66spider.proxyre()
    #cn89spider = ip89cn()
    #cn89spider.proxyre()
    #ip36ydl = ip3366()
    #ip36ydl.proxyre()
    #data5uc = data5u()
    #data5uc.proxyre()
    #ip181 = ip181com()
    #ip181.proxyre()
    #yaoyao = yaoyaodaili()
    #yaoyao.proxyre()
    #kxdl = kaixindaili()
    #kxdl.proxyre()
    xundaili = xdailicn()
    xundaili.proxyre()
    print "spider done"


if __name__ == "__main__":
    spidermain()
