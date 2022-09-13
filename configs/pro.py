# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @File   :pro.py
# @Author :haohaiyo
# @Time   :2022/5/8 16:57

class ProductionConfig():
    '开发模式下的配置'

    # 调试模式
    DEBUG = False

    REDIS = {
        'host': '127.0.0.1',
        'port': '6379',
        'db': 2,
        'password': '123456'
    }
