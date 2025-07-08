#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Time:
    2022-07-28 15:44
Author:
    HuaYang(imhuay@163.com)
Subject:
    Utils for CSV files.
"""
import os
import sys
import json
import doctest

from typing import *
from pathlib import Path
from itertools import islice
from collections import defaultdict

import csv


class _default_dialect(csv.Dialect):  # noqa
    """
    References:
        https://docs.python.org/zh-cn/3/library/csv.html#dialects-and-formatting-parameters
    """
    delimiter = ','  # 定界符
    quotechar = '"'  # 引号，用于包裹字段，当字段值中含有特殊字符时才会生效，也可以通过设置 quoting 来影响
    escapechar = None  # 转义符，None 表示禁止转义，
    doublequote = True  # 如果字段中出现引号，用连续的两个引号替换；若为 False，则必须设置转义符
    skipinitialspace = False  # 是否忽略 delimiter 之后的空格
    lineterminator = '\n'  # 换行符，仅
    quoting = csv.QUOTE_ALL  # 控制 writer 何时生成引号，以及 reader 何时识别引号
    strict = True  # 严格模式，在输入错误的 CSV 时抛出 Error 异常


class CSVUtils:
    """
    Notes:
        完整的 formats 选项，见 csv.Dialect；
        其中部分是对 reader 生效的，部分是对 writer 生效的

    """
    default_dialect: ClassVar[Type[csv.Dialect]] = _default_dialect

    @staticmethod
    def infer_dialect(fp, sample_size=1024, candidate_delimiters=None) -> Type[csv.Dialect]:
        """"""
        with open(fp, newline='') as cf:
            return csv.Sniffer().sniff(cf.read(sample_size), candidate_delimiters)

    @staticmethod
    def load(file_path: Union[str, Path],
             *, return_dict=False, encoding='utf8', dialect: Type[csv.Dialect] = None,
             delimiter: str = None, quotechar: str = None, escapechar: str = None,
             doublequote: bool = None, quoting: int = None, strict: bool = None, **formats):
        """"""
        dialect = CSVUtils._get_dialect(dialect, delimiter, quotechar, escapechar,
                                        doublequote, quoting, strict, **formats)
        get_reader = csv.DictReader if return_dict else csv.reader
        with open(file_path, encoding=encoding, newline='') as lns:
            reader = get_reader(lns, dialect=dialect)
            for row in reader:
                yield row

    read = load

    @staticmethod
    def save(f: Union[str, Path], rows: Sequence[Union[List, Dict]],
             *, fieldnames: List[str] = None, encoding='utf8', dialect: Type[csv.Dialect] = None,
             delimiter: str = None, quotechar: str = None, escapechar: str = None,
             doublequote: bool = None, quoting: int = None, strict: bool = None, **formats):
        """"""
        dialect = CSVUtils._get_dialect(dialect, delimiter, quotechar, escapechar,
                                        doublequote, quoting, strict, **formats)
        first_row = rows[0]
        with open(f, 'w', encoding=encoding, newline='') as fw:
            if isinstance(first_row, List):
                writer = csv.writer(fw, dialect=dialect)
            else:
                if fieldnames is None:
                    fieldnames = list(first_row.keys())
                writer = csv.DictWriter(fw, fieldnames, dialect=dialect)
            writer.writerows(rows)

    write = save

    @staticmethod
    def _get_dialect(dialect: Type[csv.Dialect] = None,
                     delimiter: str = None, quotechar: str = None, escapechar: str = None,
                     doublequote: bool = None, quoting: int = None, strict: bool = None, **formats):
        """"""
        def _set_attr(attr, value):
            if hasattr(dialect, attr):
                setattr(dialect, attr, value or getattr(dialect, attr))
            else:
                setattr(dialect, attr, value)

        dialect = dialect or CSVUtils.default_dialect
        _set_attr('delimiter', delimiter)
        _set_attr('quotechar', quotechar)
        _set_attr('escapechar', escapechar)
        _set_attr('doublequote', doublequote)
        _set_attr('quoting', quoting)
        _set_attr('strict', strict)
        for k, v in formats.items():
            setattr(dialect, k, v)
        return dialect


class __DoctestWrapper:
    """"""

    def __init__(self):
        """"""
        doctest.testmod()

        for k, v in self.__class__.__dict__.items():
            if k.startswith('demo') and isinstance(v, Callable):
                v(self)

    def demo_base(self):  # noqa
        """"""
        fp = r'./_test_data/test.csv'
        rows = CSVUtils.load(fp, return_dict=True, skipinitialspace=True)
        # print(list(rows))
        for r in rows:
            print(r)

    def demo_write(self):  # noqa
        """"""
        test_rows = [
            {'a': 1, 'b': 2, 'c': 1},
            {'a': 11, 'b': 21, 'c': 11},
            {'a': 13, 'b': 22, 'c': 12},
        ]

        f = './_test_data/test_w.csv'
        CSVUtils.save(f, test_rows)
        dialect = CSVUtils.infer_dialect(f)
        print(dialect.delimiter)
        rows = CSVUtils.load(f, dialect=dialect)
        print(list(rows))


if __name__ == '__main__':
    """"""
    __DoctestWrapper()
