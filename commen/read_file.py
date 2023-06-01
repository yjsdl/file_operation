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
    def __init__(self, path: str = None, sheet_name=None, encoding: str = 'utf-8', col: list = None,
                 is_list: bool = None):
        self._path = path
        self._sheet_name = sheet_name or 0
        self._encoding = encoding
        self._col = col
        self._fileType = path.rsplit('.', 1)[1]
        self._pf = None
        self._is_list = is_list

    def file_read(self):
        if self._fileType == 'xlsx':
            self._pf = file_type.get(self._fileType, None)(self._path, dtype=str, sheet_name=self._sheet_name).fillna(
                '')
        else:
            self._pf = file_type.get(self._fileType, None)(self._path, dtype=str).fillna('')

    @property
    def pf_sha(self):
        sha = self._pf.shape[0]
        return sha

    def screen_pf(self):
        self._pf = self._pf[self._col]

    def date_list(self):
        self._pf = self._pf[self._col].values.tolist()

    def start(self):
        self.file_read()
        if self._col is not None:
            self.screen_pf()
        if self._is_list:
            self.date_list()
        return self._pf


if __name__ == '__main__':
    c = ReadFile(r'Z:\数据科学平台客户数据\中国地质大学（武汉）\中国地质大学（武汉）别名表\官网别名表.csv', col=['姓名', '机构'], is_list=False)
    a = c.start()
    b = c.pf_sha
    print(b)

