# -*- coding: utf-8 -*-
# @Time    : 26/7/14 15:07
# @Author  : yy
# @File    : model_util.py
# @Software: AutoTestFrame

"""
项目描述：用例模板校验,dataclass数据校验：1.字段是否存在    2.字段是否正确
"""

from dataclasses import dataclass


@dataclass
class CaseInfo:
    # 必填项
    name: str
    request: dict
    validate: dict

    # 选填项
    feature: str = "默认模块"
    story: str = "默认功能"
    title: str = ""
    extract: dict = None
    parametrize: dict = None

    def __post_init__(self):
        if not self.title:
            self.title = self.name
        self.request = dict(self.request)
        self.validate = dict(self.validate)
        if self.extract:
            self.extract = dict(self.extract)
        if self.parametrize:
            self.parametrize = dict(self.parametrize)


def verify_yaml(date: dict):
    '''
    异常捕捉，返回解释说明
    :param date:
    :return:
    '''
    try:
        case_info = CaseInfo(**date)
        return case_info
    except Exception:
        raise Exception('测试用例的YAML内容不符合框架要求')