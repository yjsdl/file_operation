# -*- coding: utf-8 -*-
# @date：2023/5/22 17:44
# @Author：LiuYiJie
# @file： stream_handler
import logging
import colorlog


def log():
    log_colors_config = {
        'DEBUG': 'white',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'bold_red',
    }
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        fmt="%(threadName)-10s | %(asctime)s.%(msecs)03d | %(levelname)-7s | %(name)s:%(funcName)s:line:%(lineno)d - %(message)s",
        datefmt='%Y-%m-%d %H:%M:%S')

    sh_fmt = colorlog.ColoredFormatter(
        fmt="%(log_color)s%(threadName)-10s | %(asctime)s.%(msecs)03d | %(levelname)-7s | %(name)s:%(funcName)s:line:%(lineno)d - %(message)s",
        datefmt='%Y-%m-%d  %H:%M:%S',
        log_colors=log_colors_config)

    sher = logging.StreamHandler()
    sher.setLevel(logging.DEBUG)
    sher.setFormatter(fmt=sh_fmt)
    logger.addHandler(sher)
    return logger


if __name__ == '__main__':
    c = log()
    c.info(f'本次操作数据库共 | 新增：{4:^4}条 | 更新：0条')
