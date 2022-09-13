# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @File   :scheduler_init.py
# @Author :haohaiyo
# @Time   :2022/9/11 22:52
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.schedulers.background import BackgroundScheduler
from configs import Config


def scheduler_init():

    REDIS = Config.REDIS
    jobstores = {
        'redis': RedisJobStore(**REDIS)
    }

    executors = {
        'default': ThreadPoolExecutor(10),  # 默认线程数
        'processpool': ProcessPoolExecutor(3)  # 默认进程
    }
    return BackgroundScheduler(timezone='Asia/Shanghai', jobstores=jobstores, executors=executors)
