#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Time: 2021-10-05 11:47 下午

Author: huayang

Subject:

"""
import re
import os
import sys
import json
import doctest

from typing import *
from collections import defaultdict


RE_MULTI_WHITE = re.compile(r'\s+')
'''匹配多个空白符'''

RE_MULTI_SPACE = re.compile(r' +')
'''匹配多个空格'''

RE_MULTI_LINE = re.compile(r'(\n\s*)+')
'''匹配多个换行符'''

RE_CH = re.compile(r'[\u4E00-\u9FA5]')
'''中文'''

RE_EN = re.compile(r'[a-zA-Z]')
'''英文'''

RE_NUMBER = re.compile(r'[0-9]')
'''数字'''


def _test():
    """"""
    doctest.testmod()


if __name__ == '__main__':
    """"""
    _test()

    r = RE_CH.search('as 中s')
    print(r)
