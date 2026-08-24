# -*- coding: utf-8 -*-
# @Time    : 26/7/14 16:16
# @Author  : yy
# @File    : request_util.py
# @Software: AutoTestFrame

"""
项目描述：统一请求封装
"""
import allure

from commons.logger_util import get_timed_logger
import requests


logger = get_timed_logger('frame', when='midnight', backup_count=30)


class RequestUtil:
    # 类变量
    sess = requests.Session()  # 所有的请求使用同一个Session

    # 公共参数
    public_params = {
        "application": "app",
        "application_client_type": "android",
    }


    @allure.step("发送请求")
    def send_all_request(self, **kwargs):

        for k, v in kwargs.items():
            if k == 'params':
                kwargs['params'].update(self.public_params)

            logger.info(f"请求参数{k}：{v}")


        # 记录请求
        resp = self.sess.request(**kwargs)
        try:
            logger.info(f"接口响应体:{resp.json()}") # 方法，可能失败报错
        except Exception:
            logger.info(f"接口响应体:{resp.text}")

        return resp