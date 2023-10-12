# -*- coding: utf-8 -*-
# @date：2023/5/19 10:15
# @Author：LiuYiJie
# @file： merge_file
import abc
import os
import re
import pandas as pd
from commen.read_file import ReadFile


class MergeFile:
    all_list = list()
    table_head = []

    # def read_File(self, path):
    #     if os.path.isdir(path):
    #         twoFiles = os.listdir(path)
    #         for file in twoFiles:
    #             src_path = os.path.join(path, file)
    #             print(src_path)
    #             if os.path.isdir(src_path):
    #                 self.read_File(src_path)
    #             else:
    #                 if src_path.endswith('csv'):
    #                     pf = pd.read_csv(src_path, dtype=str).fillna('')
    #                     self.all_list.append(pf)
    #                 elif src_path.endswith('xlsx'):
    #                     pf = pd.read_excel(src_path, sheet_name=0, dtype=str).fillna('')
    #                     self.all_list.append(pf)
    #                 elif src_path.endswith('xls'):
    #                     with open(src_path, 'r', encoding='utf-8') as f:
    #                         data = f.read()
    #                         rows = re.findall(r'<Row ss:AutoFitHeight=\'1\'>(.*?)</Row>', data)
    #                         items = list()
    #                         for row in rows:
    #                             item = re.findall(r'<Data ss:Type=\'String\'>(.*?)</Data>', row)
    #                             item = dict(zip(self.table_head, item))
    #                             items.append(item)
    #                         pf = pd.DataFrame(data=items, columns=self.table_head)
    #                         self.all_list.append(pf)
    #                 elif src_path.endswith('html'):
    #                     pf = pd.read_html(src_path, dtype=str, header=0)[0].fillna('')
    #                     self.all_list.append(pf)
    #                 elif src_path.endswith('txt'):
    #                     pf = pd.read_table(src_path, dtype=str).fillna('')
    #                     self.all_list.append(pf)

    def read_File(self, path):
        for root, dirs, files in os.walk(path):
            # 判断是否是需要筛选的文件夹,返回True，不处理当前文件夹
            if self.is_filter_file(root):
                continue
            for file in files:
                # 排除压缩文件
                if not file.endswith('.txt'):
                    continue
                file_path = os.path.join(root, file)
                print(file_path)
                data = ReadFile(path=file_path).start()
                self.all_list.append(data)

    @abc.abstractmethod
    def is_filter_file(self, root) -> bool:
        #   对文件进行删选
        return False

    def Merge_File(self, path) -> pd.DataFrame:
        self.read_File(path)
        pf = pd.concat(self.all_list)
        return pf
        # dest_path = os.path.join(path, '结果文件.csv')
        # pf.to_csv(dest_path, index=False, encoding='utf-8')


if __name__ == '__main__':
    c = MergeFile()
    path = r'Z:\客户数据存储\WOS\河海大学'
    c.Merge_File(path)
