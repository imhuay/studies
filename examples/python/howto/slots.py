#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Time:
    2022-08-19 17:52
Author:
    huayang (imhuay@163.com)
Subject:
    slots
"""
import os
import sys
import json
import time
import doctest

from howto_typing import *
from pathlib import Path
from itertools import islice
from collections import defaultdict


class A:
    __slots__ = ('a',)

    def foo(self):
        """"""


class B:
    """"""


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

    def _test_Foo(self):  # noqa
        """"""
        a = A()
        assert '__dict__' not in dir(a)
        a.a = 1
        try:
            a.b = 2  # err
        except AttributeError as e:
            print(e)

        b = B()
        assert '__dict__' in dir(b) and '__slots__' not in dir(b)


if __name__ == '__main__':
    """"""
    __Test()
