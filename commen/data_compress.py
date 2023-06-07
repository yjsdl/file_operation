# -*- coding: utf-8 -*-
# @date：2023/6/7 15:56
# @Author：LiuYiJie
# @file： data_compress

import os
import re
import time
import datetime
import zipfile
from typing import List
import abc


class DataCompress:
    start_time: float
    SKIP_ZIP_TYPE = ('.zip', '.gz')

    def __init__(self,
                 data_path: str = None,
                 file_list: List[str] = None,
                 out_zip_file: str = None,
                 include: list = None,
                 exclude: list = None
                 ):
        if not os.path.exists(data_path):
            raise ValueError('路径不存在: %s' % data_path)
        if out_zip_file is None:
            raise ValueError('输出文件不能为空')
        print('输入路径: %s\n输出压缩文件: %s' % (
            data_path, out_zip_file)
              )
        self._data_path = data_path
        self._file_list = file_list
        self._out_zip_file = out_zip_file
        if include is not None:
            include = {str(i) for i in include}
        self._include = include
        if exclude is not None:
            exclude = {str(i) for i in exclude}
        self._exclude = exclude
        self._file_name = os.path.basename(self._data_path)

    @property
    def school_name(self):
        return self._file_name

    def pick_files(self) -> List[str]:
        """分拣文件"""
        if not self._file_list:
            new_file_list = []
            for root, dirs, files in os.walk(self._data_path):
                # 判断是否是需要筛选的文件夹,返回True，不处理当前文件夹
                if self.is_filter_file(root):
                    continue
                for file in files:
                    # 排除压缩文件
                    if file.endswith(self.__class__.SKIP_ZIP_TYPE):
                        continue
                    file = os.path.join(root, file)
                    new_file_list.append(file)
            self._file_list = new_file_list
        return self._file_list

    @abc.abstractmethod
    def is_filter_file(self, path) -> bool:
        """对文件目录做筛选, 返回结果为True跳过不处理, 不压缩当前文件"""
        return False

    def file2zip(self):
        """
        :param zip_file_name: 压缩后的文件
        :param file_names: 要压缩的文件列表
        :return:
        """
        with zipfile.ZipFile(self._out_zip_file, mode='w', compression=zipfile.ZIP_DEFLATED) as zf:
            for fn in self._file_list:
                # 去掉文件的根路径
                zf.write(fn, arcname=fn.replace(self._data_path, ''))

    def start(self):
        self.start_time = time.time()
        # 筛选要压缩的文件，如果没有指定筛选，那么压缩输入目录下的所有文件
        print('开始分拣待压缩文件...')

        self.pick_files()
        _pick_end_time = time.time()
        _pick_time = datetime.timedelta(seconds=_pick_end_time - self.start_time).total_seconds()

        print('分拣文件耗时 %s 秒，\n待压缩文件 %s 个' % (_pick_time, len(self._file_list)))
        # 执行压缩
        print('开始执行压缩...')
        self.file2zip()
        _zip_time = datetime.timedelta(seconds=time.time() - _pick_end_time).total_seconds()
        print('压缩后大小 %s ，\n压缩耗时 %s 秒' % (0, _zip_time))
        print('共耗时 %s 秒' % datetime.timedelta(seconds=time.time() - self.start_time).total_seconds())

    def zip2file(self):
        with zipfile.ZipFile(self._data_path, mode='r') as zf:
            zf.extractall(path=self._out_zip_file)


def test_compress(path):
    data_compress = DataCompress(
        data_path=path,
        out_zip_file=f'E:\任务数据\维普数据更新\郑州轻工业大学.zip',
        # include=[2022, 2023],
        # exclude=[2021, 2022, 2023]
    )
    data_compress.start()
    data_compress.zip2file()


if __name__ == '__main__':
    path = r'E:\任务数据\维普数据更新\四川大学'
    test_compress(path)
