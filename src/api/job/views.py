# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @File   :views.py
# @Author :haohaiyo
# @Time   :2022/9/11 23:15
import json
import logging

from flask import Blueprint, request

from src import result, ResultERR, HttpRes
from src.api.job.sc import add, remove, tasks
from src.api.job.service import get_item_info

job = Blueprint('job', __name__)
logger = logging.getLogger(__name__)


@job.route('/add_job', methods=['POST'])
def add_job():
    data = request.json or request.form
    itemid = data.get('itemid')
    price = data.get('price')
    remaining_time = data.get('remaining_time')
    item_info = get_item_info(itemid)
    end_time = item_info['endtime']
    item_name = item_info['item_name']
    img_url = item_info['img']

    logger.info('添加任务入参，itemid:%s,item_name:%s,price:%s,remaining_time:%s,end_time:%s', itemid, item_name, price,
                remaining_time, end_time)

    r = add(itemid, item_name, price, remaining_time, end_time, img_url)
    if r:
        return result(HttpRes.SUCCESS_ADD_JOB)
    else:
        return result(HttpRes.FAIL_ADD_JOB)


@job.route('/remove_job', methods=['POST'])
def remove_job():
    itemid = request.form.get('itemid')
    remove(itemid)
    return result(HttpRes.SUCCESS_REMOVE_JOB)


@job.route('/get_jobs', methods=['GET'])
def get_jobs():  # 获取
    all = request.args.get('all', None)
    data = tasks(all)
    return result(code="0", data=data)
