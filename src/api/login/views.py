# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @File   :views.py
# @Author :haohaiyo
# @Time   :2022/9/11 22:55
import json
import logging

from flask import Blueprint, request, make_response

from src import result, ResultERR, HttpRes
from src.api.login.service import Login

login = Blueprint('login', __name__)
logger = logging.getLogger(__name__)


@login.route('/login', methods=['post'])
def user_login():
    data = request.json or request.form
    token = data.get('token')
    if token != "1234qwer":
        return result(HttpRes.FAIL_TOKEN)
    username = data.get('username')
    password = data.get('password')
    user = Login(username, password)

    if user:
        r = result(HttpRes.SUCCESS_LOGIN, data={"user": username})
        resp = make_response(r)
        resp.set_cookie("username", user)
        return resp
    else:
        return result(HttpRes.FAIL_LOGIN)
