# -*- coding: utf-8 -*-
# @date：2023/5/25 15:26
# @Author：LiuYiJie
# @file： split_file
import os

from openpyxl import load_workbook, Workbook
from openpyxl.utils import range_boundaries
import pandas as pd
from logger_code.log import logger


def execl_split():
    # 定义每个文件的最大行数
    batch_size = 100000

    path = r'E:\任务数据\爱学术\图书信息.csv'
    # 打开Excel文件
    wb = load_workbook(path)

    # 获取第一个worksheet对象
    ws = wb.worksheets[0]

    # 获取打开文件的范围，即worksheet的行列数
    min_row, min_col, max_row, max_col = range_boundaries(ws.dimensions)

    # 计算需要分割的文件数量
    batch_count = (max_row - min_row) // batch_size + 1

    # 遍历每个文件并读取数据
    for batch_index in range(batch_count):
        # 计算当前文件的起始行和结束行
        start_row = min_row + batch_index * batch_size + 1
        end_row = min_row + (batch_index + 1) * batch_size

        # 创建新的Excel文件
        new_wb = Workbook()

        # 获取worksheet对象
        new_ws = new_wb.active

        # 遍历行并复制单元格数据到新的worksheet中
        for row in ws.iter_rows(min_row=start_row, min_col=min_col, max_row=end_row, max_col=max_col):
            row_data = [cell.value for cell in row]
            new_ws.append(row_data)

        # 保存新的Excel文件
        new_wb.save('path/to/new_excel_file_{}.xlsx'.format(batch_index + 1))


def csv_split(input_path, dest_path):
    # 定义每个小文件的行数
    chunk_size = 100000

    file_name = os.path.basename(input_path)
    logger.info('test')
    # 读取大文件
    reader = pd.read_csv(input_path, chunksize=chunk_size, dtype=str)

    if not os.path.exists(dest_path):
        os.makedirs(dest_path)

    col = {
        "name": "中文名",
        "nameENG": "英文名",
        "author": "作者",
        "authorSummary": "作者简介",
        "publishCompany": "出版社",
        "publishDate": "出版日期",
        "publishYear": "出版年份",
        "price": "出版价格",
        "summary": "内容简介",
        "coverPath": "图书封面",
        "langValue": "语种",
        "editor": "编者",
        "subtitle": "副题名",
        "seriesName": "丛书名",
        "antistop": "主题词",
        "classZtf": "中图分类号",
        "winningInfo": "获奖信息",
        "pdfContent": "全文",
    }
    # 拆分文件并保存
    for i, chunk in enumerate(reader):
        res_path = os.path.join(dest_path, file_name.replace('.csv', f'{6}.xlsx'))
        # chunk now pf
        pf = chunk.rename(columns=col)
        pf.to_excel(res_path, index=False)


if __name__ == '__main__':
    path = r'E:\任务数据\爱学术\图书信息6.csv'
    dest_path = 'E:\任务数据\爱学术\图书信息'
    csv_split(path, dest_path)
