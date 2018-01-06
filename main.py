#!/usr/bin/python
# -*- coding:utf-8 -*-

from proxyspider import zdaye, goubanjia, kuaidaili, xici, cn66, ip89cn


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
    print "spider done"


if __name__ == "__main__":
    spidermain()
