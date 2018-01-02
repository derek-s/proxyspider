#!/usr/bin/python
# -*- coding:utf-8 -*-

import urllib2
import re
from bs4 import BeautifulSoup
import os
import time
import sqlite3
import requests
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


# 站大爷
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
        for page in range(1, 3):
            if page == 1:
                url = self.url
            else:
                url = "http://ip.zdaye.com/dayProxy/" + str(page) + ".html"
            request = urllib2.Request(url, headers=self.headers)
            pagescode = urllib2.urlopen(request).read()
            soup = BeautifulSoup(pagescode, "html.parser")
            proxyhtml = soup.select("div.title > a")
            for href in proxyhtml:
                zdyurl = "http://ip.zdaye.com" + href.get('href')
                self.proxyre(zdyurl)
                time.sleep(2)

    def proxyre(self, url):
        request = urllib2.Request(url, headers=self.headers)
        pagescode = urllib2.urlopen(request).read()
        ipre = r"(((2[0-4]\d|25[0-5]|[01]?\d\d?)\.){3}(2[0-4]\d|25[0-5]|[01]?\d\d?):\d*)"
        result = re.findall(ipre, pagescode)
        proxydb = sqlite()
        for a in result:
            print str(a[0]).split(':')[0], str(a[0]).split(':')[1]
            proxydb.insertdb(str(a[0]).split(':')[0], str(a[0]).split(':')[1])


#全网代理IP
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
            for pagenumber in range(1, 50):
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


# 快代理
class kuaidaili(object):
    def __init__(self):
        self.headers = {
            "Referer": "https://www.kuaidaili.com/free/",
            "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
        }

    def inhaproxyre(self):
        print "process kuaidaili.com"
        proxydb = sqlite()
        for page in range(1, 50):
            url = "https://www.kuaidaili.com/free/inha/" + str(page)
            try:
                reqresult = requests.get(url, headers=self.headers, verify=False)
            except:
                pass
            pagescode = reqresult.text
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
            try:
                reqresult = requests.get(url, headers=self.headers, verify=False)
            except:
                pass
            pagescode = reqresult.text
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


# xici代理    
class xici(object):

    def __init__(self):
        self.headers = {
            "Referer": "http://www.xicidaili.com",
            "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
        }
    
    def wtproxyre(self):
        print "process xicidaili"
        proxydb = sqlite()
        for page in range(1, 50):
            url = "http://www.xicidaili.com/wt/" + str(page)
            request = urllib2.Request(url, headers=self.headers)
            pagescode = urllib2.urlopen(request).read()
            soup = BeautifulSoup(pagescode, "html.parser")
            iplist = soup.select("div#wrapper > div > table#ip_list > tr > td:nth-of-type(2)")
            portlist = soup.select("div#wrapper > div > table#ip_list > tr > td:nth-of-type(3)")
            lenlist = len(iplist)
            for num in range(0, lenlist):
                ipaddr = iplist[num].get_text()
                port = portlist[num].get_text()
                print ipaddr, port
                proxydb.insertdb(ipaddr, port)


# 66cn
class cn66(object):
    def __init__(self):
        self.headers = {
            "Referer": "http://www.66ip.cn",
            "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
        }

    def proxyre(self):
        print "process 66ip.cn"
        proxydb = sqlite()
        url = "http://www.66ip.cn/nmtq.php?getnum=800"
        request = urllib2.Request(url, headers=self.headers)
        pagescode = urllib2.urlopen(request).read()
        ipre = r"(((2[0-4]\d|25[0-5]|[01]?\d\d?)\.){3}(2[0-4]\d|25[0-5]|[01]?\d\d?):\d*)"
        result = re.findall(ipre, pagescode)
        proxydb = sqlite()
        for a in result:
            ipaddr = str(a[0]).split(':')[0]
            port = str(a[0]).split(':')[1]
            print ipaddr, port
            proxydb.insertdb(ipaddr, port)


# 89ip.cn
class ip89cn(object):
    def __init__(self):
        self.headers = {
            "Referer": "http://www.89ip.cn",
            "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
        }
        self.url = r"http://www.89ip.cn/tiqv.php?sxb=&tqsl=10000&ports=&ktip=&xl=on&submit=%CC%E1++%C8%A1"
    
    def proxyre(self):
        request = urllib2.Request(self.url, headers=self.headers)
        pagescode = urllib2.urlopen(request).read()
        ipre = r"(((2[0-4]\d|25[0-5]|[01]?\d\d?)\.){3}(2[0-4]\d|25[0-5]|[01]?\d\d?):\d*)"
        result = re.findall(ipre, pagescode)
        proxydb = sqlite()
        for a in result:
            ipaddr = str(a[0]).split(':')[0]
            port = str(a[0]).split(':')[1]
            print ipaddr, port
            proxydb.insertdb(ipaddr, port)


