# -*- coding: utf-8 -*-
# @Time    : 26/7/20 14:34
# @Author  : yy
# @File    : extract_util.py
# @Software: AutoTestFrame

"""
项目描述：提取变量
"""
import copy
import re

import allure
import jsonpath as jsonpath
import yaml

from hotload.debgu_talk import DebugTalk

g_var = {}


def verify_resp(resp):
    '''
    修改响应内容
    :param resp:
    :return:
    '''
    resp = copy.copy(resp)
    resp.status_code = str(resp.status_code)  # 数字 -> 字符
    resp.headers = dict(resp.headers)  # 对象 -> 字典
    resp.cookies = dict(resp.cookies)  # 对象 -> 字典
    try:
        resp.json = resp.json()
    except Exception:
        resp.json = {}

    return resp

@allure.step("变量提取")
def do_extract(resp, extract_value):
    '''
    进行变量提取
    :param resp:
    :param extract_value:
    :return:
    '''
    resp = verify_resp(resp)

    for k, v in extract_value.items():
        # 1.把键值对拆分成4个平级的参数  for var_name,v in extract_value.items():
        var_name = k
        attr_name, pattern, index = v
        # 2.把参数传给统一变量提取入口 extract
        extract(resp, var_name, attr_name, pattern, index)


def extract(resp, var_name, attr_name, pattren, index=0):
    '''
    统一变量提取入口
    :param resp: 响应内容
    :param var_name: 提取的变量名
    :param attr_name: 提取方式
    :param pattren: 表达式
    :param index: 取值下标，默认0
    :return:
    '''
    if attr_name in ["headers", "cookies", "json"]:
        extract_jsonpath(resp, var_name, attr_name, pattren, index)
    else:
        extract_re(resp, var_name, attr_name, pattren, index)

@allure.step("jsonpath提取变量")
def extract_jsonpath(resp, var_name, attr_name, pattern, index):
    '''
    jsonpath提取
    :param resp: 响应内容
    :param var_name: 提取的变量名
    :param attr_name: 提取方式
    :param pattren: 表达式
    :param index: 取值下标，默认0
    :return:
    '''
    attr = getattr(resp, attr_name)  # attr_name是字符串，attr是对象

    # 数据提取
    data = jsonpath.jsonpath(attr, pattern)[index]

    # 把提取到的数据加载到全局变量
    g_var[var_name] = data
    # print(f'提取到的变量：{var_name} = {data}')
    return True

@allure.step("正则提取提取变量")
def extract_re(resp, var_name, attr_name, pattern, index):
    '''
    正则提取
    :param resp: 响应内容
    :param var_name: 提取的变量名
    :param attr_name: 提取方式
    :param pattren: 表达式
    :param index: 取值下标，默认0
    :return:
    '''
    attr = getattr(resp, attr_name)  # attr_name是字符串，attr是对象

    # 数据提取
    data = re.findall(pattern, str(attr))[index]

    # 把提取到的数据加载到全局变量
    g_var[var_name] = data
    # print(f'提取到的变量：{var_name} = {data}')
    return True

@allure.step("注入变量")
def do_inject(data):
    # 注入变量和函数

    # 1.数据转字符串
    data_str = yaml.safe_dump(data, allow_unicode=True, sort_keys=False)
    data = do_use_vars(data_str)

    data_str = yaml.safe_dump(data, allow_unicode=True, sort_keys=False)
    data = do_use_funcs(data_str)

    return data


def do_use_vars(data_str):
    '''
    引用提取的变量
    :param data: 原始数据
    :return:
    '''

    # 2.注入变量： `${name}` -> g_var[name']
    # 2.1 使用正则，找到所有  ${var_name}
    data = re.findall(r'\${(.*?)}', data_str)
    var_name_list = list(set(data))

    # 2.2 把${var_name} 替换成g_var[name']
    for var_name in var_name_list:
        vat_tag = "${" + var_name + "}"
        data_str = data_str.replace(vat_tag, g_var.get(var_name, vat_tag))

    # 3. 字符串转为数据
    new_data = yaml.safe_load(data_str)
    return new_data


def do_use_funcs(data_str):
    '''
    引用提取的变量，转成函数名，找到函数的参数列表，通过反射得到函数的返回值
    :param data: 原始数据
    :return:
    '''

    # 2.注入函数： `${time()}` -> 函数返回值    `${add(1,   2)}` ->  函数返回值
    # 2.1 使用正则，找到所有  ${func_name(func_args)}
    data = re.findall(r'\${(.*?)\((.*?)\)}', data_str)
    if data:
        func_call_list = list(set(data))

        # 2.2 把${func_name(func_args)} 函数返回值
        for func_cll in func_call_list:
            func_name = func_cll[0]  # 函数名
            func_args = []  # 函数的参数列表
            if func_cll[1] == "":  # 过滤掉不到参数的函数
                pass
            else:  # 参数处理
                args_list = func_cll[1].split(",")  # 带空格的参数
                for arg in args_list:
                    new_arg = do_use_vars(arg.strip())  # 去除参数中的无效空格
                    func_args.append(new_arg)  # 在参数在使用变量

            # 得到了函数名、和函数参数值，换回函数返回值
            func = getattr(DebugTalk(), func_name)
            func_result = func(*func_args)

            # 用函数的返回值替换掉原有的字符串
            func_tag = "${" + func_cll[0] + "(" + func_cll[1] + ")}"
            data_str = data_str.replace(func_tag, str(func_result))

        # 3. 字符串转为数据
        new_data = yaml.safe_load(data_str)
        return new_data
    else:
        new_data = yaml.safe_load(data_str)
        return new_data