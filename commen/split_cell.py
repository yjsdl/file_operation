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
    path = r'Z:\客户数据存储\CQVIP\上海交通大学\上海交通大学2009-2009中文发文.csv'
    splitCell(path)