#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Time:
    2022-08-22 18:36
Author:
    huayang (imhuay@163.com)
Subject:
    typing
References:
    - https://docs.python.org/zh-cn/3/library/typing.html
    - https://docs.python.org/zh-cn/3/library/typing.html#typing.TypeVar
"""
import os
import sys
import json
import time
import doctest

from typing import *
from pathlib import Path
from itertools import islice
from collections import defaultdict

NewStr = TypeVar('NewStr', str, bytes)
NewInt = NewType('NewInt', int)


def bar(a: NewInt):
    print(a)


class __Test:
    """"""

    def __init__(self):
        """"""
        for k, v in self.__class__.__dict__.items():
            if k.startswith('_test') and isinstance(v, Callable):
                print(f'\x1b[32m=== Start "{k}" {{\x1b[0m')
                start = time.time()
                v(self)
                print(f'\x1b[32m}} End "{k}" - Spend {time.time() - start:3f}s===\x1b[0m\n')

    def _test_doctest(self):  # noqa
        """"""
        import doctest
        doctest.testmod()

    def _test_TypeVar(self):  # noqa
        """"""

        class S(int):
            """"""

        def foo(a: NewStr, b: NewStr):
            print(a, b)

        # def bar(a: NewInt):
        #     print(a)

        bar(1)


if __name__ == '__main__':
    """"""
    __Test()
