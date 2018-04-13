#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2018/4/3 16:09
# @Author  : Derek.S
# @Site    : 
# @File    : queue_db.py

from Queue import Queue
import threading
from model import sqlite


q = Queue()

def queue_db():
    try:
        t_Qdb = threading.Thread(target=db_process, args=())
        t_Qdb.setName("t_Qdb")
        return t_Qdb
    except Exception as e:
        print e



def db_process():
    db = sqlite()
    while_Falg = True
    while while_Falg:
        operation = q.get()
        db_info = operation[1]
        if operation[0] == "insert_Proxy":
            db.insert_Proxy(db_info['table_name'], db_info['ip'], db_info['port'], db_info['point'])
        elif operation[0] == "del_proxy":
            db.del_proxy(db_info['table_name'], db_info['id'])
        elif operation[0] == "update_point":
            db.update_point(db_info['table_name'], db_info['id'], db_info['point'])
        elif operation[0] == "update_Failed":
            db.update_Failed(db_info['table_name'], db_info['id'], db_info['failed'])
        elif operation == "over":
            while_Falg = False
    db.closedb()

