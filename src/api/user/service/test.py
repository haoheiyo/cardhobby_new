# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @File   :test.py
# @Author :haohaiyo
# @Time   :2022/8/29 09:21

import logging

logger = logging.getLogger(__name__)


def func():
    logger.info("service1")
    logger.error("service2")

