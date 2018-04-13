#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2018/4/2 15:22
# @Author  : Derek.S
# @Site    : 
# @File    : app.py

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask import render_template
import jinja2
import os

app = Flask(__name__, template_folder="template")

# path
basepath = os.path.abspath(os.path.dirname(__file__))

# db config
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(basepath, "db/pool.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy()

db.init_app(app)
#Templates dev Testing Code
app.jinja_env.auto_reload = True


class httpproxy_db(db.Model):
    __tablename__  = "Proxy_HTTP"
    ID = db.Column("ID", db.Integer, primary_key=True)
    IP = db.Column("IP", db.TEXT)
    Port = db.Column("Port", db.TEXT)
    Point = db.Column("Point", db.TEXT)

    def __init__(self, ID, IP, Port, Point):
        self.ID = ID
        self.IP = IP
        self.Port = Port
        self.Point = Point


class httpsproxy_db(db.Model):
    __tablename__  = "Proxy_HTTPS"
    ID = db.Column("ID", db.Integer, primary_key=True)
    IP = db.Column("IP", db.TEXT)
    Port = db.Column("Port", db.TEXT)
    Point = db.Column("Point", db.TEXT)

    def __init__(self, ID, IP, Port, Point):
        self.ID = ID
        self.IP = IP
        self.Port = Port
        self.Point = Point



@app.route("/")
def index():
    count_http = httpproxy_db.query.count()
    count_https = httpsproxy_db.query.count()
    return render_template("index.html", count_http=count_http, count_https=count_https)

@app.route("/http")
def http_proxy():
    count = request.args.get("count", 0, type=int)
    if count == 0:
        off_set = 20
    else:
        off_set = count
    print(count)
    http_proxy_list = httpproxy_db.query.limit(off_set).all()
    proxy_json = []
    for proxy in http_proxy_list:
        proxy_dict = {
            'ip':proxy.IP,
            'port':proxy.Port
        }
        proxy_json.append(proxy_dict)

    return jsonify(proxy_json)

@app.route("/https")
def https_proxy():
    count = request.args.get("count", 0, type=int)
    if count == 0:
        off_set = 20
    else:
        off_set = count
    print(count)
    https_proxy_list = httpsproxy_db.query.limit(off_set).all()
    proxy_json = []
    for proxy in https_proxy_list:
        proxy_dict = {
            'ip':proxy.IP,
            'port':proxy.Port
        }
        proxy_json.append(proxy_dict)

    return jsonify(proxy_json)


if __name__ == '__main__':
    app.run(debug = True, port = 5500)
