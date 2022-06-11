#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Time: 2022-01-17 2:32 下午

Author: huayang

Subject:

"""
import os  # noqa
import doctest  # noqa

from typing import Union, List
# from itertools import islice
# from collections import defaultdict
from pathlib import Path


# from tqdm import tqdm


def default_allow_fn(fp: Union[str, Path]):
    black_kw = ('_assets',)

    is_dir = os.path.isdir(fp)
    no_startswith__ = not str(fp.name).startswith('_')
    no_black_kw = all(kw not in str(fp) for kw in black_kw)
    return is_dir and no_startswith__ and no_black_kw


def default_key_fn(path_name: Path):
    """"""
    path_dt = {
        # lv 1
        '机器学习': '01-01',
        '深度学习': '01-02',
        '自然语言处理': '01-03',

        # lv 2
        '预训练语言模型': '02-01',
        '细粒度情感分析': '02-02',
    }
    return path_dt.get(path_name.name, '~'), path_name


class DirParse:
    tree: List[str] = []

    def __init__(self, dir_path, allow_fn=None, key_fn=None):
        """"""
        self.dir_path = Path(dir_path)
        self.lv_start = len(self.dir_path.parts)
        self.allow_fn = allow_fn if allow_fn else default_allow_fn
        self.key_fn = key_fn if key_fn else default_key_fn

        # init
        self.generate_toc(self.dir_path)

    def get_toc_link(self, path, dir_lv):  # noqa
        """"""
        space_prefix = '    ' * dir_lv
        link = space_prefix + '- ' + f'[{path.name}]({path})'
        return link

    def generate_toc(self, path: Path, dir_lv=-1, with_top=False, max_lv=10000):
        """生成树形目录"""
        if with_top:
            dir_lv += 1

        if dir_lv >= max_lv:
            return

        if self.allow_fn(path) and dir_lv >= 0:
            link = self.get_toc_link(path, dir_lv)
            self.tree.append(link)

        if path.is_file():
            return

        path_iter = sorted(path.iterdir(), key=self.key_fn)
        for dp in path_iter:
            self.generate_toc(dp, dir_lv + 1)


def _test():
    """"""
    doctest.testmod()

    dp = DirParse(r'/notes')
    print('\n'.join(dp.tree))


if __name__ == '__main__':
    """"""
    _test()
