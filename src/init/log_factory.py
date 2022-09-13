# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @File   :log_factory.py
# @Author :haohaiyo
# @Time   :2022/8/26 17:40
import logging
from flask import request, g


class ContextFilterInfo(logging.Filter):
    """
    自定义过滤器
    1.只记录info级别的日志
    2.日志格式增加trace_id
    """

    def filter(self, record):
        if record.levelno == logging.INFO:
            if request:
                record.trace_id = g.trace_id
            else:
                record.trace_id = None
            return super().filter(record)


class ContextFilterError(logging.Filter):
    def filter(self, record):
        if record.levelno == logging.ERROR:
            if request:
                record.trace_id = g.trace_id
            else:
                record.trace_id = None
            return super().filter(record)


class ContextFilterConsole(logging.Filter):
    def filter(self, record):
        if request:
            record.trace_id = g.trace_id
        else:
            record.trace_id = None
        return super().filter(record)


LOG_CONFIG_DICT = {
    'version': 1,

    'disable_existing_loggers': False,

    'formatters': {
        'base': {
            'class': 'logging.Formatter',
            'format': '%(asctime)s|%(name)s|%(trace_id)s|%(pathname)s|[%(lineno)d]|%(levelname)s|%(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
    },

    # 针对 LogRecord 的筛选器
    'filters': {
        'info_filter': {
            '()': ContextFilterInfo,
        },
        'error_filter': {
            '()': ContextFilterError,
        },
        'console_filter': {
            '()': ContextFilterConsole
        }
    },

    # 处理器(被loggers使用)
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'NOTSET',
            'formatter': 'base',
            'filters': ['console_filter', ]
        },
        'file_console': {
            'level': 'NOTSET',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': "logs/console.log",
            'when': 'D',
            'interval': 1,
            'encoding': 'UTF-8',
            'backupCount': 7,
            'formatter': 'base',
            'delay': True,
            'filters': ['console_filter', ]
        },
        'file_info': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': "logs/info.log",
            'when': 'D',
            'interval': 1,
            'encoding': 'UTF-8',
            'backupCount': 7,
            'formatter': 'base',
            'delay': True,
            'filters': ['info_filter', ]
        },
        'file_error': {
            'level': 'ERROR',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': "logs/error.log",
            'when': 'D',
            'interval': 1,
            'encoding': 'UTF-8',
            'backupCount': 7,
            'formatter': 'base',
            'delay': True,
            'filters': ['error_filter', ]
        },
        'file_db': {
            'level': 'NOTSET',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': "logs/db.log",
            'when': 'D',
            'interval': 1,
            'encoding': 'UTF-8',
            'backupCount': 7,
            'formatter': 'base',
            'delay': True,
            'filters': ['console_filter', ]
        },
    },

    # 默认的logger
    'root': {
        'level': 'INFO',
        'handlers': ['file_info', 'file_error', 'console', 'file_console']
    },

    # business层的logger
    'loggers': {
        'db_logger': {
            'handlers': ['file_db'],
            'level': 'DEBUG',
            'propagate': True
        },
        'src.api.user': {
            'handlers': ['file_db', 'file_info', 'file_error', 'console'],
            'level': 'DEBUG',
            'propagate': False
        },
    },
}
