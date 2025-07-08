#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Time: 2021-11-03 1:32 下午

Author: huayang

Subject:

"""
import doctest
from huaytools_local.pytorch._todo.nn.transformer import _transformer


def _test():
    """"""
    doctest.testmod(_transformer)  # noqa


if __name__ == '__main__':
    """"""
    _test()
