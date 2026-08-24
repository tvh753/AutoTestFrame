# -*- coding: utf-8 -*-
# @Time    : 26/7/20 14:15
# @Author  : yy
# @File    : main_util.py
# @Software: AutoTestFrame

"""
项目描述：用例执行文件
"""
import allure

from commons.assert_util import do_assert
from commons.extract_util import do_extract, do_inject
from commons.request_util import RequestUtil


def stand_case_flow(case_info):


    # allure.dynamic.epic("接口测试框架")
    # if case_info.feature:
    #     allure.dynamic.feature(case_info.feature)
    # if case_info.story:
    #     allure.dynamic.story(case_info.story)
    # if case_info.title:
    #     allure.dynamic.title(case_info.story)
    #

    #替换和使用变量
    new_request = do_inject(case_info.request)


    resp = RequestUtil().send_all_request(**new_request)

    #提取变量
    if case_info.extract:
        do_extract(resp,case_info.extract)
    #
    if case_info.validate:
        new_validate = do_inject(case_info.validate)
        do_assert(new_validate)
    #
    # if case_info.parametrize:
    #     print('进行数据驱动')