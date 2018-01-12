# !/usr/bin/python
# -*- coding:utf-8 -*-

import urllib2
import re
from bs4 import BeautifulSoup
import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class request():
    def __init__(self):
        self.verify = False
        self.timeout = 10

    def r(self, url, headers):
        fails = 1
        while fails < 31:
            try:
                request = requests.get(url, headers=headers, verify=self.verify, timeout=self.timeout)
                return request.text
            except Exception as e:
                print e
                print "error retry"
                fails += 1


# 站大爷
class zdaye():
    def __init__(self):
        self.headers = {
            "Referer": "http://ip.zdaye.com/dayProxy.html",
            "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
        }
        self.url = "http://ip.zdaye.com/dayProxy.html"
    
    def zdylist(self):
        getHtml = request()
        print 'process zdaye.com'
        for page in range(1, 3):
            if page == 1:
                url = self.url
            else:
                url = "http://ip.zdaye.com/dayProxy/" + str(page) + ".html"
            pagescode = getHtml.r(url, self.headers)
            soup = BeautifulSoup(pagescode, "html.parser")
            proxyhtml = soup.select("div.title > a")
            for href in proxyhtml:
                zdyurl = "http://ip.zdaye.com" + href.get('href')
                self.proxyre(zdyurl)
                time.sleep(2)

    def proxyre(self, url):
        getHtml = request()
        pagescode = getHtml.r(url, self.headers)
        ipre = r"(((2[0-4]\d|25[0-5]|[01]?\d\d?)\.){3}(2[0-4]\d|25[0-5]|[01]?\d\d?):\d*)"
        result = re.findall(ipre, pagescode)
        for a in result:
            print str(a[0]).split(':')[0], str(a[0]).split(':')[1]


#全网代理IP
class goubanjia():
    def __init__(self):
        self.dcap = DesiredCapabilities.PHANTOMJS.copy()
        self.dcap['phantomjs.page.customHeaders.Referer'] = 'http://www.goubanjia.com/free/index.shtml'
        self.dcap["phantomjs.page.settings.userAgent"] = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
        self.driver = webdriver.PhantomJS(
            executable_path='lib/phantomjs', 
            desired_capabilities=self.dcap)
        self.url = "http://www.goubanjia.com/free/gngn/index.shtml"
    
    def proxyre(self):
        print "process guobanjia.com"
        self.driver.get(self.url)
        try:
            WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located(By.ID, "wp-pagenavi")
            )
        except Exception as e:
            pass
        finally:
            pagesoup = BeautifulSoup(self.driver.page_source, "html.parser")
            for pagenumber in range(1, 50):
                url = "http://www.goubanjia.com/free/gngn/index" + str(pagenumber) + ".shtml"
                print url
                self.driver.get(url)
                try:
                    WebDriverWait(self.driver, 60).until(
                        EC.presence_of_element_located(By.ID, "wp-pagenavi")
                        )
                except Exception as e:
                    pass
                finally:
                    pagescode = self.driver.page_source
                    soup = BeautifulSoup(pagescode, "html.parser")
                    dellist = soup.select("div#list > table.table > tbody > tr > td.ip > p")
                    for delnode in dellist:
                        delnode.decompose()
                    iplist = soup.select("div#list > table.table > tbody > tr > td.ip")
                    for ip in iplist:
                        ipport = str(ip.get_text()).split(":")
                        if len(ipport) == 2:
                            ipaddr = ipport[0]
                            port = ipport[1]
                            print ipaddr, port
                        else:
                            pass
            self.driver.quit()


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
            time.sleep(2)


# xici代理    
class xici():

    def __init__(self):
        self.headers = {
            "Referer": "http://www.xicidaili.com",
            "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
        }
    
    def wtproxyre(self):
        print "process xicidaili"
        getHtml = request()
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


# 66cn
class cn66():
    def __init__(self):
        self.headers = {
            "Referer": "http://www.66ip.cn",
            "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
        }

    def proxyre(self):
        print "process 66ip.cn"
        getHtml = request()
        url = "http://www.66ip.cn/nmtq.php?getnum=800"
        pagescode = getHtml.r(url, self.headers)
        ipre = r"(((2[0-4]\d|25[0-5]|[01]?\d\d?)\.){3}(2[0-4]\d|25[0-5]|[01]?\d\d?):\d*)"
        result = re.findall(ipre, pagescode)
        for info in result:
            print info[0]


