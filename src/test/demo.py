#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Time: 2022-06-05 12:58 上午

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


from huaytools.utils import get_print_json


class A:
    """"""


if __name__ == '__main__':
    """"""
    d = {'a': A()}
    print(get_print_json(d))
    doctest.testmod()
