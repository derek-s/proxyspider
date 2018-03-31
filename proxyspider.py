# !/usr/bin/python
# -*- coding:utf-8 -*-

import urllib2
import re
from bs4 import BeautifulSoup
import os
import time
import requests
import json
from model import sqlite
import string

db = sqlite()

class request():
    def __init__(self):
        self.verify = False
        self.timeout = 10

    def r(self, url, headers):
        fails = 1
        while fails < 31:
            try:
                request = requests.get(url, headers=headers, verify=self.verify, timeout=self.timeout)
                print(request.text)
                return request.text
            except Exception as e:
                print e
                print "error retry"
                fails += 1


# 快代理
class kuaidaili():
    def __init__(self):
        self.headers = {
            "Referer": "https://www.kuaidaili.com/free/",
            "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
        }

    def inhaproxyre(self):
        print "process kuaidaili.com"
        getHtml = request()
        for page in range(1, 50):
            url = "https://www.kuaidaili.com/free/inha/" + str(page)
            pagescode = getHtml.r(url, self.headers)
            soup = BeautifulSoup(pagescode, "html.parser")
            iplist = soup.select('div#list > table > tbody > tr > td[data-title="IP"]')
            portlist = soup.select('div#list > table > tbody > tr > td[data-title="PORT"]')
            lenlist = len(iplist)
            for num in range(0, (lenlist)):
                ipaddr = iplist[num].get_text()
                port = portlist[num].get_text()
                print ipaddr, port
                db.insertdb(ipaddr, port)
            time.sleep(2)


# xici代理    
class xici():

    def __init__(self):
        self.headers = {
            "Referer": "http://www.xicidaili.com/api",
            "Host": "www.xicidaili.com",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/5"
        }
    
    def wtproxyre(self):
        print "process xicidaili"
        getHtml = request()
        print(getHtml)
        for page in range(1, 50):
            url = "http://www.xicidaili.com/nn/" + str(page)
            pagescode = getHtml.r(url, self.headers)
            soup = BeautifulSoup(pagescode, "html.parser")
            iplist = soup.select("div#wrapper > div > table#ip_list > tr > td:nth-of-type(2)")
            portlist = soup.select("div#wrapper > div > table#ip_list > tr > td:nth-of-type(3)")
            lenlist = len(iplist)
            for num in range(0, lenlist):
                ipaddr = iplist[num].get_text()
                port = portlist[num].get_text()
                print ipaddr, port
                db.insertdb(ipaddr, port)


# 66cn
class cn66():
    def __init__(self):
        self.headers = {
            "Referer": "http://www.66ip.cn",
            "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
            "Host": "www.66ip.cn"
        }

    def proxyre(self):
        print "process 66ip.cn"
        getHtml = request()
        url = "http://www.66ip.cn/nmtq.php?getnum=800"
        pagescode = getHtml.r(url, self.headers)
        ipre = r"(((2[0-4]\d|25[0-5]|[01]?\d\d?)\.){3}(2[0-4]\d|25[0-5]|[01]?\d\d?):\d*)"
        result = re.findall(ipre, pagescode)
        for info in result:
            ipaddr = str(info[0]).split(':')[0]
            port = str(info[0]).split(':')[1]
            print ipaddr, port
            db.insertdb(ipaddr, port)


# 89ip.cn
class ip89cn():
    def __init__(self):
        self.headers = {
            "Referer": "http://www.89ip.cn",
            "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
            "Host": "www.89ip.cn"
        }
        self.url = r"http://www.89ip.cn/tiqv.php?sxb=&tqsl=10000&ports=&ktip=&xl=on&submit=%CC%E1++%C8%A1"
    
    def proxyre(self):
        getHtml = request()
        pagescode = getHtml.r(self.url, self.headers)
        ipre = r"(((2[0-4]\d|25[0-5]|[01]?\d\d?)\.){3}(2[0-4]\d|25[0-5]|[01]?\d\d?):\d*)"
        result = re.findall(ipre, pagescode)
        for info in result:
            ipaddr = str(info[0]).split(':')[0]
            port = str(info[0]).split(':')[1]
            print ipaddr, port
            db.insertdb(ipaddr, port)

# ip3366
class ip3366():
    def __init__(self):
        self.headers = {
            "Referer": "http://www.ip3366.net/apidoc/",
            "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
            "Host": "www.ip3366.net"
        }

    def proxyre(self):
        getHtml = request()
        url = "http://www.ip3366.net/free/"
        pagescode = getHtml.r(url, self.headers)
        soup = BeautifulSoup(pagescode, "html.parser")
        iplist = soup.select('div#list > table > tbody > tr > td:nth-of-type(1)')
        portlist = soup.select('div#list > table > tbody > tr > td:nth-of-type(2)')
        for x in range(0, (len(iplist))):
            ipaddr = iplist[x].get_text()
            port = portlist[x].get_text()
            print ipaddr, port
            db.insertdb(ipaddr, port)

#data5u
class data5u():
    def __init__(self):
        self.headers = {
            "Referer": "http://www.data5u.com",
            "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
            "Host": "www.data5u.com"
        }
        self.url = "http://www.data5u.com/free/gngn/index.shtml"

    def proxyre(self):
        getHtml = request()
        pagescode = getHtml.r(self.url, self.headers)
        soup = BeautifulSoup(pagescode, "html.parser")
        iplist = soup.select("div.wlist > ul > li > ul.l2 > span:nth-of-type(1) > li")
        portlist = soup.select("div.wlist > ul > li > ul.l2 > span:nth-of-type(2) > li")
        for x in range(0, (len(iplist))):
            ipaddr = iplist[x].get_text()
            port = portlist[x].get_text()
            print ipaddr, port
            db.insertdb(ipaddr, port)

class coderbusy():
    def __init__(self):
        self.headers = {
            "Referer": "https://proxy.coderbusy.com/classical/anonymous-type/highanonymous.aspx",
            "User-Agent":
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
            "Host": "proxy.coderbusy.com"
        }


    def proxyre(self):
        getHtml = request()
        for i in range(1, 25):
            url = "https://proxy.coderbusy.com/classical/country/cn.aspx?page=" + str(i)
            pagescode = getHtml.r(url, self.headers)
            soup = BeautifulSoup(pagescode, "html.parser")
            iplist = soup.select("div.table-responsive > table.table > tbody > tr > td:nth-of-type(1)")
            portlist = soup.select("div.table-responsive > table.table > tbody > tr > td:nth-of-type(3)")
            for x in range(0, (len(iplist))):
                ipaddr = string.strip(iplist[x].get_text())
                port = string.strip(portlist[x].get_text())
                print ipaddr, port
                db.insertdb(ipaddr, port)

class horocn():
    def __init__(self):
        self.headers = {
            "Referer": "https://proxy.horocn.com/free-proxy.html",
            "User-Agent":
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
            "Host": "proxy.horocn.com"
        }
        self.url = "https://proxy.horocn.com/free-proxy.html?loc_name=%E4%B8%AD%E5%9B%BD"

    def proxyre(self):
        getHtml = request()
        pagescode = getHtml.r(self.url, self.headers)
        soup = BeautifulSoup(pagescode, "html.parser")
        iplist = soup.select("div.bs-docs-section > table.table > tbody > tr > th:nth-of-type(1)")
        portlist = soup.select("div.bs-docs-section > table.table > tbody > tr > th:nth-of-type(2)")
        for x in range(0, (len(iplist))):
            ipaddr = string.strip(iplist[x].get_text())
            port = string.strip(portlist[x].get_text())
            print ipaddr, port
            db.insertdb(ipaddr, port)

