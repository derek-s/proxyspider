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
            "select * from proxy"
        )
        return self.c.fetchall()

    def closedb(self):
        self.c.close()
