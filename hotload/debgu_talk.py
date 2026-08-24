# -*- coding: utf-8 -*-
# @Time    : 26/7/22 17:04
# @Author  : yy
# @File    : debgu_talk.py
# @Software: AutoTestFrame

"""
项目描述：热加载文件，注册各种在yaml中使用的函数
"""
import random
import time


class DebugTalk:


    def time(self):
        return str(time.time())

    def add(self,a,b):
        return int(a) + int(b)

    def print(self, data):
        print("热加载要打印的内容是：",data)
        return "热加载要打印的内容是：",data

    def random(self):
       return random.randint(1,10)