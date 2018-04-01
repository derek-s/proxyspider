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

    def ping_test(self, ip):
        """
        ping 测试
        :param ip:
        :return:
        """
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
            return True
        else:
            return False

    def nc_test(self, ip, port):
        """
        nc 测试
        :param ip:
        :param port:
        :return:
        """
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
            return True
        else:
            return False

    def requers_conn(self, url, local_proxy):
        result = requests.get(url, proxies=local_proxy, timeout=3)
        return result

    def ip_pool_list(self):
        # 获取IP池总表
        ipportlist = db.allip()
        return ipportlist

    def http_pool_list(self):
        # HTTP协议代理ip表
        http_pool = db.http_pool()
        return http_pool

    def https_pool_list(self):
        https_pool = db.https_pool()
        return https_pool

    def connectTest(self, start_part, end_part):
        """
        连通性测试
        :return:
        """
        db_thread = sqlite()
        httpbin_url = "http://httpbin.org/ip"
        httpsbin_url = "https://httpbin.org/ip"

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

            if self.ping_test(ip):
                if self.nc_test(ip, port):
                    try:
                        print(str(ip) + " UP Test Web visit")
                        print(str(ip) + " Test http")
                        http_result = self.requers_conn(httpbin_url, proxy_setting)
                        http_r_status = http_result.status_code
                        if http_r_status == 200:
                            remote_ip = http_result.json()['origin']
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
                        print(str(ip) + " http connection fail")
                    try:
                        print(str(ip) + " Test https")
                        https_r = self.requers_conn(httpsbin_url, proxy_setting)
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

    def availability_test(self, table, start_part, end_part):
        """
        可用性测试
        :param table: 数据表名
        :param start_part: 分片起点
        :param end_part:  分片终点
        :return: None
        """
        db_avatest = sqlite()
        httpbin_url = "http://httpbin.org/ip"
        httpsbin_url = "https://httpbin.org/ip"

        if table == "http":
            table_name = "Proxy_HTTP"
            http_ip_list = db_avatest.http_pool()
            for each_ip in http_ip_list[start_part:end_part]:
                id = str(each_ip[0])
                ip = str(each_ip[1])
                port = str(each_ip[2])
                point = int(each_ip[3])
                if point == 0:
                    db_avatest.del_proxy(table_name, id)
                proxy = ip + ":" + port
                proxy_setting = {
                    'http': proxy,
                    'https': proxy
                }
                if self.ping_test(ip):
                    if self.nc_test(ip, port):
                        try:
                            print(str(ip) + " UP Test Web visit")
                            print(str(ip) + " Test http")
                            http_result = self.requers_conn(httpbin_url, proxy_setting)
                            http_r_status = http_result.status_code
                            if http_r_status == 200:
                               print("now point %s" % str(point))
                               point += 1
                               db_avatest.update_point(table_name, id, str(point))
                            else:
                                print("now point %s" % str(point))
                                point -= 1
                                db_avatest.update_point(table_name, id, str(point))
                        except Exception as e:
                            print(str(ip) + " http connection fail")
                    else:
                        print(str(ip) + " down")
                        point -= 1
                        db_avatest.update_point(table_name, id, str(point))
                else:
                    print(str(ip) + " down")
                    point -= 1
                    db_avatest.update_point(table_name, id, str(point))

        elif table == "https":
            table_name = "Proxy_HTTPS"
            https_ip_list = db_avatest.https_pool()
            for each_ip in https_ip_list[start_part:end_part]:
                id = str(each_ip[0])
                ip = str(each_ip[1])
                port = str(each_ip[2])
                point = int(each_ip[3])
                if point == 0:
                    db_avatest.del_proxy(table_name, id)
                proxy = ip + ":" + port
                proxy_setting = {
                    'http': proxy,
                    'https': proxy
                }
                if self.ping_test(ip):
                    if self.nc_test(ip, port):
                        try:
                            print(str(ip) + " UP Test Web visit")
                            print(str(ip) + " Test https")
                            https_result = self.requers_conn(httpsbin_url, proxy_setting)
                            https_r_status = https_result.status_code
                            if https_r_status == 200:
                               print("now point %s" % str(point))
                               point += 1
                               db_avatest.update_point(table_name, id, point)
                            else:
                                print("now point %s" % str(point))
                                point -= 1
                                db_avatest.update_point(table_name, id, point)
                        except Exception as e:
                            print(str(ip) + " https connection fail")
                    else:
                        print(str(ip) + " down")
                        point -= 1
                        db_avatest.update_point(table_name, id, str(point))
                else:
                    print(str(ip) + " down")
                    point -= 1
                    db_avatest.update_point(table_name, id, str(point))
        db_avatest.closedb()