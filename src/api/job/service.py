# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @File   :service.py
# @Author :haohaiyo
# @Time   :2022/9/11 23:18
import logging

from flask import request
from lxml import html

from src import ResultERR, HttpRes
from src.api.login.user import User
from src.utils.http_client import HttpClient

logger = logging.getLogger(__name__)


def get_item_info(itemid):
    url = "http://www.cardhobby.com.cn/market/item/%s" % itemid
    user = request.cookies.get("username")
    # user = '18140563517'
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36",
        "Referer": "http://www.cardhobby.com.cn/Verify/index",
    }
    if user not in User:
        raise ResultERR(HttpRes.FAIL_LOGIN_TIMEOUT)
    ret = HttpClient().get(url, headers=headers, cookies=User[user])
    tree = html.fromstring(ret.text)
    endtime = tree.xpath('//*[@id="cardItem"]/div/div/div/div[2]/div[2]/div/table/tbody/tr[1]/td[3]/div/text()')[0]
    price = tree.xpath('//*[@id="currentPrice"]/text()')[0]
    name = tree.xpath('//*[@id="cardItem"]/div/div/div/div[2]/div[1]/div/text()')[1]
    img = tree.xpath('//*[@id="preview"]/span/img/@src')[0]
    d = {"item_name": name.strip(),
         "img": img,
         "endtime": endtime,
         "price": price.strip()}
    logger.info("商品详情：%s" % str(d))
    return d


def bidItemPrice(itemid, price, user):
    url = 'http://www.cardhobby.com.cn/market/BidItemPrice'
    params = "itemid=%s&price=%s" % (itemid, price)
    # data={"itemid":"11822891",}
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36",
        "Referer": "http://www.cardhobby.com.cn/market/item/%s" % itemid,
    }
    ret = HttpClient().post(url, params=params, headers=headers, cookies=User[user])
    logging.info("【出价】商品id：%s 入参：%s 出价结果：%s" % (itemid, params, ret.text))
