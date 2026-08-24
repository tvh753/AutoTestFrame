# -*- coding: utf-8 -*-
# @Time    : 26/7/14 17:16
# @Author  : yy
# @File    : logger_util.py
# @Software: AutoTestFrame

"""
项目描述：日志封装
"""

import logging
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
import sys
from pathlib import Path


class LoggerManager:
    """日志管理器 - 支持追加和轮转"""
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        self._initialized = True
        self._loggers = {}
        # self._setup_default_logger()

    def _setup_default_logger(self):
        """设置默认日志配置"""
        self.get_logger('default')

    def get_logger(self, name='app', log_file=None, level=logging.INFO,
                   max_bytes=10 * 1024 * 1024, backup_count=5, when='midnight'):
        """
        获取或创建logger

        Args:
            name: logger名称
            log_file: 日志文件路径，None则使用默认
            level: 日志级别
            max_bytes: 单个日志文件最大字节数（RotatingFileHandler）
            backup_count: 保留的备份文件数
            when: 轮转时间间隔（TimedRotatingFileHandler）
        """
        if name in self._loggers:
            return self._loggers[name]

        logger = logging.getLogger(name)
        logger.setLevel(level)

        # 避免重复添加handler
        if logger.handlers:
            self._loggers[name] = logger
            return logger

        # 格式器
        # formatter = logging.Formatter(
        #     '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s',
        #     datefmt='%Y-%m-%d %H:%M:%S'
        # )

        # 1. 控制台处理器
        # console = logging.StreamHandler(sys.stdout)
        # console.setLevel(level)
        # console.setFormatter(formatter)
        # logger.addHandler(console)

        # 2. 文件处理器 - 默认追加模式
        if log_file is None:
            log_file = f'logs/{name}.log'

        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        # 方式A：普通FileHandler，追加模式（默认）
        # file_handler = logging.FileHandler(log_file, mode='a', encoding='utf-8')
        # file_handler.setLevel(level)
        # file_handler.setFormatter(formatter)
        # logger.addHandler(file_handler)

        self._loggers[name] = logger
        return logger

    def get_logger_with_rotation(self, name='app', log_file=None, level=logging.INFO,
                                 max_bytes=10 * 1024 * 1024, backup_count=5):
        """
        获取支持按大小轮转的logger（防止单个文件过大）
        """
        if name in self._loggers and f'{name}_rotation' in self._loggers:
            return self._loggers[f'{name}_rotation']

        logger = logging.getLogger(f'{name}_rotation')
        logger.setLevel(level)

        if logger.handlers:
            self._loggers[f'{name}_rotation'] = logger
            return logger

        formatter = logging.Formatter(
            '%(levelname)s %(asctime)s %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        # 控制台
        console = logging.StreamHandler(sys.stdout)
        console.setLevel(level)
        console.setFormatter(formatter)
        logger.addHandler(console)

        # 文件轮转 - 按大小
        if log_file is None:
            log_file = f'logs/{name}.log'

        Path(log_file).parent.mkdir(parents=True, exist_ok=True)

        # RotatingFileHandler: 文件达到max_bytes时自动轮转
        # mode='a' 表示追加
        file_handler = RotatingFileHandler(
            log_file,
            mode='a',  # 追加模式
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding='utf-8'
        )
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        self._loggers[f'{name}_rotation'] = logger
        return logger

    def get_logger_with_timed_rotation(self, name='app', log_file=None, level=logging.INFO,
                                       when='midnight', interval=1, backup_count=30):
        """
        获取支持按时间轮转的logger（每天一个文件）
        """
        key = f'{name}_timed'
        if key in self._loggers:
            return self._loggers[key]

        logger = logging.getLogger(key)
        logger.setLevel(level)

        if logger.handlers:
            self._loggers[key] = logger
            return logger

        formatter = logging.Formatter(
            '%(levelname)s %(asctime)s %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        # 控制台
        # console = logging.StreamHandler(sys.stdout)
        # console.setLevel(level)
        # console.setFormatter(formatter)
        # logger.addHandler(console)

        # 文件轮转 - 按时间
        if log_file is None:
            log_file = f'logs/{name}.log'

        Path(log_file).parent.mkdir(parents=True, exist_ok=True)

        # TimedRotatingFileHandler: 按时间轮转
        # when='midnight' 每天午夜轮转，保留backup_count个文件
        file_handler = TimedRotatingFileHandler(
            log_file,
            when=when,  # 'midnight', 'H'(小时), 'D'(天), 'W0'(周一) 等
            interval=interval,
            backupCount=backup_count,
            encoding='utf-8'
        )
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        self._loggers[key] = logger
        return logger


# 创建全局实例
logger_manager = LoggerManager()


# 便捷函数
def get_logger(name='app'):
    return logger_manager.get_logger(name)


def get_rotating_logger(name='app', max_bytes=10 * 1024 * 1024, backup_count=5):
    return logger_manager.get_logger_with_rotation(name, max_bytes=max_bytes, backup_count=backup_count)


def get_timed_logger(name='app', when='midnight', backup_count=30):
    return logger_manager.get_logger_with_timed_rotation(name, when=when, backup_count=backup_count)


# 默认logger
logger = get_logger()