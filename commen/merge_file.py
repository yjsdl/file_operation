# -*- coding: utf-8 -*-
# @date：2023/5/19 10:15
# @Author：LiuYiJie
# @file： merge_file
import abc
import os
import re
import pandas as pd
from typing import Optional
from commen.read_file import ReadFile
from commen.logger_code.stream_handler import log
logging = log()


class MergeFile:
    all_list = list()
    table_head = []

    def __init__(self, col: Optional[list] = None):
        self._col = col

    def read_File(self, path):
        for root, dirs, files in os.walk(path):
            # 判断是否是需要筛选的文件夹,返回True，不处理当前文件夹
            if self.is_filter_file(root):
                continue
            for file in files:
                # 排除压缩文件
                # if not file.endswith('.zip'):
                #     continue
                file_path = os.path.join(root, file)
                print(file_path)
                data = ReadFile(path=file_path, col=self._col).start()
                print(data.columns)
                self.all_list.append(data)

    @abc.abstractmethod
    def is_filter_file(self, root) -> bool:
        #   对文件进行删选
        return False

    def Merge_File(self, path) -> pd.DataFrame:
        self.read_File(path)
        pf = pd.concat(self.all_list)
        return pf

    def get_all_file(self, path):
        self.read_File(path)
        pf = pd.concat(self.all_list)
        dest_path = os.path.join(path.rsplit('\\', 1)[0], '结果文件.csv')
        pf.to_csv(dest_path, index=False, encoding='utf-8')

if __name__ == '__main__':
    c = MergeFile(col=['C1', 'RP'])
    path = r'Z:\客户数据存储\WOS\中国地质大学\OG=(China University of Geosciences) AND (PY==(2019))'
    c.get_all_file(path)
