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


# 复制文件
def copy_file(src, dest):
    # 判断是否是文件夹
    if os.path.isdir(src):
        file_list = os.listdir(src)  # 拿到源文件夹里的所有文件
        # 遍历列表
        for file in file_list:
            # 得到全路径
            src_path = os.path.join(src, file)
            # 如果是文件夹 --> 在目标文件夹下新建文件夹然后复制
            target_path = os.path.join(dest, file)
            if not os.path.exists(os.path.dirname(target_path)):
                os.makedirs(os.path.dirname(target_path))

            if os.path.isdir(src_path):
                # 拿到文件夹的名然后在目标文件夹下新建
                copy_file(src_path, target_path)
            else:
                # 不是文件夹 --> 正常复制
                dest_path = os.path.join(dest, file)
                if os.path.exists(dest_path):
                    continue
                with open(src_path, 'rb') as rstream:
                    contain = rstream.read()

                    print(f'正在复制{src_path}')
                    with open(dest_path, 'wb') as wstream:
                        wstream.write(contain)
        else:
            print("复制完毕！")


if __name__ == '__main__':
    path = r'Z:\需求文档\代码\science-data-upload\science_data_upload\_base\school_sid.json'
    FileTime(path)
