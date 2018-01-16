# !/usr/bin/python
# -*- coding:utf-8 -*-

from model import sqlite
import requests

db = sqlite()

class proxytest(object):
    def __init__(self):
        self.headers = {
            "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
        }
        self.urlhttps = "https://www.baidu.com/"
        self.urlhttp = "http://bj.ganji.com/"
    
    def ip_pool_list(self):
        # 获取IP池总表
        ipportlist = db.allip()
        return ipportlist

    def anonymity_test(self, ip, proxy, protocol):
        # 匿名检测
        if protocol == "HTTP":
            r = requests.get("http://ip.ddemo.xyz", headers=self.headers, proxies=proxy, timeout=10)
            visit_ip = str(r.text).split(":")[0]
            if visit_ip == ip:
                return True

    def http_test(self):
        # http协议测试
        print "Test Http protocol"
        iplist = self.ip_pool_list()
        for ipinfo in iplist:
            proxy = ipinfo[1] + ":" + ipinfo[2]
            print "tesing: " + proxy
            proxy_setting = {
                "http" : str("http://" + proxy)
            }
            try:
                r = requests.get(self.urlhttp, headers=self.headers, proxies=proxy_setting, timeout=10)
                statuscode = r.status_code
                if statuscode == 200:
                    print "True"
                    if self.anonymity_test(ipinfo[1], proxy_setting, "HTTP"):
                        pass
            except Exception as e:
                print e

    def https_test(self):
        # http协议测试
        print "Test Http protocol"
        iplist = self.ip_pool_list()
        for ipinfo in iplist:
            proxy = ipinfo[1] + ":" + ipinfo[2]
            print "tesing: " + proxy
            proxy_setting = {
                "https" : str("https://" + proxy)
            }
            try:
                r = requests.get(self.urlhttp, headers=self.headers, proxies=proxy_setting, timeout=10)
                statuscode = r.status_code
                if statuscode == 200:
                    print "True"
                    if self.anonymity_test(ipinfo[1], proxy_setting, "HTTP"):
                        pass
            except Exception as e:
                print e
