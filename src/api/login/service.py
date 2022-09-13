# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @File   :service.py
# @Author :haohaiyo
# @Time   :2022/9/11 23:01
import logging
import requests

from src.api.login.user import User
from src.utils.http_client import HttpClient

logger = logging.getLogger(__name__)


def Login(username, password):
    url = "http://www.cardhobby.com.cn/Verify/Index"
    params = "username=%s&password=%s&commit=登录" % (username, password)
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36",
        "Referer": "http://www.cardhobby.com.cn/Verify/index",
    }
    ret = HttpClient().post(url, params=params, headers=headers, allow_redirects=False)
    logger.info(ret)
    cookies = ret.cookies
    cookies = requests.utils.dict_from_cookiejar(cookies)
    if 'userid' in cookies:
        User[username] = cookies
        logging.info("登录成功")
        return username
