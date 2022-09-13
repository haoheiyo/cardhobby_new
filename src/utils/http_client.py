# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @File   :http_client.py
# @Author :haohaiyo
# @Time   :2022/6/7 13:24

import requests
import json as complexjson

from src import logger


class HttpClient(object):

    def __init__(self, api_root_url=None):
        self.api_root_url = api_root_url
        self.session = requests.session()

    def get(self, url, **kwargs):
        return self.request(url, "GET", **kwargs)

    def post(self, url, data=None, json=None, **kwargs):
        return self.request(url, "POST", data, json, **kwargs)

    def put(self, url, data=None, **kwargs):
        return self.request(url, "PUT", data, **kwargs)

    def delete(self, url, **kwargs):
        return self.request(url, "DELETE", **kwargs)

    def patch(self, url, data=None, **kwargs):
        return self.request(url, "PATCH", data, **kwargs)

    def request(self, url, method, data=None, json=None, **kwargs):
        url = self.api_root_url + url if self.api_root_url else url
        self.__request_log(url, method, data, json, **kwargs)
        if method == "GET":
            return Res(self.session.get(url, **kwargs))
        if method == "POST":
            return Res(self.session.post(url, data, json, **kwargs))
        if method == "PUT":
            if json:
                # PUT 和 PATCH 中没有提供直接使用json参数的方法，因此需要用data来传入
                data = complexjson.dumps(json)
            return Res(self.session.put(url, data, **kwargs))
        if method == "DELETE":
            return Res(self.session.delete(url, **kwargs))
        if method == "PATCH":
            if json:
                data = complexjson.dumps(json)
            return Res(self.session.patch(url, data, **kwargs))

    def __request_log(self, url, method, data=None, json=None, **kwargs):
        logger.info("请求地址 ==>> {}".format(url))
        logger.info("请求方式 ==>> {}".format(method))
        if data:
            logger.info("请求参数data ==>> {}".format(complexjson.dumps(data, indent=4, ensure_ascii=False)))
        if json:
            logger.info("请求参数json ==>> {}".format(complexjson.dumps(json, indent=4, ensure_ascii=False)))
        for k, v in dict(**kwargs).items():
            logger.info("请求参数{} ==>> {}".format(k, v))


class Res(object):
    def __init__(self, r):
        self.r = r

    @property
    def status_code(self):
        logger.info("接口响应状态码 ==>> %s" % self.r.status_code)
        return self.r.status_code

    def json(self):
        logger.info("接口响应状态码 ==>> %s" % self.r.status_code)
        logger.info("接口响应时间 ==>> %s" % str(self.r.elapsed.total_seconds()))
        logger.info("接口响应结果 ==>> %s" % str(self.r.text))
        logger.info("接口响应结果 ==>> %s" % complexjson.dumps(self.r.json(), indent=4, ensure_ascii=False))

        return self.r.json()

    @property
    def text(self):
        logger.info("接口响应状态码 ==>> %s" % self.r.status_code)
        logger.info("接口响应时间 ==>> %s" % str(self.r.elapsed.total_seconds()))
        logger.info("接口响应结果 ==>> %s" % self.r.text)
        return self.r.text

    @property
    def headers(self):
        logger.info("接口响应头 ===> %s" % self.r.headers)
        return self.r.headers

    @property
    def cookies(self):
        logger.info("接口cookies ===> %s" % self.r.cookies)
        return self.r.cookies
