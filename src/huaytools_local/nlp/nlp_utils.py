#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Time:
    2022-08-05 11:53
Author:
    huayang (imhuay@163.com)
Subject:
    nlp_utils
"""
import os
import re
import sys
import json
import time
import doctest

from typing import *
from pathlib import Path
from itertools import islice
from collections import defaultdict


class NLPUtils:

    @staticmethod
    def n_gram_split(seq: Sequence,
                     n: Union[int, List[int]] = 3,
                     split_fn: Callable = None,
                     filter_fn: Callable = lambda x: x) -> Dict[int, List[Tuple]]:
        """
        N-Gram Split

        Examples:
            >>> ss = list('abc')
            >>> NLPUtils.n_gram_split(ss, 2)
            defaultdict(<class 'list'>, {1: [('a',), ('b',), ('c',)], 2: [('a', 'b'), ('b', 'c')]})
            >>> ss = [1, 2, 3]
            >>> NLPUtils.n_gram_split(ss, [2, 3])
            defaultdict(<class 'list'>, {2: [(1, 2), (2, 3)], 3: [(1, 2, 3)]})
            >>> ss = 'a  b c '  # use default split_fn and filter_fn
            >>> NLPUtils.n_gram_split(ss, 2, filter_fn=lambda x: x not in 'bd')
            defaultdict(<class 'list'>, {1: [('a',), ('c',)], 2: [('a', 'c')]})
            >>> ss = 'a,b|c,'  # use special split_fn
            >>> NLPUtils.n_gram_split(ss, [2, 3], split_fn=re.compile(r'[^a-z]').split)
            defaultdict(<class 'list'>, {2: [('a', 'b'), ('b', 'c')], 3: [('a', 'b', 'c')]})

        Args:
            seq:
            n:
            split_fn:
                seq = split_fn(seq)
                default split_fn=str.split if isinstance(seq, str) else None
            filter_fn:
                seq = list(filter(filter_fn, seq))
                default filter_fn=lambda x: x, it means remove empty object, such as None, '', [], {}, () etc.

        Returns:

        """
        if isinstance(n, int):
            n = list(range(1, n + 1))

        if isinstance(seq, str) and split_fn is None:
            split_fn = str.split

        if split_fn is not None:
            seq = split_fn(seq)

        seq = list(filter(filter_fn, seq))

        ret = defaultdict(list)
        for w in n:
            for i in range(len(seq) + 1 - w):
                gram = tuple(seq[i: i + w])
                ret[w].append(gram)

        return ret


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
