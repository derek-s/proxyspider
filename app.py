#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2018/4/2 15:22
# @Author  : Derek.S
# @Site    : 
# @File    : app.py

from flask import Flask
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



@app.route("/")
def index():
    count = httpproxy_db.query.count()
    return render_template("index.html")

@app.route("/http")
def http_proxy():
    pass


if __name__ == '__main__':
    app.run(debug = True, port = 5500)
