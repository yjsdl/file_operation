# -*- coding: utf-8 -*-
# @date：2023/5/25 16:40
# @Author：LiuYiJie
# @file： read_file
from typing import Hashable, Sequence, Literal, Union
from pandas import DataFrame
import pandas as pd

file_type = {
    'csv': pd.read_csv,
    'xlsx': pd.read_excel,
    'txt': pd.read_table,
    'html': pd.read_html,
    'xls': pd.read_excel
}


class ReadFile:
    def __init__(self, path: str = None, sheet_name: Union[str, int] = 0,
                 encoding: str = 'utf-8', col: list = None,
                 is_list: bool = None):
        self._path = path
        self._sheet_name = sheet_name or 0
        self._encoding = encoding
        self._col = col
        self._fileType = path.rsplit('.', 1)[1]
        self._pf = None
        self._is_list = is_list

    def file_read(self):
        try:
            if self._fileType == 'xlsx':
                self._pf = file_type.get(self._fileType, None)(self._path, dtype=str, sheet_name=self._sheet_name).fillna(
                    '')
            elif self._fileType == 'html':
                self._pf = file_type.get(self._fileType, None)(self._path, dtype=str, header=0)[0].fillna('')
            else:
                self._pf = file_type.get(self._fileType, None)(self._path, dtype=str).fillna('')
        except:
            pass

    def screen_pf(self):
        pf = self._pf[self._col]
        return pf

    def date_list(self):
        columns = self._pf.columns
        _col = self._col or columns
        pf = self._pf[_col].values.tolist()
        return pf

    def drop_Date(self, pf, subset=None, keep: str = 'first'):
        self._pf = pf.drop_duplicates(subset=subset, keep=keep)
        return self._pf

    def start(self) -> DataFrame:
        self.file_read()
        if self._col is not None:
            self._pf = self.screen_pf()
        if self._is_list:
            self._pf = self.date_list()
        return self._pf


if __name__ == '__main__':
    c = ReadFile(r'Z:\客户数据存储\专利\西安电子科技大学\xlsx\西电专利.csv', is_list=False).start()
    # d = ReadFile(r'F:\高校花名册\file_in\东南大学\花名册\学校别名表.csv', is_list=True).start()
    # a = c.start()
    c.to_csv(r'F:\mysubject\files_operation\上海交通大学花名册\校内部门代码.csv', index=False, encoding='utf-8')
