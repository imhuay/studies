#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Time: 2022-06-10 3:31 下午

Author: huayang

Subject:

"""
import os  # noqa
import doctest  # noqa

# from collections import defaultdict
# from itertools import islice
# from pathlib import Path
# from typing import *

# from tqdm import tqdm

from dataclasses import dataclass, fields, field, Field


class Demo:
    a: int = 1
    b = 2

    def __init__(self):
        self.c = 3



if __name__ == '__main__':
    """"""
    doctest.testmod()

    d = Demo()
    print(d.__dir__())
    print(d.__dict__)
    print(d.__annotations__)

