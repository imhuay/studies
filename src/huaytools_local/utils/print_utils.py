#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Time:
    2022-08-03 16:45
Author:
    HuaYang (imhuay@163.com)
Subject:
    Print Utils
"""
import os
import sys
import json
import time

from typing import *
from pathlib import Path
from collections import defaultdict

COLOR = BACKCOLOR = Literal['black', 'red', 'green', 'yellow', 'blue', 'white', 'gray']
# https://en.wikipedia.org/wiki/ANSI_escape_code#Colors
COLOR_MAPPING = {
    'black': 30,
    'red': 31,
    'green': 32,
    'yellow': 33,
    'blue': 34,
    'white': 37,
    'gray': 90,
}
MODE = Literal['normal', 'bold', 'light', 'italic', 'underline', 'reverse', 'deleted', 'bold_underline']
# https://en.wikipedia.org/wiki/ANSI_escape_code#SGR_(Select_Graphic_Rendition)_parameters
BACKCOLOR_MAPPING = {
    'black': 40,
    'red': 41,
    'green': 42,
    'yellow': 43,
    'blue': 44,
    'white': 47,
    'gray': 100,
}
MODE_MAPPING = {
    'normal': 0,
    'bold': 1,
    'light': 2,
    'italic': 3,
    'underline': 4,
    'reverse': 7,
    'deleted': 9,
    'bold_underline': 21,
}
SUFFIX = '\x1b[0m'  # \033[0m


class PrintUtils:
    """"""

    @staticmethod
    def cprint(*args,
               mode: Union[int, MODE] = 'normal',
               color: Union[int, COLOR] = 'red',
               backcolor: Union[int, BACKCOLOR] = None,
               **kwargs):
        """
        彩色打印
            基本格式：\x1b[显示模式;前景色;背景色m{text}\x1b[0m
            示例：print("\x1b[1;31;47m{}\x1b[0m".format(123))  # 加粗，红字，白底
            更多显示模式和颜色 ID 见：
                - https://en.wikipedia.org/wiki/ANSI_escape_code#SGR_(Select_Graphic_Rendition)_parameters
                - https://en.wikipedia.org/wiki/ANSI_escape_code#Colors

        Args:
            *args:
            mode: 显式模式
            color: 前景色
            backcolor: 背景色
            **kwargs:

        References:
            - [Python：print显示颜色 - 博客园](https://www.cnblogs.com/hanfe1/p/10664942.html)
            - https://stackoverflow.com/questions/287871/how-do-i-print-colored-text-to-the-terminal
        """
        prefix = PrintUtils._get_prefix(mode, color, backcolor)

        if len(args) == 1:
            args = (f'{prefix}{args[0]}{SUFFIX}',)
        else:
            args = (f'{prefix}{args[0]}',) + args[1:-1] + (f'{args[-1]}{SUFFIX}',)
        print(*args, **kwargs)

    @staticmethod
    def _get_prefix(mode, color, backcolor):
        prefix = '\x1b['  # \033[
        if isinstance(color, str):
            color = COLOR_MAPPING[color]
        if mode is not None:
            if isinstance(mode, str):
                mode = MODE_MAPPING[mode]
            prefix += f'{mode};'
        prefix += f'{color}'
        if backcolor is not None:
            if isinstance(backcolor, str):
                backcolor = BACKCOLOR_MAPPING[backcolor]
            prefix += f';{backcolor}'
        prefix += 'm'
        return prefix

    @staticmethod
    def color(src, *,
              mode: Union[int, MODE] = 'normal',
              color: Union[int, COLOR] = 'red',
              backcolor: Union[int, BACKCOLOR] = None):
        prefix = PrintUtils._get_prefix(mode, color, backcolor)
        return f'{prefix}{src}{SUFFIX}'

    @staticmethod
    def red(src):
        return PrintUtils.color(src, color='red')

    @staticmethod
    def yellow(src):
        return PrintUtils.color(src, color='yellow')

    @staticmethod
    def green(src):
        return PrintUtils.color(src, color='green')

    @staticmethod
    def blue(src):
        return PrintUtils.color(src, color='blue')

    @staticmethod
    def black(src):
        return PrintUtils.color(src, color='black')

    @staticmethod
    def white(src):
        return PrintUtils.color(src, color='white')


cprint = PrintUtils.cprint


class __TestWrapper:
    """"""

    def __init__(self):
        """"""
        for k, v in self.__class__.__dict__.items():
            if k.startswith('_test') and isinstance(v, Callable):
                print(f'=== Start "{k}" {{')
                start = time.time()
                v(self)
                print(f'}} End "{k}" - Spend {time.time() - start:f}s===\n')

    def _test_doctest(self):  # noqa
        """"""
        import doctest
        doctest.testmod()

    def _test_base(self):  # noqa
        """"""
        cprint(1, '2', [3, 4], color='black', backcolor='white')
        cprint(1, '2', [3, 4])  # default red
        cprint(1, '2', [3, 4], color='green')
        cprint(1, '2', [3, 4], color='yellow')
        cprint(1, '2', [3, 4], color='blue')
        cprint(1, '2', [3, 4], color='white')
        cprint(1, '2', [3, 4], color='gray')
        cprint(1, '2', [3, 4], mode=7)
        cprint(1, '2', [3, 4], mode=9)
        cprint(1, '2', [3, 4], mode=4)
        cprint(1, '2', [3, 4], mode='bold_underline')

    def _test_color(self):  # noqa
        print(f'Test {PrintUtils.red("test")} {PrintUtils.color("test", color="yellow")}')


if __name__ == '__main__':
    """"""
    __TestWrapper()
