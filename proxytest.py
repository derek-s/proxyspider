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
        ping连通性测试
        :return:
        """
        for proxy_one in self.allip[start_part:end_part]:
            id = proxy_one[0]
            ip = str(proxy_one[1])
            port = str(proxy_one[2])
            ping_test = "ping -c 5 -w 1 %s" % (ip)
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
                nc_test = "nc -z -w3 -nvv %s %s" % (ip, port)
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
                    print(str(ip) + " up")
                else:
                    pass
                    #print(str(ip) + "down")
            else:
                pass
                #print("down")
