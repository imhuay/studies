#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Time:
    2022-08-06 16:46
Author:
    huayang (imhuay@163.com)
Subject:
    str_utils
"""
import re
import os
import sys
import json
import time
import doctest

from typing import *
from pathlib import Path
from itertools import islice
from collections import defaultdict


class StrUtils:
    """"""
    RE_INDENT = re.compile(r'^( *)(?=\S)', re.MULTILINE)

    @staticmethod
    def replace_tag_to_space(s: str, tab_size=4) -> str:
        """
        Examples:
            >>> StrUtils.replace_tag_to_space('a\\tbc\\tdef')
            'a   bc  def'
        """
        return s.expandtabs(tabsize=tab_size)  # default tabsize=8

    @staticmethod
    def insert_indent(s: str, indent: int = 4) -> str:
        """
        Add the given number of space characters to the beginning of
        every non-blank line in `s`, and return the result.

        References:
            doctest._indent

        Examples:
            >>> StrUtils.insert_indent("abc\\ndef")
            '    abc\\n    def'
        """
        # This regexp matches the start of non-blank lines:
        return re.sub('(?m)^(?!$)', indent * ' ', s)

    @staticmethod
    def min_indent(s: str) -> int:
        """
        Return the minimum indentation of any non-blank line in `s`

        References:
            doctest.DocTestParser._min_indent

        Examples:
            >>> StrUtils.min_indent(StrUtils.min_indent.__doc__)
            8
        """
        indents = [len(indent) for indent in StrUtils.RE_INDENT.findall(s)]
        if len(indents) > 0:
            return min(indents)
        else:
            return 0

    @staticmethod
    def remove_min_indent(s: str):
        """
        Examples
            >>> one_indent = ' ' * 4
            >>> _s = '''
            ...     def fun():
            ...         pass
            ... '''
            >>> _s = StrUtils.remove_min_indent(_s)
            >>> print(_s.strip())
            def fun():
                pass
        """
        m = StrUtils.min_indent(s)
        if m > 0:
            s = '\n'.join([line[m:] for line in s.split('\n')])
        return s


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

    def _test_insert_indent(self):  # noqa
        """"""


if __name__ == '__main__':
    """"""
    __Test()
