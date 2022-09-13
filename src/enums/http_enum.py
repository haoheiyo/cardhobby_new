# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @File   :http_enum.py
# @Author :haohaiyo
# @Time   :2022/5/8 15:20


from enum import Enum, unique


@unique
class HttpRes(Enum):
    def code(self):
        return self.value[0]

    def message(self):
        return self.value[1]

    SUCCESS = (200, '调用成功')
    SUCCESS_LOGIN = (20001, "登陆成功")
    SUCCESS_ADD_JOB = (20002, "任务添加成功")
    SUCCESS_REMOVE_JOB = (20002, "任务移除成功")


    ERR_SERVICES = (50001, '系统异常，请稍后再试！')
    FAIL_TOKEN = (40301, "授权码校验失败")
    FAIL_LOGIN = (40302, "登录失败")
    FAIL_ADD_JOB = (40303, "任务添加失败")
    FAIL_LOGIN_TIMEOUT = (40304, "登录态失效，请重新登录")




if __name__ == '__main__':
    print(HttpRes.SUCCESS.code(), HttpRes.SUCCESS.message())
