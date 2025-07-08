#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Time:
    2023-02-22 20:01
Author:
    imhuay (imhuay@163.com)
Subject:
    udf_template
"""
from __future__ import annotations

import os
import json
import sys
import platform
import logging
import argparse

from typing import *

# from pathlib import Path
# from collections import defaultdict


test_data = [
    'a\tb\tc\n',
]

_DEFAULT_LOCAL_NODE_NAME = 'xxx'
_MODE_MAP = 'map'
_MODE_REDUCE = 'reduce'


class Processor:
    """"""
    _NULL = r'\N'
    _row_sep = '\t'

    def __init__(self):
        """"""
        # 用于判断是否在本地运行, 实际使用时替换为本地 `platform.node()` 的运行结果
        assert _DEFAULT_LOCAL_NODE_NAME != 'xxx', \
            'Please use the result of `platform.node()` to set `_default_local_node_name`.'
        self._is_run_local = platform.node() == _DEFAULT_LOCAL_NODE_NAME

        if self._is_run_local:
            self._src = test_data
        else:
            self._src = sys.stdin

        self._parse_args()
        # self._run()

    def _process_row(self, row) -> Union[list, list[list]]:
        """"""
        raise NotImplemented

        # # 1. 读取每行的数据
        # f1, f2 = row[:2]

        # # 2. 数据处理

        # # 2.1 推荐把结果包装到一个 json 中, 在结果表中使用 get_json_object 或者 json_tuple 读取结果
        # ext_info = {}
        # ext_info_str = json.dumps(ext_info)

        # # 3. 返回结果, 如果 --multiple_row, 则返回 list[list], 表示每行输入会输出多行数据到结果表
        # if self._args.multiple_row:
        #     return [[o01, o02, ...], [o11, o12, ...], ...]
        # else:
        #     return row + [ext_info_str]

        # # 3.1 如果是 map_reduce 模式, 不需要返回结果, 在处理完所有行之后在处理相关统计结果, 类似 GROUP BY & MAX 的逻辑
        # # map_reduce 模式的一般做法是建立一个全局 k-v 对象, 在处理完全部数据后再把结果输出

    def _output_r(self):
        """"""
        if self._args.run_mode == _MODE_REDUCE:
            raise NotImplemented

    def _output_m(self, ret):
        if ret == self._NULL or not ret:
            return
        if self._args.multiple_row:
            for row in ret:
                print(self._row_sep.join([str(it) for it in row]))
        else:
            print(self._row_sep.join([str(it) for it in ret]))

    def _parse_args(self):
        """"""
        parser = argparse.ArgumentParser()
        parser.add_argument('--multiple_row', action='store_true')  # if input one row and output multiple rows.
        parser.add_argument('--run_mode', type=str, default=_MODE_MAP,
                            choices=[_MODE_MAP, _MODE_REDUCE])  # map reduce mode
        # parser.add_argument('--map_reduce', action='store_true')  # map reduce mode
        # self._parser.add_argument('--a', type=str, default='123')
        # self._parser.add_argument('--b', type=int, default=123)
        self._args = parser.parse_args(sys.argv[1:])

    def run(self):
        """"""
        for ln in self._src:
            try:
                row = ln.strip('\n').split(self._row_sep)
                ret = self._process_row(row)
                if self._args.run_mode == _MODE_MAP:
                    self._output_m(ret)
            except:  # noqa
                logging.error(ln)

        # 如果是 map_reduce 模式, 需要在处理完所有行之后输出
        if self._args.run_mode == _MODE_REDUCE:
            self._output_r()


if __name__ == '__main__':
    """"""
    Processor().run()