# 89ip.cn
class ip89cn():
    def __init__(self):
        self.headers = {
            "Referer": "http://www.89ip.cn",
            "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
        }
        self.url = r"http://www.89ip.cn/tiqv.php?sxb=&tqsl=10000&ports=&ktip=&xl=on&submit=%CC%E1++%C8%A1"
    
    def proxyre(self):
        getHtml = request()
        pagescode = getHtml.r(self.url, self.headers)
        ipre = r"(((2[0-4]\d|25[0-5]|[01]?\d\d?)\.){3}(2[0-4]\d|25[0-5]|[01]?\d\d?):\d*)"
        result = re.findall(ipre, pagescode)
        for info in result:
            print info[0]

# ip3366
class ip3366():
    def __init__(self):
        self.headers = {
            "Referer": "http://www.ip3366.com/free/",
            "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
        }
        self.url = "http://www.ip3366.net/free/?stype=1&page=1"

    def proxyre(self):
        getHtml = request()
        for pagenumber in range(1, 6):
            url = "http://www.ip3366.net/free/?stype=1&page=" + str(pagenumber)
            pagescode = getHtml.r(url, self.headers)
            soup = BeautifulSoup(pagescode, "html.parser")
            iplist = soup.select('div#list > table > tbody > tr > td:nth-of-type(1)')
            portlist = soup.select('div#list > table > tbody > tr > td:nth-of-type(2)')
            for x in range(0, (len(iplist))):
                print iplist[x].get_text(), portlist[x].get_text()

#data5u
class data5u():
    def __init__(self):
        self.headers = {
            "Referer": "http://www.data5u.com",
            "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
        }
        self.url = "http://www.data5u.com/free/gngn/index.shtml"

    def proxyre(self):
        getHtml = request()
        pagescode = getHtml.r(self.url, self.headers)
        soup = BeautifulSoup(pagescode, "html.parser")
        iplist = soup.select("div.wlist > ul > li > ul.l2 > span:nth-of-type(1) > li")
        portlist = soup.select("div.wlist > ul > li > ul.l2 > span:nth-of-type(2) > li")
        for x in range(0, (len(iplist))):
            print iplist[x].get_text(), portlist[x].get_text()

#ip181
class ip181com():
    def __init__(self):
        self.headers = {
            "Referer": "https://www.baidu.com",
            "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
        }
        self.url = "http://www.ip181.com/"

    def proxyre(self):
        getHtml = request()
        pagescode = getHtml.r(self.url, self.headers)
        soup = BeautifulSoup(pagescode, "html.parser")
        iplist = soup.select("div > table > tbody > tr > td:nth-of-type(1)")
        portlist = soup.select("div > table > tbody > tr > td:nth-of-type(2)")
        for x in range(0, len(iplist)):
            print iplist[x].get_text(), portlist[x].get_text()

#nttpsdaili
class yaoyaodaili():
    def __init__(self):
        self.headers = {
            "Referer": "http://www.httpsdaili.com",
            "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
        }
        self.url = "http://www.httpsdaili.com"

    def proxyre(self):
        getHtml = request()
        for pagenumber in range(1, 6):
            url = "http://www.httpsdaili.com/free.asp?page=" + str(pagenumber)
            pagescode = getHtml.r(url, self.headers)
            soup = BeautifulSoup(pagescode, "html.parser")
            iplist = soup.select("div#list > table > tbody > tr > td:nth-of-type(1)")
            portlist = soup.select("div#list > table > tbody > tr > td:nth-of-type(2)")
            for x in range(0, len(iplist)):
                print iplist[x].get_text(), portlist[x].get_text()


#kxdaili.com
class kaixindaili():
    def __init__(self):
        self.headers = {
            "Referer": "http://www.kxdaili.com/dailiip/1/1.html#ip",
            "User-Agent":
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
        }
        self.url = "http://www.kxdaili.com/dailiip/1/1.html#ip"

    def proxyre(self):
        getHtml = request()
        for pagenumber in range(1, 10):
            url = "http://www.kxdaili.com/dailiip/1/" + str(pagenumber) + ".html#ip"
            pagescode = getHtml.r(url, self.headers)
            soup = BeautifulSoup(pagescode, "html.parser")
            iplist = soup.select("div > table > tbody > tr > td:nth-of-type(1)")
            portlist = soup.select("div > table > tbody > tr > td:nth-of-type(2)")
            for x in range(0, len(iplist)):
                print iplist[x].get_text(), portlist[x].get_text()