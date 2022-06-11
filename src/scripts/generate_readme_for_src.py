#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Time: 2022-05-17 8:55 下午

Author: huayang

Subject:

"""
import os
import re
import sys
import inspect

from dataclasses import dataclass
from collections import defaultdict
# from itertools import islice
# from pathlib import Path
from types import *
from typing import *


# from tqdm import tqdm

class args:  # noqa
    flag = 'huaytools'
    script_path = os.path.dirname(__file__)
    repo_path = os.path.abspath(os.path.join(script_path, '../..'))
    src_path = os.path.join(repo_path, 'src')
    algo_path = os.path.join(repo_path, 'algorithms')
    prefix_topics = 'topics'
    prefix_problems = 'problems'
    prefix_notes = '_notes'
    problems_path = os.path.join(algo_path, prefix_problems)
    notes_path = os.path.join(algo_path, prefix_notes)
    topics_path = os.path.join(algo_path, prefix_topics)


sys.path.append(args.src_path)

try:
    from huaytools.tools.code_analysis import module_iter, slugify
    from huaytools._python.file_utils import file_concat
    from huaytools._python.utils import get_logger
    from huaytools.tools.auto_readme import *
except:
    ImportError(f'import huaytools error.')

logger = get_logger()

WORK_UTILS = (10, 'Work Utils')
PYTORCH_MODELS = (20, 'Pytorch Models')
PYTORCH_UTILS = (30, 'Pytorch Utils')
PYTHON_UTILS = (40, 'Python Utils')

TAG_MAPPING = {
    'NLP Utils': WORK_UTILS,
    'Image Utils': WORK_UTILS,
    'Work Utils': WORK_UTILS,
    'Python Utils': PYTHON_UTILS,
    'Python 自定义数据结构': PYTHON_UTILS,
    'Pytorch Models': PYTORCH_MODELS,
    'Pytorch Utils': PYTORCH_UTILS,
    'Pytorch Loss': PYTORCH_UTILS,
    'Pytorch Train Plugin': PYTORCH_UTILS,
}

RE_INFO = re.compile(r'<!--(.*?)-->', flags=re.S)
RE_TAG = re.compile(r'Tag: (.*?)\s')
RE_SEP = re.compile(r'[,，、]')
RE_TITLE = re.compile(r'#+\s+(.*?)$')
RE_INDENT = re.compile(r'^([ ]*)(?=\S)', re.MULTILINE)

beg_details_tmp = '<details><summary><b> {key} <a href="{url}">¶</a></b></summary>\n'
beg_details_cnt_tmp = '<details><summary><b> {key} [{cnt}] <a href="{url}">¶</a></b></summary>\n'
end_details = '\n</details>\n'
auto_line = '<font color="LightGrey"><i> `This README is Auto-generated` </i></font>\n'


def hn_line(line, lv=2):
    """"""
    return f'{"#" * lv} {line}'


class Codes:
    """"""

    @dataclass()
    class DocItem:
        """ 每个 docstring 需要提取的内容 """
        flag: Tuple
        summary: str
        content: str
        module_path: str
        line_no: int
        link: str = None

        def __post_init__(self):
            self.link = f'[source]({self.module_path}#L{self.line_no})'

        def get_block(self, prefix=''):
            """"""

            block = f'### {self.summary}\n'
            block += f'> [source]({os.path.join(prefix, self.module_path)}#L{self.line_no})\n\n'
            # block += f'<details><summary><b> Intro & Example </b></summary>\n\n'
            block += '```python\n'
            block += f'{self.content}'
            block += '```\n'
            # block += '\n</details>\n'

            return block

    def __init__(self):
        """"""
        self.code_readme_path = os.path.join(args.src_path, 'README.md')
        self.toc_name = self.__class__.__name__
        self.code_basename = os.path.basename(os.path.abspath(args.src_path))
        self.docs_dt = self.parse_docs()
        self.content = self.gen_readme_md_simply(self.docs_dt)

    def parse_docs(self):
        """ 生成 readme for code """
        docs_dt = defaultdict(list)

        sys.path.append(args.repo_path)
        for module in module_iter(args.src_path):
            if hasattr(module, '__all__'):
                # print(module.__name__)
                for obj_str in module.__all__:
                    obj = getattr(module, obj_str)
                    if isinstance(obj, (ModuleType, FunctionType, type)) \
                            and getattr(obj, '__doc__') \
                            and obj.__doc__.startswith('@'):
                        # print(obj.__name__)
                        doc = self.parse_doc(obj)
                        docs_dt[doc.flag].append(doc)

        return docs_dt

    def parse_doc(self, obj) -> DocItem:
        """"""
        raw_doc = obj.__doc__
        lines = raw_doc.split('\n')
        flag = TAG_MAPPING[lines[0][1:]]

        lines = lines[1:]
        min_indent = self.get_min_indent('\n'.join(lines))
        lines = [ln[min_indent:] for ln in lines]

        summary = f'`{obj.__name__}: {lines[0]}`'
        content = '\n'.join(lines)

        line_no = self.get_line_number(obj)
        module_path = self.get_module_path(obj)
        return self.DocItem(flag, summary, content, module_path, line_no)

    @staticmethod
    def get_line_number(obj):
        """ 获取对象行号
        基于正则表达式，所以不一定保证准确
        """
        return inspect.findsource(obj)[1] + 1

    @staticmethod
    def get_module_path(obj):
        abs_url = inspect.getmodule(obj).__file__
        dirs = abs_url.split('/')
        idx = dirs[::-1].index(args.flag)  # *从后往前*找到 my 文件夹，只有这个位置是基本固定的
        return '/'.join(dirs[-(idx + 1):])  # 再找到这个 my 文件夹的上一级目录

    @staticmethod
    def get_min_indent(s):
        """Return the minimum indentation of any non-blank line in `s`"""
        indents = [len(indent) for indent in RE_INDENT.findall(s)]
        if len(indents) > 0:
            return min(indents)
        else:
            return 0

    def gen_readme_md_simply(self, docs_dt: Dict[str, List[DocItem]]):
        """ 简化首页的输出 """
        # args = self.args
        # code_prefix = os.path.basename(os.path.abspath(args.code_path))
        # print(code_prefix)

        toc = [self.toc_name, '---']
        append_toc = [self.toc_name, '---']
        readme_lines = []
        # append_lines = []

        key_sorted = sorted(docs_dt.keys())
        for key in key_sorted:
            blocks = docs_dt[key]
            key = key[1]
            toc.append(beg_details_tmp.format(key=key, url=f'#{slugify(key)}'))

            # append_toc.append(beg_details_tmp.format(key=key, url=f'{self.code_basename}/README.md#{slugify(key)}'))
            append_toc.append('### {key} [¶]({url})\n'.format(key=key,
                                                              url=f'{self.code_basename}/README.md#{slugify(key)}'))

            readme_lines.append(hn_line(key, 2))
            # append_lines.append(hn_line(key, 2))
            for d in blocks:
                toc.append(f'- [{d.summary}](#{slugify(d.summary)})')
                append_toc.append(f'- [{d.summary}]({self.code_basename}/README.md#{slugify(d.summary)})')
                readme_lines.append(d.get_block())
                # append_lines.append(d.get_block(prefix=code_prefix))

            toc.append(end_details)

            # append_toc.append(end_details)
            append_toc.append('\n')

        toc_str = '\n'.join(toc[:2] + [auto_line] + toc[2:])
        sep = '\n---\n\n'
        content_str = '\n\n'.join(readme_lines)
        code_readme = toc_str + sep + content_str
        # with open(self.code_readme_path, 'w', encoding='utf8') as fw:
        #     fw.write(code_readme)
        fw_helper.write(self.code_readme_path, code_readme)

        append_toc_str = '\n'.join(append_toc)
        main_append = append_toc_str + sep  # + '\n\n'.join(append_lines)
        return main_append


class Demo:
    def __init__(self):
        """"""
        doctest.testmod()


if __name__ == '__main__':
    """"""
    Demo()
