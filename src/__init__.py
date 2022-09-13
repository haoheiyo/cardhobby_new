# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @File   :__init__.py
# @Author :haohaiyo
# @Time   :2022/5/8 15:20
import uuid
import traceback
from flask import Flask, request, g, render_template
from flask_cors import CORS
import logging.config
from configs import Config
from src.enums.http_enum import HttpRes
from src.init.scheduler_init import scheduler_init
from src.utils.framework import auto_try, ResultERR, result
from src.init.exts import db as db
from src.init.log_factory import LOG_CONFIG_DICT

logger = logging.getLogger(__name__)


def create_app():
    logging.config.dictConfig(LOG_CONFIG_DICT)
    flask_app = Flask(__name__)

    # 加载配置
    flask_app.config.from_object(Config)

    # 开启cors
    CORS(flask_app, supports_credentials=True)

    # 初始化数据库
    db.init_app(flask_app)

    # 注册蓝图
    register_blueprint(flask_app)

    return flask_app


def register_blueprint(app):
    from src.api.login.views import login
    from src.api.job.views import job

    app.register_blueprint(login, url_prefix='/login')
    app.register_blueprint(job, url_prefix='/job')


scheduler = scheduler_init()
scheduler.start()
app = create_app()


# rpc提供者
# jsonrpc = JSONRPC(app, '/openapi', enable_web_browsable_api=True)
# from src.rpc import *


# rpc调用者
# server = ServiceProxy('http://127.0.0.1:5000/openapi')
# server.App.test1(1, 2)

# 全局拦截器 请求前
@app.before_request
def before_request_log():
    g.trace_id = uuid.uuid4().hex
    if request.method != 'OPTIONS':
        if request.method == 'GET':
            form_data1 = request.args
        elif request.method == 'POST':
            if request.json:
                form_data1 = request.json
            else:
                form_data1 = request.form
        else:
            form_data1 = ""
        logger.info("接口:%s,入参:%s" % (str(request.path), str(form_data1)))


# 全局拦截器 请求后
@app.after_request
def after_request_log(res):
    if request.method != 'OPTIONS':
        ret = res.json
        if not ret:
            ret = res.response
        logger.info("接口:%s,出参:%s" % (str(request.path), str(ret)))
    return res


@app.errorhandler(500)
def error_500(e):
    return result(HttpRes.ERR_SERVICES, tips=str(e.original_exception))


@app.errorhandler(ResultERR)
def error_ResultERR(e):
    logger.error(e.get_enum())
    return result(e.get_enum())


@app.errorhandler(Exception)
def error_Exception(e):
    logger.error(traceback.format_exc())
    return result(HttpRes.ERR_SERVICES, tips=str(e))


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=False, port=5000, host='localhost')
