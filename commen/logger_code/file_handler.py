# -*- coding: utf-8 -*-
# @date：2023/5/22 17:50
# @Author：LiuYiJie
# @file： file_handler
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    "%(threadName)-10s | %(asctime)s.%(msecs)03d | %(levelname)-7s | %(name)s:%(funcName)s:line:%(lineno)d - %(message)s",
    datefmt='%Y-%m-%d %H:%M:%S')
fileHandler = logging.FileHandler('file_name.log')
fileHandler.setLevel(logging.DEBUG)
fileHandler.setFormatter(formatter)
logger.addHandler(fileHandler)
