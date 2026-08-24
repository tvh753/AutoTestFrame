# -*- coding: utf-8 -*-
# @Time    : 26/7/14 15:40
# @Author  : yy
# @File    : yaml_util.py
# @Software: AutoTestFrame

"""
项目描述：yaml文件读取
"""

import yaml


class YamlUtil:
    """YAML文件读写常用类"""

    def __init__(self, file):
        self.file = file

    def read(self):
        f = open(self.file, encoding="utf-8")

        data = yaml.safe_load(f)

        return data

    def write(self, data):
        f = open(self.file, "w", encoding="utf-8")

        yaml.safe_dump(data, f, allow_unicode=True, sort_keys=False)

        return True