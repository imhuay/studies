#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Time:
    2022-08-05 18:09
Author:
    huayang (imhuay@163.com)
Subject:
    单例模式
References:
    [Python单例模式(Singleton)的N种实现 - 知乎](https://zhuanlan.zhihu.com/p/37534850)
"""
import os
import sys
import json
import time
import doctest
import functools

from typing import *
from pathlib import Path
from itertools import islice
from collections import defaultdict


class singleton:  # noqa
    """
    Notes:
        基于装饰器的单例可能会导致 IDE 的提示功能失效；
        一个解决办法是使用 type hint；

    Examples:
        >>> @singleton
        ... class Demo:
        ...     pass
        >>> d1: Demo = Demo()  # 如果不使用 type hint，可能会导致 IDE 的提示功能失效；
        >>> d2 = Demo()
        >>> assert d1 is d2
    """
    _instance: ClassVar[Dict[Type, Any]] = dict()

    def __init__(self, cls):
        functools.update_wrapper(self, cls)
        self._cls = cls

    def __call__(self, *args, **kwargs):
        if self._cls not in self._instance:
            self._instance[self._cls] = self._cls(*args, **kwargs)
        return self._instance[self._cls]


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

    def _test_base(self):  # noqa
        """"""

        @singleton
        class Demo:
            b: int = 10

            def __init__(self, a):
                self.a = a

        d1 = Demo(1)
        d2 = Demo(1)
        assert d1 is d2


if __name__ == '__main__':
    """"""
    __Test()
