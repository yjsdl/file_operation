# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import os
import re
import pandas as pd


# 保存到csv文件
def save_list(data, file, name):
    # desk = os.path.join(os.path.expanduser('~'), 'Desktop')
    # 当前文件夹
    file_path = os.path.dirname(__file__) + '/fin_result/' + file
    if os.path.isfile(file_path):
        df = pd.DataFrame(data=data)
        df.to_csv(file_path, encoding="utf-8", mode='a', header=False, index=False)
    else:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        df = pd.DataFrame(data=data, columns=name)
        df.to_csv(file_path, encoding="utf-8", index=False)


def html2xlsx(filepath, name, filename):
    pf_lists = []
    filenames = os.listdir(filepath)
    # filenames.sort(key=lambda x: int(x.split('-')[0]))  # 对读取的文件进行排序
    for file in filenames:
        file_path = os.path.join(filepath, file)
        print(file_path)
        if os.path.isdir(file_path):
            filenamess = os.listdir(file_path)
            # filenamess.sort(key=lambda x: int(x.split('-')[0]))  # 对读取的文件进行排序
            for file2 in filenamess:
                file_path2 = os.path.join(file_path, file2)
                try:
                    a = pd.read_html(file_path2, header=0)
                    print(file_path2)
                    pf_lists.append(a[0])
                except:
                    pass
        else:
            try:
                a = pd.read_html(file_path, header=0)
                pf_lists.append(a[0])
            except:
                pass
    # pf1 = pf_lists[0]
    # for aa in pf_lists[1:]:
    pf1 = pd.concat(pf_lists)
    new_filepath = fr'Z:\客户数据存储\CNKI\{name}\期刊(转码)\{filename}.xlsx'
    if not os.path.exists(os.path.dirname(new_filepath)):
        os.makedirs(os.path.dirname(new_filepath))
    pf1.to_excel(new_filepath, index=False)


# 不合并,原文件下
def html2xlsx2(filepath):
    # filenames.sort(key=lambda x: int(x.split('-')[0]))  # 对读取的文件进行排序
    for root, dirs, files in os.walk(filepath):
        for file in files:
            file_path = os.path.join(root, file)
            print(file_path)
            # 保存文件夹
            new_filepath = os.path.join(root + '(转换)', file.replace('xls', 'xlsx'))
            # 判断文件是否已经转换
            if os.path.isfile(new_filepath) or not file_path.endswith('xls'):
                continue
            a = pd.read_html(file_path, header=0)[0]
            if not os.path.exists(os.path.dirname(new_filepath)):
                os.makedirs(os.path.dirname(new_filepath))
            a.to_excel(new_filepath, index=False)


# 不合并,原文件下, txt文件转成csv
def txt2xlsx2(filepath):
    # filenames.sort(key=lambda x: int(x.split('-')[0]))  # 对读取的文件进行排序
    for root, dirs, files in os.walk(filepath):
        for file in files:
            file_path = os.path.join(root, file)
            print(file_path)
            # 保存文件夹
            new_filepath = os.path.join(root.replace('wos数据-教育学', 'wos数据-教育学(转换)'), file.replace('txt', 'csv'))
            # 判断文件是否已经转换
            if os.path.isfile(new_filepath) or not file_path.endswith('txt'):
                continue
            try:
                a = pd.read_table(file_path, header=0)
                if not os.path.exists(os.path.dirname(new_filepath)):
                    os.makedirs(os.path.dirname(new_filepath))
                a.to_csv(new_filepath, index=False, encoding='utf-8')
            except:
                print(file_path + '----------错误')



def merge_files(dirpath, name):
    filedirs = os.listdir(dirpath)
    filedirs.sort(key=lambda x: int(x.split('-')[0]))
    all_list = []
    for one_dir in filedirs:
        filenames = os.listdir(dirpath + one_dir)
        filenames.sort(key=lambda x: int(x.split('-')[0]))

        for file in filenames:
            file_path = dirpath + one_dir + '\\' + file
            pf1 = pd.read_csv(file_path, dtype=str)
            all_list.append(pf1)

    df = pd.concat(all_list)
    result_path = fr'F:\CNKI主站\中图分类号\file_result\{name}.csv'
    if not os.path.exists(os.path.dirname(result_path)):
        os.makedirs(os.path.dirname(result_path))
    print(name + ' 合并成功')
    df.to_csv(result_path, index=False)


if __name__ == '__main__':

    # # html2xls 转换后合并
    path = r'Z:\客户数据存储\CNKI\江南大学\AF%=江南大学\JOURNAL'
    html2xlsx(path, '江南大学', '江南大学')
    # 转换后不合并
    # html2xlsx2(path)
    # txt转成csv
    # txt2xlsx2(path)