# !/usr/bin/python
# -*- coding:utf-8 -*-

import sqlite3

class sqlite(object):
    def __init__(self):
        self.db = sqlite3.connect("db/pool.db")
        self.c = self.db.cursor()
    
    def insertdb(self, ip, port):
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
        self.c.execute(
            "select * from IP_Pool"
        )
        return self.c.fetchall()

    def insert_Proxy(self, table, ip, port, point):
        self.c.execute(
            'insert into %s(IP,Port,Point) VALUES(?,?,?)' %(table), (ip, port, point)
        )
        self.commit()

    def selete_point(self, table, ip, port):
        self.c.execute(
            'select Point from %s where ip = ? and port = ?' %(table), (ip, port,)
        )
        point = self.c.fetchone()
        return point

    def http_pool(self):
        self.c.execute(
            "select * from Proxy_HTTP"
        )
        return self.c.fetchall()

    def https_pool(self):
        self.c.execute(
            "select * from Proxy_HTTPS"
        )
        return self.c.fetchall()

    def emtrypool(self):
        self.db.execute(
            "delete from IP_Pool"
        )
        self.db.execute(
            'update sqlite_sequence set seq = 0 where name = "IP_Pool"'
        )
        self.commit()

    def del_proxy(self, table, id):
        self.db.execute(
            "delete from %s where id = ?" %(table), (id,)
        )
        self.commit()

    def update_point(self, table, id, point):
        self.db.execute(
            "update %s set Point = ? where ID = ?" %(table), (point, id,)
        )
        self.commit()

    def commit(self):
        self.db.commit()

    def closedb(self):
        self.c.close()