# 数据库
class sqlite(object):
    def __init__(self):
        self.db = sqlite3.connect("pool.db")
        self.c = self.db.cursor()
    
    def insertdb(self, ip, port):
        #OP, SOP = 0
        PCOL = ""
        self.c.execute(
            'select IP from proxy where IP = ?', (ip,)
        )
        result = self.c.fetchone()
        if result is not None:
            if result[0] == ip:
                print "IP already exist"
            else:
                self.c.execute(
                    "insert into proxy(IP,Port,OnlinePoint,HTTP,SOPoint,HTTPS) values(?,?,?,?,?,?)", (ip, port, 0, PCOL, 0, PCOL)
                )
                self.db.commit()
        else:
            self.c.execute(
                    "insert into proxy(IP,Port,OnlinePoint,HTTP,SOPoint,HTTPS) values(?,?,?,?,?,?)", (ip, port, 0, PCOL, 0, PCOL)
                )
            self.db.commit()

    def allip(self):
        self.c.execute(
            "select * from proxy"
        )
        return self.c.fetchall()

    def closedb(self):
        self.c.close()

    def uphttppoint(self, id, point):
        self.c.execute(
            "UPDATE proxy SET OnlinePoint=? where ID=?", (point, id)
        )
        self.db.commit()
    
    def uphttpspoint(self, id, point):
        self.c.execute(
            "UPDATE proxy SET SOPoint=? where ID=?", (point, id)
        )
        self.db.commit()

    def point(self, id):
        self.c.execute(
            "select OnlinePoint from proxy where ID=?", (int(id),)
        )
        return self.c.fetchone()

    def protocol(self, id, pcol):
        if pcol == "HTTP":
            self.c.execute(
                "UPDATE proxy SET HTTP=? where ID=?", (pcol, id)
            )
        elif pcol == "HTTPS":
            self.c.execute(
                "UPDATE proxy SET HTTPS=? where ID=?", (pcol, id)
            )
        self.db.commit()


class proxytest(object):
    def __init__(self):
        self.headers = {
            "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
        }
        self.urlhttps = "https://www.baidu.com/"
        self.urlhttp = "http://bj.ganji.com/"
    
    def ip_list(self):
        proxydb = sqlite()
        ipportlist = proxydb.allip()
        proxydb.closedb()
        self.test(ipportlist)
    
    def test(self, iplist):
        proxydb = sqlite()
        for info in iplist:
            ipid = info[0]
            ipaddr = info[1]
            port = info[2]
            proxyip = str(ipaddr)+":"+str(port)
            httpprox = {
                "http": proxyip
            }
            httpsprox = {
                "https": proxyip
            }
            try:
                print 'HTTP tesing: ' + proxyip
                r = requests.get(self.urlhttp, proxies=httpprox, timeout=3)
                code = r.status_code
                if code == 200:
                    print code
                    point = proxydb.point(ipid)
                    proxydb.uphttppoint(ipid, str(int(point[0])+1))
                    proxydb.protocol(ipid, "HTTP")
            except Exception as e:
                print "Not Support HTTP"
                point = proxydb.point(ipid)
                proxydb.uphttppoint(ipid, str(int(point[0])-1))
            try:
                print 'HTTPS tesing: ' + proxyip
                r = requests.get(self.urlhttps, proxies=httpsprox, timeout=3)
                code = r.status_code
                print code
                if code == 200:
                    point = proxydb.point(ipid)
                    proxydb.uphttpspoint(ipid, str(int(point[0])+1))
                    proxydb.protocol(ipid, "HTTPS")
            except Exception as e:
                print "Not Support HTTPS"
                point = proxydb.point(ipid)
                proxydb.uphttppoint(ipid, str(int(point[0])-1))

def spidermain():
    zdayefree = zdaye()
    zdayefree.zdylist()
    goubanjiafree = goubanjia()
    goubanjiafree.proxyre()
    kdaili = kuaidaili()
    kdaili.inhaproxyre()
    kdaili.intrproxyre()
    xicispider = xici()
    xicispider.wtproxyre()
    cn66spider = cn66()
    cn66spider.proxyre()
    cn89spider = ip89cn()
    cn89spider.proxyre()
    print "spider done"


def proxytestmain():
    test = proxytest()
    test.ip_list()
    


if __name__ == "__main__":
    #spidermain()
    proxytestmain()
