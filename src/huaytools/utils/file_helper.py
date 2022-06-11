#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Time: 2021-10-01 10:50 下午

Author: huayang

Subject:

"""
import os
import json
import doctest

from typing import *
from collections import defaultdict

__all__ = [
    'list_dir_recur',
    'file_concat',
]


def list_dir_recur(src_path,
                   cond_fn: Callable[[str], bool] = lambda s: True) -> List[str]:
    """@Python Utils
    递归遍历目录下的所有文件

    Args:
        src_path:
        cond_fn: 条件函数，传入文件完整路径，判断是否需要加入返回列表
    """
    if not os.path.isdir(src_path):
        return [src_path]

    ret = []
    for dir_path, dir_names, file_names in os.walk(src_path):
        """"""
        for fn in file_names:
            fp = os.path.join(dir_path, fn)
            if cond_fn(fp):
                ret.append(fp)

    return ret


def file_concat(src_in: List[str], sep: str = '') -> str:
    """@Python Utils
    文件拼接

    Examples:
        >>> _dir = r'./-test'
        >>> os.makedirs(_dir, exist_ok=True)
        >>> f1 = os.path.join(_dir, r't1.txt')
        >>> os.system(f'echo 123 > {f1}')
        0
        >>> f2 = '456'  # f2 = os.path.join(_dir, r't2.txt')
        >>> _out = file_concat([f1, f2])  # 可以拼接文件、字符串
        >>> print(_out)
        123
        456
        <BLANKLINE>
        >>> _out = file_concat([f1, f2], '---')
        >>> print(_out)
        123
        ---
        456
        <BLANKLINE>
        >>> os.system(f'rm -rf {_dir}')
        0

    """

    def _fc(fc):
        txt = open(fc).read() if os.path.exists(fc) else fc
        return txt if txt.endswith('\n') else txt + '\n'

    if sep and not sep.endswith('\n'):
        sep += '\n'

    buf = sep.join([_fc(fp) for fp in src_in])

    return buf
    # with open(file_out, 'w') as fw:
    #     fw.write(buf)


if __name__ == '__main__':
    """"""
    doctest.testmod()

    dp = r'/Users/huayang/workspace/my/studies/src/huaytools/_python/_test_data'
    for fp in list_dir_recur(dp):
        print(fp)

    # for dirpath, dirnames, filenames in os.walk(dir_path):
    #     print(dirpath, dirnames, filenames)
    #     for fn in filenames:
    #         print(os.path.join(dirpath, fn))
