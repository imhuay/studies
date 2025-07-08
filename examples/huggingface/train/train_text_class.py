#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Time:
    2022-08-18 20:21
Author:
    huayang (imhuay@163.com)
Subject:
    train_text_class
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

from transformers.trainer import Trainer



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

    def _test_xxx(self):  # noqa
        """"""
        pass


if __name__ == '__main__':
    """"""
    __Test()
