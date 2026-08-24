# -*- coding: utf-8 -*-
# @Time    : 26/7/24 15:57
# @Author  : yy
# @File    : assert_util.py
# @Software: AutoTestFrame

"""
项目描述：断言封装
"""
import allure

from commons.logger_util import get_timed_logger
logger = get_timed_logger('frame', when='midnight', backup_count=30)

@allure.step("相等断言")
def assert_equals(a, b, assert_msg):
    '''
    相等断言
    '''
    try:
        assert a == b, assert_msg
        logger.info(f"测试结果：断言成功，测试通过")
    except:
        logger.error(f"测试结果：断言失败，预期结果：{b},实际结果：{a}")

@allure.step("不相等断言")
def assert_not_equals(a, b, assert_msg):
    '''
    不相等断言
    '''
    try:
        assert a != b, assert_msg
        logger.info(f"测试结果：断言成功，测试通过")
    except:
        logger.error(f"测试结果：断言失败，预期结果：{b},实际结果：{a}")

@allure.step("b包含a断言")
def assert_contains(a, b, assert_msg):
    '''
    b包含a断言
    '''
    try:
        assert a in b, assert_msg
        logger.info(f"测试结果：断言成功，测试通过")
    except:
        logger.error(f"测试结果：断言失败，预期结果：{b},实际结果：{a}")

@allure.step("b不包含a断言")
def assert_not_contains(a, b, assert_msg):
    '''
    b不包含a断言
    '''
    try:
        assert a not in b, assert_msg
        logger.info(f"测试结果：断言成功，测试通过")
    except:
        logger.error(f"测试结果：断言失败，预期结果：{b},实际结果：{a}")

@allure.step("a大于等于b断言")
def assert_lgt(a, b, assert_msg):
    '''
    a大于等于b断言
    '''
    try:
        assert a >= b, assert_msg
        logger.info(f"测试结果：断言成功，测试通过")
    except:
        logger.error(f"测试结果：断言失败，预期结果：{b},实际结果：{a}")

@allure.step("执行断言")
def do_assert(assert_value):
    '''
    解析yaml用例中的断言数据，调用对应的断言函数
    '''
    for assert_type, assert_data in assert_value.items():
        # 获取断言类型，断言内容
        for assert_msg, a_b_value in assert_data.items():
            # 获取断言信息和a、b值
            a = a_b_value[0]
            b = a_b_value[1]

            if assert_type == 'equals':
                assert_equals(a, b, assert_msg)
            elif assert_type == 'not_equals':
                assert_not_equals(a, b, assert_msg)
            elif assert_type == 'contains':
                assert_contains(a, b, assert_msg)
            elif assert_type == 'not_contains':
                assert_not_contains(a, b, assert_msg)
            else:
                assert False, f"错误的断言类型：{assert_type}"
