# -*- coding: utf-8 -*-
# @date：2023/5/18 11:06
# @Author：LiuYiJie
# @file： file_time
import os
import time
from datetime import datetime


# 查看文件的时间
def FileTime(path):
    # 判断是否是文件夹
    if os.path.isdir(path):
        file_list = os.listdir(path)
        for file in file_list:
            # 是否是二级文件夹
            src_file = os.path.join(path, file)
            FileTime(src_file)
    else:
        # 不是文件夹直接输出时间
        # 创建时间,修改时间,访问时间
        ctime = os.path.getctime(path)
        ctime_string = datetime.fromtimestamp(int(ctime))
        mtime = os.path.getmtime(path)
        mtime_string = datetime.fromtimestamp(int(mtime))
        atime = os.path.getatime(path)
        atime_string = datetime.fromtimestamp(int(atime))
        print(f'{path}->创建时间->{ctime_string}')
        print(f'{path}->修改时间->{mtime_string}')
        print(f'{path}->访问时间->{atime_string}')
        # 当前时间
        stime = int(time.time())
        stime_string = datetime.fromtimestamp(stime)
        start_time = datetime.strptime(str(mtime_string), '%Y-%m-%d %H:%M:%S')
        end_time = datetime.now()
        print((end_time - start_time).days)


if __name__ == '__main__':
    path = r'F:\高校花名册\file_in\河北工业大学\花名册\官网别名表.csv'
    FileTime(path)
