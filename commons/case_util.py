# -*- coding: utf-8 -*-
# @Time    : 26/7/14 15:18
# @Author  : yy
# @File    : case_util.py
# @Software: AutoTestFrame

"""
项目描述：读取测试用例内容
"""

from pathlib import Path

from commons.model_util import verify_yaml
from commons.yaml_util import YamlUtil

case_dir_str = 'tests/yaml_cases'  #指定用例目录

def get_case_list():
    case_list = []
    case_dir_path = Path(case_dir_str)
    yaml_path_list = list(case_dir_path.glob('test_*.yaml'))  #从目录搜索以test_开关的文件,返回文件列表，可任意修改
    #按文件名进行排序，调整用例执行顺序
    yaml_path_list.sort()

    for yaml_path in yaml_path_list:
        #打开yaml文件加载内容
        data = YamlUtil(yaml_path).read()

        #识别数据驱动
        try:
            parametrize = data.get("parametrize")
            if parametrize:
                pass
        except:
            pass

        #校验文件内容
        case = verify_yaml(data)
        case_list.append(case)

    #以列表形式返回yaml用例内容
    return case_list