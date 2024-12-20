# -*- coding: utf-8 -*-
# @date：2023/6/5 9:34
# @Author：LiuYiJie
# @file： save_file
import pandas as pd
import os
from typing import List
from commen.read_file import ReadFile

file_type = {
}


def xlsx2csv(path):
    pf = ReadFile(path).start()
    pf.to_csv(path.replace('xlsx', 'csv'), index=False, encoding='utf-8')


def csv2xlsx(path):
    pf = ReadFile(path).start()
    pf.to_excel(path.replace('csv', 'xlsx'), index=False)


class SaveFile:

    def __init__(self, path: str = None, headers: list = None, sheet_name: str = 'sheet1'):
        self._filepath = path
        self._fileType = path.rsplit('.', 1)[1]
        self._headers = headers
        self._sheet_name = sheet_name

    # 保存到csv文件
    def CsvSave(self, data):
        if not self._headers:
            self._headers = data[0].keys()
        # 当前文件夹
        is_exist = self.judgeFile(self._filepath)
        if is_exist:
            df = pd.DataFrame(data=data)
            df.to_csv(self._filepath, encoding="utf-8", mode='a', header=False, index=False)
        else:
            df = pd.DataFrame(data=data, columns=self._headers)
            df.to_csv(self._filepath, encoding="utf-8", index=False)

    # 保存到execl文件
    def ExeclSave(self, data):
        if not self._headers:
            assert self._headers is not None
        is_exist = self.judgeFile(self._filepath)
        if is_exist:
            odf = ReadFile(path=self._filepath).start()
            ndf = pd.DataFrame(data=data, columns=self._headers)
            df = pd.concat([odf, ndf], ignore_index=True)
            df.to_excel(self._filepath, encoding='utf-8', index=False, sheet_name=self._sheet_name)
        else:
            df = pd.DataFrame(data=data, columns=self._headers)
            df.to_excel(self._filepath, encoding="utf-8", index=False, sheet_name=self._sheet_name)

    # 保存到普通文件
    def TxtSave(self, data):
        if type(data) == list:
            data = [f'{i}\n' for i in data]
        f = open(self._filepath, 'w', encoding='utf-8')
        f.writelines(data)
        f.close()

    @staticmethod
    def judgeFile(filepath):
        if os.path.isfile(filepath):
            return True
        else:
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            return False


if __name__ == '__main__':
    datas = ['3', 'a', '4', 'b']
    # c = SaveFile(path=r'F:\高校花名册\file_in\三江学院\花名册\学校别名表.xlsx')
    xlsx2csv(path=r'F:\School_Roster\file_in\南京大学\教工信息（苏州）to汪老师.xlsx')
    # csv2xlsx(path=r'F:\School_Roster\file_in\上海交通大学\花名册\学生别名表raw.csv')