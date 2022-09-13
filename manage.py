# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @File   :manage.py
# @Author :haohaiyo
# @Time   :2022/5/8 15:18

from flask_script import Manager
from src import app

# 使用终端管理工具
manager = Manager(app)


if __name__ == '__main__':
    manager.run()
