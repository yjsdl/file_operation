# -*- coding: utf-8 -*-
# @date：2024/1/9 16:49
# @Author：LiuYiJie
# @file： test_log

import logging
from logging import handlers
import datetime


class ColoredFormatter(logging.Formatter):
    COLORS = {
        "black": "\033[90m",  # 黑色
        "red": "\033[91m",  # 红色
        "green": "\033[92m",  # 绿色
        "yellow": "\033[93m",  # 黄色
        "blue": "\033[94m",  # 蓝色
        "purple": "\033[95m",  # 紫色
        "dgreen": "\033[96m",  # 深绿
        "white": "\033[97m",  # 白色
        "reset": '\033[0m',  # 默认
    }

    DEFAULT_STYLES = {
        "spam": "green",
        "debug": "green",
        "verbose": "blue",
        "info": "green",
        "warning": "yellow",
        "success": "green",
        "error": "red",
        "critical": "red",

        "asctime": "green",
        "message": "green",
        "lineno": "purple",
        "threadName": "red",
        "module": "red",
        "levelname": "white",
        "name": "blue",
    }

    def __init__(self, styles=None):
        super().__init__()
        self.styles = styles or self.DEFAULT_STYLES

    def set_color(self, msg: str = None):
        msg = msg or 'threadName - asctime - pathname - module: - funcName: - lineno - levelname - message'
        return ' - '.join(
            map(lambda part: f"{self.COLORS.get(self.styles.get(part, 'reset'))}{{}}{self.COLORS['reset']}",
                msg.split(' - ')))

    def format(self, record):
        levelname = record.levelname
        asctime = datetime.datetime.fromtimestamp(record.created).strftime('%Y-%m-%d %H:%M:%S')
        threadName = record.threadName
        pathname = record.pathname
        lineno = record.lineno
        funcName = record.funcName
        module = record.module
        message = super().format(record)

        color_msg = self.set_color(
            'threadName - asctime - pathname - module - funcName - lineno - levelname - message')

        colored_message = color_msg.format(threadName, asctime, pathname, module, funcName, lineno, levelname, message)
        return colored_message


class ColoredConsoleHandler(logging.StreamHandler):
    def __init__(self, formatter=None):
        super().__init__()
        self.formatter = formatter or ColoredFormatter()


def setup_logger():
    log_obj = logging.getLogger()
    log_obj.setLevel(logging.DEBUG)

    # 控制台输出
    console_handler = ColoredConsoleHandler()
    log_obj.addHandler(console_handler)

    # 文件输出，每天一个文件
    file_handler = handlers.TimedRotatingFileHandler("log_file.log", when="midnight", interval=1, backupCount=7)
    file_handler.setFormatter(logging.Formatter(
        '%(threadName)-10s - %(asctime)s - %(module)s - %(funcName)s:line:%(lineno)d - %(levelname)s - %(message)s'))
    log_obj.addHandler(file_handler)

    return log_obj


logger = setup_logger()
