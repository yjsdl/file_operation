# -*- coding: utf-8 -*-
# @date：2023/5/25 15:26
# @Author：LiuYiJie
# @file： split_file

from openpyxl import load_workbook, Workbook
from openpyxl.utils import range_boundaries

# 定义每个文件的最大行数
batch_size = 1000

path = 'F:\高校花名册\标准花名册\三江学院检索策略.xlsx'
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