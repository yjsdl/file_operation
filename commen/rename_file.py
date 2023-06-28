# -*- coding: utf-8 -*-
# @date：2023/6/28 9:31
# @Author：LiuYiJie
# @file： rename_file
import os
from commen.logger_code.stream_handler import log

log = log()


class RenameFile:
    def __init__(self, path: str = None, old_name: str = None, new_name: str = None, edit_num: int = 1):
        self._path = path
        self._old_name = old_name
        self._new_name = new_name
        self._edit_num = edit_num
        self._num = 0

    def rename_dir(self):
        if os.path.isdir(self._path):
            layers = os.listdir(self._path)
            for one in layers:
                old_path = os.path.join(self._path, one)
                new_path = os.path.join(self._path, f'OG=(Anhui University) AND (PY==({one}))')
                if self.is_filter_file(old_path):
                    continue
                os.rename(old_path, new_path)
        # if self._num == self._edit_num:
        #     return '重命名完成'
        # else:
        #     self._num += 1
        #     files = os.listdir(self._path)
        #     self._path = os.path.join(self._path, )
        #     return self.rename_dir()

    @staticmethod
    def is_filter_file(path):
        base_name = os.path.basename(path)
        if 'OG' in base_name and 'PY' in base_name:
            return True
        else:
            return False

    def one_file(self):
        old_path = os.path.join(self._path, self._old_name)
        new_path = os.path.join(self._path, self._new_name)
        os.rename(old_path, new_path)
        log.debug(f'重命名完成{old_path} --> {new_path}')


if __name__ == '__main__':
    c = RenameFile(path=r'E:\WOS\一流高校重新\安徽大学', old_name='3', new_name='33')
    c.rename_dir()

    # files = os.listdir(r'F:\mysubject\files_operation\test')