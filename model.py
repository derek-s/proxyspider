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
                self.db.commit()
        else:
            self.c.execute(
                    "insert into IP_Pool(IP,Port) values(?,?)", (ip, port)
                )
            self.db.commit()

    def allip(self):
        self.c.execute(
            "select * from IP_Pool"
        )
        return self.c.fetchall()

    def insert_Proxy(self, table, ip, port, point):
        self.c.execute(
            'insert into ?(IP,Port,Point) VALUES(?,?,?)', (table, ip, port, point)
        )
        self.db.commit()

    def selete_point(self, table, ip, port):
        self.c.execute(
            'select Point from ? where ip = ? and port = ?', (table, ip, port,)
        )
    def closedb(self):
        self.c.close()
