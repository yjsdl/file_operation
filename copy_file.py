# -*- coding: utf-8 -*-
# @date：2023/5/18 15:56
# @Author：LiuYiJie
# @file： copy_file
import os


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
    src_path = ''
    dest_path = ''
    copy_file(src_path, dest_path)