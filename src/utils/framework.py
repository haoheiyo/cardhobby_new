# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @File   :framework.py
# @Author :haohaiyo
# @Time   :2022/5/8 15:20

import functools
import logging
import traceback
from flask import jsonify, request, g
from src.enums.http_enum import HttpRes

logger = logging.getLogger(__name__)


def result(HttpResEnum=HttpRes.SUCCESS, code=None, message=None, data=None, tips=None):
    """
    为视图函数构造返回数据结构
    :param success: 成功标识
    :param data: 返回结构体
    :param code: code码
    :param message: 前端选择性展示
    :return:{'error': {'code': 1001, 'message': '无效的会话', 'data': {}}}
    """
    if not code:
        code = HttpResEnum.code()
    if not message:
        message = HttpResEnum.message()

    if data is None:
        data = {}
    if str(code).startswith("200"):
        success = True
    else:
        success = False
    return jsonify(
        {"code": code, "success": success, "message": message, "data": data, "tips": tips, "trace_id": g.trace_id})


def checkJSON(d, key):
    if key in d and d[key] is not None:
        return True
    for i in d.values():
        if type(i) == type({}):
            if checkJSON(i, key):
                return True
    else:
        return False


def validate_params(params=None):
    """
    必填参数校验
    :param p_args: 必传参数集合
    :return:
    """
    if params is None:
        params = []

    def decorator(view_func):
        @functools.wraps(view_func)
        def inner(*args, **kwargs):
            if request.method == 'GET':
                form_data = request.args
            else:
                if request.json:
                    form_data = request.json
                else:
                    form_data = request.form
            # logger.info("接口:%s,接口入参:%s" % (str(request.url), str(form_data)))
            if not form_data:
                return result(HttpResEnum=HttpRes.ERR_PARAMS_EMPTY)

            # if not all(k in form_data for k in params):
            if not all(checkJSON(form_data, k) for k in params):
                return result(HttpRes.ERR_PARAMS_REQUIRED, tips="必填参数：%s" % params)

            return view_func(*args, **kwargs)

        return inner

    return decorator


class ResultERR(Exception):
    """
    自定义异常类
    """

    def __init__(self, HttpRes):
        self.HttpRes = HttpRes

    def get_enum(self):
        return self.HttpRes


def auto_try(func):
    """
    自动捕获异常
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):

        try:
            return func(*args, **kwargs)
        except ResultERR as e:
            logger.info("异常：%s" % str(e.get_enum().message()))
            return result(e.get_enum())
        except Exception as e:
            logger.info("服务异常：%s" % traceback.format_exc())
            return result(HttpRes.ERR_SERVICES, tips=str(e))

    return wrapper
