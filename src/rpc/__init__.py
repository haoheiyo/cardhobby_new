# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @File   :__init__.py.py
# @Author :haohaiyo
# @Time   :2022/5/8 20:41

from src import jsonrpc


@jsonrpc.method('App.index')
def index():
    return u'Hello World!'


@jsonrpc.method('User.index')
def index():
    return u'User.index'
