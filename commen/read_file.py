# -*- coding: utf-8 -*-
# @date：2023/5/25 16:40
# @Author：LiuYiJie
# @file： read_file
from typing import Hashable, Sequence, Literal

import pandas as pd

file_type = {
    'csv': pd.read_csv,
    'xlsx': pd.read_excel,
    'txt': pd.read_table,
    'html': pd.read_html,
}


class ReadFile:
    def __init__(self, path: str = None, sheet_name: str = 'sheet1', encoding: str = 'utf-8', col: list = None,
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
        elif self._fileType == 'txt':
            self._pf = file_type.get(self._fileType, None)(self._path, dtype=str).fillna('')
        else:
            self._pf = file_type.get(self._fileType, None)(self._path, dtype=str).fillna('')

    def screen_pf(self):
        self._pf = self._pf[self._col]

    def date_list(self):
        columns = self._pf.columns
        _col = self._col or columns
        self._pf = self._pf[_col].values.tolist()

    def drop_Date(self, pf, subset=None, keep: str = 'first'):
        self._pf = pf.drop_duplicates(subset=subset, keep=keep)
        return self._pf

    def start(self) -> pd.DataFrame:
        self.file_read()
        if self._col is not None:
            self.screen_pf()
        if self._is_list:
            self.date_list()
        return self._pf


if __name__ == '__main__':
    c = ReadFile(r'E:\任务\2023-4-25\检索策略0420.csv', is_list=False)
    a = c.start()
    a.to_csv(r'F:\mysubject\files_operation\\以前.csv', index=False, encoding='utf-8')
