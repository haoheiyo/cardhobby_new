# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @File   :sc.py
# @Author :haohaiyo
# @Time   :2022/9/11 23:22
import datetime

from flask import request

from src import scheduler
from src.api.job.service import bidItemPrice


def add(itemid, item_name, price, remaining_time, end_time, img_url=None):
    user = request.cookies.get("username")
    end_time = datetime.datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
    t = datetime.timedelta(seconds=int(remaining_time))
    run_date = end_time - t
    scheduler.add_job(func=bidItemPrice, id=itemid, name=item_name, args=(itemid, price, user, img_url), trigger='date',
                      jobstore='redis', run_date=run_date, replace_existing=True)
    return True


def remove(job_id):  # 移除
    scheduler.remove_job(str(job_id))


def tasks(all=None):
    jobs = scheduler.get_jobs()
    user = request.cookies.get("username")
    l = []
    for i in jobs:
        if all:
            d = {'item_name': i.name,
                 'itemid': i.id, 'price': i.args[1], 'img_url': i.args[3],
                 'run_date': datetime.datetime.strftime(i.trigger.run_date, '%Y-%m-%d %H:%M:%S')}
            l.append(d)
        else:
            if user == i.args[2]:
                d = {'item_name': i.name,
                     'itemid': i.id, 'price': i.args[1], 'img_url': i.args[3],
                     'run_date': datetime.datetime.strftime(i.trigger.run_date, '%Y-%m-%d %H:%M:%S')}
                l.append(d)
    return l
