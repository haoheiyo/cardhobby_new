# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @File   :__init__.py
# @Author :haohaiyo
# @Time   :2022/5/8 15:20
from configs.dev import DevelopmentConfig
from configs.pro import ProductionConfig

# 配置环境
env = 'pro'

config = {
    'dev': DevelopmentConfig,
    'pro': ProductionConfig,
}

Config = config[env]
