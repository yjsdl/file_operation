# -*- coding: utf-8 -*-
# @date：2023/5/25 16:40
# @Author：LiuYiJie
# @file： read_file

import pandas as pd

file_type = {
    'csv': pd.read_csv,
    'xlsx': pd.read_excel,
    'txt': pd.read_table,
    'html': pd.read_html,
}


class ReadFile:
    def __init__(self, path: str = None, sheet_name=None, encoding: str = 'utf-8'):
        self._path = path
        self._sheet_name = sheet_name or 0
        self._encoding = encoding
        self._fileType = path.rsplit('.', 1)[1]

    def file_read(self):
        if self._fileType == 'xlsx':
            pf = file_type.get(self._fileType, None)(self._path, dtype=str, sheet_name=self._sheet_name).fillna('')
        else:
            pf = file_type.get(self._fileType, None)(self._path, dtype=str).fillna('')
        return pf

    def screen_pf(self):
        pass


if __name__ == '__main__':
    c = ReadFile(r'EZ:\数据科学平台客户数据\中国地质大学（武汉）\中国地质大学（武汉）别名表\官网别名表.csv')
    c.file_read()
