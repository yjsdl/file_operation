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

with pdfplumber.open(r'F:\mysubject\files_operation\1ac24d74-f898-4ec2-949c-3a9f3858045d.pdf') as pdf:
    print(pdf.pages)  # Page对象列表
    page = pdf.pages[1]
    # print(page.extract_text())  # 提取文本
    # lists = page.extract_table()
    for row in page.extract_text().split('\n'):
        print(row)

