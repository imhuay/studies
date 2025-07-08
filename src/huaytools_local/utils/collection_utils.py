#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Time:
    2022-08-26 11:44
Author:
    huayang (imhuay@163.com)
Subject:
    collection_utils
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


class CollectionUtils:
    """"""

    @staticmethod
    def distinct_append(ls: List, elem) -> NoReturn:
        """
        Examples:
            >>> _ls = [1,2,3]
            >>> CollectionUtils.distinct_append(_ls, 4); _ls
            [1, 2, 3, 4]
            >>> CollectionUtils.distinct_append(_ls, 4); _ls
            [1, 2, 3, 4]
        """
        if elem not in ls:
            ls.append(elem)

    @staticmethod
    def flat_list(ls: List[Iterable]) -> List:
        """
        Examples:
            >>> _l = [[1,2,3], range(4, 7), (i for i in range(7, 10))]  # noqa
            >>> CollectionUtils.flat_list(_l)
            [1, 2, 3, 4, 5, 6, 7, 8, 9]
        """
        import itertools
        return list(itertools.chain.from_iterable(ls))

    @staticmethod
    def remove_duplicates(src: Sequence[Hashable], ordered=True) -> List:
        """
        Examples:
            >>> ls = [1,2,3,3,2,4,2,3,5]
            >>> CollectionUtils.remove_duplicates(ls)
            [1, 2, 3, 4, 5]
        """
        src_distinct = list(set(src))

        if ordered:
            src_distinct.sort(key=src.index)

        return src_distinct


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
