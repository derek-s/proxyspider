# !/usr/bin/python
# -*- coding:utf-8 -*-

from model import sqlite
import requests
import threading
import re
db = sqlite()

class proxytest(object):
    def __init__(self):
        self.headers = {
            "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
        }
        self.urlhttps = "https://www.baidu.com/"
        self.urlhttp = "http://www.sina.com/"
        self.allip = self.ip_pool_list()
        self.allhttp = self.http_pool_list()
        self.s = requests.session()


    def ip_pool_list(self):
        # 获取IP池总表
        ipportlist = db.allip()
        return ipportlist

    def http_pool_list(self):
        # HTTP协议代理ip表
        http_pool = db.http_pool()
        return http_pool


    def anonymity_test(self, table, iplist, start, end):
        # 匿名检测
        db = sqlite()
        for i in iplist[start:end]:
            id = i[0]
            ip = str(i[1])
            port = str(i[2])
            point = str(i[3])
            proxy_ip = ip + ":" + port
            proxy_setting = {
                'http': proxy_ip,
                'https:': proxy_ip
            }
            try:
                r = self.s.get("http://ip.chinaz.com/getip.aspx", headers=self.headers, proxies=proxy_setting, timeout=5)
                re_str = r"\d*\.\d*\.\d*\.\d*"
                visit_ip = re.findall(re_str, r.text)
                if visit_ip[0] == ip:
                    print proxy_ip + " True"
                    point = db.selete_point('Proxy_HTTP', ip, port)[0] + 1
                    print point
                    db.update_point(table, id, point)
                else:
                    db.del_proxy(table, id)
            except Exception as e:
                print proxy_ip + " Error"


    def http_test(self, start, end):
        # http协议测试
        db = sqlite()
        print "Test protocol"
        for i in self.allip[start:end]:
            ip = str(i[1])
            port = str(i[2])
            proxy = ip + ":" + port
            print threading.current_thread().getName() + " tesing: " + proxy
            proxy_setting_http = {
                "http" : str(proxy)
            }
            proxy_setting_https = {
                "https": str(proxy)
            }
            try:
                r = self.s.get(self.urlhttp, headers=self.headers, proxies=proxy_setting_http, timeout=10)
                statuscode = r.status_code
                print r.status_code
                if statuscode == 200:
                    print "True"
                    point = db.selete_point('Proxy_HTTP', ip, port)
                    print point
                    if point is None:
                        db.insert_Proxy("Proxy_HTTP", ip, port, 1)
                    else:
                        db.insert_Proxy("Proxy_HTTP", ip, port, (point + 1))
            except Exception as e:
                #print e
                print "Error"
                try:
                    r = self.s.get(self.urlhttps, headers=self.headers, proxies=proxy_setting_https, timeout=10)
                    statuscode = r.status_code
                    print r.status_code
                    if statuscode == 200:
                        print "True"
                        point = db.selete_point('Proxy_HTTPS', ip, port)
                        print point
                        if point is None:
                            db.insert_Proxy("Proxy_HTTPS", ip, port, 1)
                        else:
                            db.insert_Proxy("Proxy_HTTPS", ip, port, (point + 1))
                except Exception as e:
                    #print e
                    print "Error"
        db.closedb()
