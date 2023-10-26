# -*- coding: utf-8 -*-
# @date：2023/7/13 17:16
# @Author：LiuYiJie
# @file： pdf_file


# from PyPDF2 import PdfReader
#
# reader = PdfReader(r'F:\mysubject\files_operation\1ac24d74-f898-4ec2-949c-3a9f3858045d.pdf')
# number_of_pages = len(reader.pages)
# print(number_of_pages)
# page = reader.pages[0]
# text = page.extract_text()
# print(text)


import pdfplumber
import pandas as pd

pf = pd.DataFrame()
path = r'F:\高校花名册\test\123456.pdf'

with pdfplumber.open(path) as pdf:
    print(pdf.pages)  # Page对象列表

    # page = pdf.pages[0]
    # print(page.extract_text())  # 提取文本
    # lists = page.extract_table()
    # for row in page.extract_text().split('\n'):
    #     print(row)

    pages = pdf.pages
    for page in pages:
        table = page.extract_table()
        pf = pf.append(table)
pf.to_excel(path.replace('.pdf', '.xlsx'), index=False, header=False, encoding='utf-8')
