#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Time: 2022-06-05 12:43 上午

Author: huayang

Subject:

"""
import os  # noqa
import doctest  # noqa


# from collections import defaultdict
# from itertools import islice
# from pathlib import Path
from typing import *

# from tqdm import tqdm


import openpyxl as xls


class XLSHelper:
    """@Work Utils
    Excel 文件加载（基于 openpyxl）

    Examples:
        >>> fp = r'./_test_data/test.xlsx'
        >>> xh = XLSHelper(fp)
        >>> xh.get_data_from('Sheet2')
        [['S1', 'S2', 'S3'], ['a', 'b', 'c'], ['aa', 'bb', 'cc']]
        >>> type(xh.workbook)
        <class 'openpyxl.workbook.workbook.Workbook'>
        >>> list(xh.sheet_names)
        ['Sheet1', 'Sheet2']
        >>> xh.sheets['Sheet1']
        [['H1', 'H2', 'H3'], [1, 2, 3], [11, 22, 33]]
        >>> xh.sheets['Sheet2']
        [['S1', 'S2', 'S3'], ['a', 'b', 'c'], ['aa', 'bb', 'cc']]
        >>> xh.first_sheet
        [['H1', 'H2', 'H3'], [1, 2, 3], [11, 22, 33]]
        >>> xh.active_sheet
        [['S1', 'S2', 'S3'], ['a', 'b', 'c'], ['aa', 'bb', 'cc']]
    """
    _sheets: Dict[str, List] = None
    _first_sheet: List = None  # 打开 Excel 排在第一个的 sheet
    _active_sheet: List = None  # 打开 Excel 时默认展示的 sheet

    def __init__(self, file_path, *args, **kwargs):
        """"""
        self.file_path = file_path
        self.workbook = xls.load_workbook(file_path, *args, **kwargs)
        self.sheet_names = [sheet.title for sheet in self.workbook]

    @property
    def sheets(self):
        if self._sheets is None:
            self._load_sheets()
        return self._sheets

    @property
    def first_sheet(self):
        if self._first_sheet is None:
            self._load_first_sheet()
        return self._first_sheet

    @property
    def active_sheet(self):
        if self._active_sheet is None:
            self._load_active_sheet()
        return self._active_sheet

    def _load_sheets(self):
        """"""
        self._sheets = {sheet.title: self.get_data_from_sheet(sheet) for sheet in self.workbook}

    def _load_first_sheet(self):
        """"""
        self._first_sheet = self.get_data_from_sheet(next(iter(self.workbook)))

    def _load_active_sheet(self):
        """"""
        self._active_sheet = self.get_data_from_sheet(self.workbook.active)

    def get_data_from(self, sheet_name: str):
        """"""
        return self.sheets[sheet_name]

    @staticmethod
    def get_data_from_sheet(sheet):
        """"""
        return [[item.value for item in row] for row in sheet]


if __name__ == '__main__':
    """"""
    doctest.testmod()
