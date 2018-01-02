#!/usr/bin/python
# -*- coding:utf-8 -*-

import urllib2
import re
from bs4 import BeautifulSoup
import os
import time
import sqlite3
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


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
        ipre = r"(((2[0-4]\d|25[0-5]|[01]?\d\d?)\.){3}(2[0-4]\d|25[0-5]|[01]?\d\d?):\d*)"
        result = re.findall(ipre, pagescode)
        proxydb = sqlite()
        for a in result:
            print str(a[0]).split(':')[0], str(a[0]).split(':')[1]
            proxydb.insertdb(str(a[0]).split(':')[0], str(a[0]).split(':')[1])


class goubanjia(object):
    def __init__(self):
        self.dcap = DesiredCapabilities.PHANTOMJS.copy()
        self.dcap['phantomjs.page.customHeaders.Referer'] = 'http://www.goubanjia.com/free/index.shtml'
        self.dcap["phantomjs.page.settings.userAgent"] = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
        self.driver = webdriver.PhantomJS(
            executable_path='lib/phantomjs', 
            desired_capabilities=self.dcap)
        self.url = "http://www.goubanjia.com/free/index.shtml"
    
    def proxyre(self):
        print "process guobanjia.com"
        proxydb = sqlite()
        self.driver.get("http://www.goubanjia.com/free/index.shtml")
        try:
            WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located(By.ID, "wp-pagenavi")
            )
        except Exception as e:
            pass
        finally:
            pagesoup = BeautifulSoup(self.driver.page_source, "html.parser")
            maxpage = pagesoup.select("div.wp-pagenavi > a:nth-of-type(9)")[0].get_text()
            for pagenumber in range(1, int(maxpage)):
                url = "http://www.goubanjia.com/free/index" + str(pagenumber) + ".shtml"
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
                            proxydb.insertdb(ipaddr, port)
                        else:
                            pass
            self.driver.quit()


class kuaidaili(object):
    def __init__(self):
        self.headers = {
            "Referer": "https://www.kuaidaili.com/free/",
            "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
        }
        self.url = "https://www.kuaidaili.com/free/"

    def inhaproxyre(self):
        print "process kuaidaili.com"
        proxydb = sqlite()
        for page in range(1, 50):
            url = "https://www.kuaidaili.com/free/inha/" + str(page)
            request = urllib2.Request(url, headers=self.headers)
            pagescode = urllib2.urlopen(request).read()
            soup = BeautifulSoup(pagescode, "html.parser")
            iplist = soup.select('div#list > table > tbody > tr > td[data-title="IP"]')
            portlist = soup.select('div#list > table > tbody > tr > td[data-title="PORT"]')
            lenlist = len(iplist)
            for num in range(0, (lenlist)):
                ipaddr = iplist[num].get_text()
                port = portlist[num].get_text()
                print ipaddr, port
                proxydb.insertdb(ipaddr, port)
            time.sleep(2)
    
    def intrproxyre(self):
        print "process kuaidaili.com"
        proxydb = sqlite()
        for page in range(1, 50):
            url = "https://www.kuaidaili.com/free/intr/" + str(page)
            request = urllib2.Request(url, headers=self.headers)
            pagescode = urllib2.urlopen(request).read()
            soup = BeautifulSoup(pagescode, "html.parser")
            iplist = soup.select('div#list > table > tbody > tr > td[data-title="IP"]')
            portlist = soup.select('div#list > table > tbody > tr > td[data-title="PORT"]')
            lenlist = len(iplist)
            for num in range(0, (lenlist)):
                ipaddr = iplist[num].get_text()
                port = portlist[num].get_text()
                print ipaddr, port
                proxydb.insertdb(ipaddr, port)
            time.sleep(2)
            


class sqlite(object):
    def __init__(self):
        self.db = sqlite3.connect("pool.db")
        self.c = self.db.cursor()
    
    def insertdb(self, ip, port):
        self.c.execute(
            "insert into proxy(IP,Port) values(?,?)", (ip, port)
        )
        self.db.commit()


if __name__ == "__main__":
    # zdayefree = zdaye()
    # zdayefree.zdylist()
    # goubanjiafree = goubanjia()
    # goubanjiafree.proxyre()
    kdaili = kuaidaili()
    kdaili.inhaproxyre()
