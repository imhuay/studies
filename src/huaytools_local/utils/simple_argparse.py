#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Time: 2021-09-29 9:21 下午

Author: huayang

Subject: 一个简化版的 argparse

"""
import os
import sys
import json
import doctest
import argparse

from typing import *
from collections import defaultdict

__all__ = [
    'simple_argparse',
]

from huaytools_local.utils.dict_extensions import BunchDict


def simple_argparse(args=None):
    """@Python Utils
    一个简化版 argparse

    不需要预先设置字段，严格按照 `--a A` 一组的方式自动提取，
        其中 A 部分会调用 eval()，某种程度上比自带的 argparse 更强大

    Examples:
        >>> sys.argv = ['xxx.py', '--a', 'A', '--b', '1', '--c', '3.14', '--d', '[1,2]', '--e', '"[1,2]"']
        >>> simple_argparse()
        {'a': 'A', 'b': 1, 'c': 3.14, 'd': [1, 2], 'e': '[1,2]'}
        >>> _args = BunchDict(x=1, b=20)
        >>> simple_argparse(_args)
        {'x': 1, 'b': 1, 'a': 'A', 'c': 3.14, 'd': [1, 2], 'e': '[1,2]'}
        >>> sys.argv = ['xxx.py']
        >>> simple_argparse(_args)
        {'x': 1, 'b': 1, 'a': 'A', 'c': 3.14, 'd': [1, 2], 'e': '[1,2]'}
        >>> sys.argv = ['xxx.py', '-a', 'A']
        >>> simple_argparse()
        Traceback (most recent call last):
            ...
        AssertionError: `-a` should starts with "--"

    """
    from huaytools_local.utils import set_attr

    if len(sys.argv) < 2:
        return args

    if args is None:
        args = BunchDict()

    argv = sys.argv[1:]
    assert len(argv) % 2 == 0, argv

    for i in range(0, len(argv), 2):
        assert argv[i].startswith('--'), f'`{argv[i]}` should starts with "--"'

        name = argv[i][2:]
        try:
            value = eval(argv[i + 1])
        except:  # noqa
            value = argv[i + 1]

        set_attr(args, name, value)

    return args


if __name__ == '__main__':
    """"""
    doctest.testmod()
