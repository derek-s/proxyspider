# !/usr/bin/python
# -*- coding:utf-8 -*-

from model import sqlite
import requests
import threading
import re
import httplib
import subprocess
import string

db = sqlite()

class proxytest(object):
    def __init__(self):
        self.headers = {
            "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",

        }
        self.allip = self.ip_pool_list()


    def ip_pool_list(self):
        # 获取IP池总表
        ipportlist = db.allip()
        return ipportlist

    def http_pool_list(self):
        # HTTP协议代理ip表
        http_pool = db.http_pool()
        return http_pool

    def connectTest(self, start_part, end_part):
        """
        连通性测试
        :return:
        """
        db_thread = sqlite()
        httpbin_url = "http://httpbin.org/ip"
        httpsbin_url = "https://httpbin.org/ip"
        headers = {
            'User_Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/5"
        }
        for proxy_one in self.allip[start_part:end_part]:
            # basic info
            id = proxy_one[0]
            ip = str(proxy_one[1])
            port = str(proxy_one[2])
            proxy = ip + ":" + port
            proxy_setting = {
                'http': proxy,
                'https': proxy
            }

            # ping test
            ping_test = "ping -c 5 -w 2 %s" % (ip)
            subp = subprocess.Popen(
                ping_test,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True
            )

            ping_result = subp.stdout.read()
            ping_regex = re.findall("100% packet loss", ping_result)
            if len(ping_regex) == 0:
                # netcat test
                nc_test = "nc -z -w 2 -nvv %s %s" % (ip, port)
                subnc = subprocess.Popen(
                    nc_test,
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    shell=True
                    )
                nc_result = string.strip(subnc.stderr.read())
                nc_success = re.findall("succeeded", nc_result)
                nc_open = re.findall("open", nc_result)
                if len(nc_success) != 0 or len(nc_open) != 0:
                    try:
                        print(str(ip) + " UP Test Web visit")
                        print(str(ip) + " Test http")
                        http_r = requests.get(httpbin_url, proxies=proxy_setting, timeout=2)
                        http_r_status = http_r.status_code
                        if http_r_status == 200:
                            remote_ip = http_r.json()['origin']
                            if remote_ip == ip:
                                print("high anonymity")
                                point = db_thread.selete_point('Proxy_HTTP', ip, port)
                                if point is None:
                                    db_thread.insert_Proxy("Proxy_HTTP", ip, port, 5)
                            else:
                                print(remote_ip)
                        else:
                            print(http_r_status)
                    except Exception as e:
                        print e
                        print(str(ip) + " http connection fail")
                    try:
                        print(str(ip) + " Test https")
                        https_r = requests.get(httpsbin_url, proxies=proxy_setting, timeout=2)
                        https_r_status = https_r.status_code
                        if https_r_status == 200:
                            remote_ip = https_r.json()['origin']
                            if remote_ip == ip:
                                print("high anonymity")
                                point = db_thread.selete_point('Proxy_HTTPS', ip, port)
                                if point is None:
                                    db_thread.insert_Proxy("Proxy_HTTPS", ip, port, 5)
                            else:
                                print(remote_ip)
                        else:
                            print(https_r_status)
                    except:
                        print(str(ip) + " https connection fail")
                else:
                    print(str(ip) + " down")
            else:
                print(str(ip) + " down")
        db_thread.closedb()