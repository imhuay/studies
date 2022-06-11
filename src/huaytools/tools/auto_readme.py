#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Time: 2022-01-18 10:51 上午

Author: huayang

Subject:
    帮助生成 studies 仓库下各模块的目录
"""
import os  # noqa
import doctest  # noqa

# from collections import defaultdict
# from itertools import islice
from pathlib import Path
from typing import *

# from tqdm import tqdm

from huaytools.utils import get_logger

logger = get_logger()


class _FileWriteHelper:
    """"""
    add_cnt = 0

    def write(self, abspath, content):
        """"""
        old_content = ''
        if os.path.exists(abspath):
            old_content = open(abspath, encoding='utf8').read()

        if old_content != content:
            with open(abspath, 'w', encoding='utf8') as fw:
                fw.write(content)

            command_ln = f'git add "{abspath}"'
            logger.info(command_ln)
            os.system(command_ln)
            self.add_cnt += 1


fw_helper = _FileWriteHelper()
"""单例模式"""


class TreeTOC:
    """"""
    # relative_path = r'.'
    black_kw = ('_assets',)
    sort_lv = {}
    tree: List[str]
    content: str

    def __init__(self, dir_path):
        """"""
        self.toc_name = self.__class__.__name__
        self.dir_path = Path(dir_path)

        self.gen_local_readme_flag = True
        self.gen_local_readme()

        self.gen_local_readme_flag = False
        self.gen_main_readme()

    def process_relative_path(self, path: Path):
        parts = path.parts
        if self.gen_local_readme_flag:
            return os.path.join(*parts[2:])  # ../a/b -> b
        return os.path.join(*parts[1:])  # ../a/b -> a/b

    @staticmethod
    def no_readme(path: Path):
        """"""
        return not (path / 'README.md').exists()

    def get_toc_link(self, path: Path, dir_lv):  # noqa
        """"""
        space_prefix = '    ' * dir_lv
        path_name = path.name
        if self.no_readme(path) or path_name.startswith('-'):
            path_name = path_name[1:] if path_name.startswith('-') else path_name
            link = space_prefix + '- ' + f'{path_name}'
        else:
            link = space_prefix + '- ' + f'[{path_name}]({self.process_relative_path(path)})'
        return link

    def gen_local_readme(self):
        """"""
        self.tree = [self.toc_name, '===']
        self.generate_toc(self.dir_path)
        content = '\n'.join(self.tree)
        fp = os.path.join(self.dir_path, 'README.md')
        fw_helper.write(fp, content)

    def gen_main_readme(self):
        self.tree = [self.toc_name, '---']
        self.generate_toc(self.dir_path)
        self.content = '\n'.join(self.tree)

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

    def key_fn(self, path: Path):
        return self.sort_lv.get(path.name, '~'), path.name

    def allow_fn(self, fp: Union[str, Path]):
        is_dir = os.path.isdir(fp)
        no_startswith__ = not str(fp.name).startswith('_')
        no_black_kw = all(kw not in str(fp) for kw in self.black_kw)
        return is_dir and no_startswith__ and no_black_kw


class Notes(TreeTOC):
    """"""
    # relative_path = r'../notes'
    sort_lv = {
        '算法': 'note-00',
        '机器学习': 'note-01',
        '深度学习': 'note-02',
        '自然语言处理': 'note-03',
        '搜索、广告、推荐': 'note-04',

        '预训练语言模型': 'NLP-01',
        '细粒度情感分析': 'NLP-02',

        'Python': 'PL-01',
        'CCpp': 'PL-02',
        'Java': 'PL-03',

        '基础知识': '01',
        '语法备忘': '~-98',
        '常见报错记录': '~-99'
    }


class Books(TreeTOC):
    """"""
    # relative_path = r'../books'
    sort_lv = {

    }


class Papers(TreeTOC):
    """"""
    # relative_path = r'../papers'
    sort_lv = {

    }


def _test():
    """"""
    doctest.testmod()

    # n = Notes(r'/Users/huayang/workspace/my/studies/notes')
    # print(n.content)


if __name__ == '__main__':
    """"""
    _test()
