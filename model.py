# !/usr/bin/python
# -*- coding:utf-8 -*-

import sqlite3

class sqlite(object):
    def __init__(self):
        self.db = sqlite3.connect("db/pool.db")
        self.c = self.db.cursor()
    
    def insertdb(self, ip, port):
        """
        免费代理ip入库
        :param ip: ip地址
        :param port: port地址
        :return:
        """
        self.c.execute(
            'select IP from IP_Pool where IP = ?', (ip,)
        )
        result = self.c.fetchone()
        if result is not None:
            if result[0] == ip:
                print "IP already exist"
            else:
                self.c.execute(
                    "insert into IP_Pool(IP,Port) values(?,?)", (ip, port)
                )
                self.commit()
        else:
            self.c.execute(
                    "insert into IP_Pool(IP,Port) values(?,?)", (ip, port)
                )
            self.commit()

    def allip(self):
        """
        获取ip_pool表
        :return:
        """
        self.c.execute(
            "select * from IP_Pool"
        )
        return self.c.fetchall()

    def insert_Proxy(self, table, ip, port, point):
        """
        插入Proxy_Http Proxy_Https表
        :param table: 表
        :param ip: IP地址
        :param port: Port端口
        :param point: 评分
        :return:
        """
        self.c.execute(
            'insert into %s(IP,Port,Point) VALUES(?,?,?)' %(table), (ip, port, point)
        )
        self.commit()

    def selete_point(self, table, ip, port):
        """
        查询ip分数
        :param table: 表
        :param ip: IP地址
        :param port: Port端口
        :return: 评分
        """
        self.c.execute(
            'select Point from %s where ip = ? and port = ?' %(table), (ip, port,)
        )
        point = self.c.fetchone()
        return point

    def http_pool(self):
        """
        获取Proxy_HTTP表内容
        :return:
        """
        self.c.execute(
            "select * from Proxy_HTTP"
        )
        return self.c.fetchall()

    def https_pool(self):
        """
        获取Proxy_HTTPS表内容
        :return:
        """
        self.c.execute(
            "select * from Proxy_HTTPS"
        )
        return self.c.fetchall()

    def emtrypool(self):
        """
        清空表
        :return:
        """
        self.db.execute(
            "delete from IP_Pool"
        )
        self.db.execute(
            'update sqlite_sequence set seq = 0 where name = "IP_Pool"'
        )
        self.commit()

    def del_proxy(self, table, id):
        """
        删除代理
        :param table: 表
        :param id: proxy id
        :return:
        """
        self.db.execute(
            "delete from %s where id = ?" %(table), (id,)
        )
        self.commit()

    def update_point(self, table, id, point):
        """
        更新分数
        :param table: 表
        :param id: Proxy id
        :param point: 分数
        :return:
        """
        self.db.execute(
            "update %s set Point = ? where ID = ?" %(table), (point, id,)
        )
        self.commit()

    def commit(self):
        self.db.commit()

    def closedb(self):
        self.c.close()
