#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Time: 2022-06-05 2:00 上午

Author: huayang

Subject:

"""
import os  # noqa
import doctest  # noqa
import inspect

# from collections import defaultdict
# from itertools import islice
# from pathlib import Path
from typing import *
from types import *

from pkgutil import walk_packages


# from tqdm import tqdm


def module_iter(path='.') -> Iterable[ModuleType]:
    """
    Examples:
        >>> _path = r'../'
        >>> modules = module_iter(_path)
        >>> m = next(modules)  # noqa
        >>> type(m)
        <class 'module'>

    """
    assert os.path.isdir(path)
    path = os.path.abspath(path)
    base = os.path.basename(path)
    for finder, module_name, is_pkg in walk_packages([path], base + '.'):
        loader = finder.find_module(module_name)
        module = loader.load_module(module_name)
        yield module


def get_line_number(obj):
    """ 获取对象行号
    基于正则表达式，所以不一定保证准确

    Examples:
        # 获取失败示例
        class Test:
        >>> class Test:  # 正确答案应该是这行，但因为上面那行也能 match，所以实际返回的是上一行
        ...     ''''''
        >>> # get_line_number(Test)

    """
    return inspect.findsource(obj)[1] + 1


if __name__ == '__main__':
    """"""
    doctest.testmod()
