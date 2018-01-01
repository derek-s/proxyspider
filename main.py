#!/usr/bin/python
# -*- coding:utf-8 -*-

import urllib2
import re
from bs4 import BeautifulSoup
import os
import sqlite3


class zdaye(object):
    def __init__(self):
        self.headers = {
            "Referer": "http://ip.zdaye.com/dayProxy.html",
            "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
        }
        self.url = "http://ip.zdaye.com/dayProxy.html"
    def zdylist(self):
        print 'process zdaye.com'
        request = urllib2.Request(self.url, headers=self.headers)
        pagescode = urllib2.urlopen(request).read()
        soup = BeautifulSoup(pagescode, "html.parser")
        proxyhtml = soup.select("div.title > a")
        for href in proxyhtml:
            zdyurl = "http://ip.zdaye.com" + href.get('href')
            self.proxyre(zdyurl)

    def proxyre(self, url):
        request = urllib2.Request(url, headers=self.headers)
        pagescode = urllib2.urlopen(request).read()
        soup = BeautifulSoup(pagescode, "html.parser")
        ipre = r"(((2[0-4]\d|25[0-5]|[01]?\d\d?)\.){3}(2[0-4]\d|25[0-5]|[01]?\d\d?):\d*)"
        result = re.findall(ipre, pagescode)
        proxydb = sqlite()
        for a in result:
            print str(a[0]).split(':')[0], str(a[0]).split(':')[1]
            proxydb.insertdb(str(a[0]).split(':')[0], str(a[0]).split(':')[1])


class sqlite(object):
    def __init__(self):
        self.db = sqlite3.connect("pool.db")
        self.c = self.db.cursor()
    
    def insertdb(self, ip, port):
        self.c.execute(
            "insert into proxy(IP,Port) values(?,?)",(ip, port)
        )
        self.db.commit()

if __name__ == "__main__":
    zdayefree = zdaye()
    zdayefree.zdylist()
