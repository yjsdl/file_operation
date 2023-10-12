# -*- coding: utf-8 -*-
# @date：2023/9/6 9:19
# @Author：LiuYiJie
# @file： split_cell
from commen.read_file import ReadFile


def splitCell(path):
    pf = ReadFile(path=path).start()
    pf1 = pf.set_index(["姓名", "编号", '机构'])["email"].str.split(",", expand=True).stack().reset_index(drop=True,level=-1).\
        reset_index().rename(columns={0: "email"})
    pf1.to_csv(path.replace('.csv', '拆分后.csv'), index=False, encoding='utf-8')

if __name__ == '__main__':
    path = r'F:\高校花名册\file_in\西安电子科技大学\花名册\学校别名表_before.csv'
    splitCell(path)