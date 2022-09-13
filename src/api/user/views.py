# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @File   :views.py
# @Author :haohaiyo
# @Time   :2022/5/8 15:18
import logging

from flask import Blueprint

from src import result

# from src.init.log_utils import logger
from src.api.user.service.test import func

user = Blueprint('user', __name__)
logger = logging.getLogger(__name__)


@user.route('/', methods=['GET', 'POST'])
def index():
    logger.info(123)
    logger.error(456)
    logger.warning(111)
    func()
    return result(data='helloWord11')
