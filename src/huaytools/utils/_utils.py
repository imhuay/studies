"""
Time:
    2025-07-08 19:07
Author:
    huayang (imhuay@163.com)
Subject:
    _utils
License:
    MIT License
"""
from __future__ import annotations

import inspect
import logging
import os
import sys

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s@%(lineno)dL : %(message)s',
                    datefmt='%Y.%m.%d %H:%M:%S', level=logging.INFO)
"""
References: https://docs.python.org/zh-cn/3/library/logging.html#logrecord-attributes
"""


class PythonUtils:
    """"""

    @staticmethod
    def get_version() -> tuple:
        """"""
        return tuple(sys.version_info[:3])  # (3, 9, 13)

    @staticmethod
    def get_frame(stack_level: int = 0):
        """
        Examples:
            >>> def foo():
            ...     f = PythonUtils.get_frame()
            ...     return f.f_code.co_name
            >>> foo()
            'foo'
        """
        assert stack_level >= 0
        frame = inspect.currentframe()  # 获取当前 frame，即 `get_frame` 的 frame
        # for _ in range(stack_level + 1):  # 向上逐级回溯调用者的 frame，`+1` 表示跳过 get_frame 本身的调用
        #     frame = frame.f_back
        n_back = stack_level + 1
        while n_back > 0:
            if frame is not None:
                frame = frame.f_back
            else:
                raise ValueError(f'stack_level={stack_level} more than maximum.')

            n_back -= 1

        return frame

    @staticmethod
    def get_caller_name(stack_level: int = 1) -> str:
        """
        获取调用者的名字

        使用场景：
            假设 foo 内部调用了 get_caller_name，则 get_caller_name 默认（level=1）会返回调用了 foo 的对象名；
            如果调用 foo 的对象是一个方法/模块/类，则返回该相应的的方法名/模块名/类名；

        Args:
            stack_level: 回溯层级，默认为 1；

        Examples:
            >>> def foo():
            ...     name = PythonUtils.get_caller_name(0)  # name of who called `get_caller_name`
            ...     print(name)
            >>> foo()
            foo
            >>> def foo():
            ...     name = PythonUtils.get_caller_name()  # name of who called `foo`
            ...     print(name)
            >>> def bar():
            ...     foo()
            >>> bar()
            bar
            >>> def zoo():
            ...     foo()
            >>> zoo()
            zoo
        """
        assert stack_level >= 0
        frame = PythonUtils.get_frame(stack_level + 1)
        co_name = frame.f_code.co_name

        # 当调用方是一个模块，此时返回模块的文件名
        if co_name == '<module>':
            return os.path.basename(frame.f_code.co_filename)

        return co_name

    @staticmethod
    def get_lineno(stack_level: int = 0) -> int:
        """
        获取调用时行号

        Args:
            stack_level: 回溯层级

        Examples:
            # example1: default
            lno = get_lineno()  # this line
            print(lno)

            # example2: stack_level > 0
            def foo():
                return get_lineno(1)

            lno = foo()  # this line
            print(lno)
        """
        return PythonUtils.get_frame(stack_level + 1).f_lineno

    @staticmethod
    def get_annotation_names(obj: object) -> list[str]:
        return list(obj.__annotations__.keys())


def get_logger(name: str = None):
    """返回一个 logger"""
    return logging.getLogger(name or PythonUtils.get_caller_name())
