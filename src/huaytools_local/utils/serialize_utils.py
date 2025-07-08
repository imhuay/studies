#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Time:
    2022-08-03 17:50
Author:
    HuaYang (imhuay@163.com)
Subject:
    Serialize Utils
"""
import os
import sys
import json
import time
import base64
import pickle

from typing import *
from pathlib import Path
from collections import defaultdict


class SerializeUtils:
    """"""

    @staticmethod
    def obj_to_str(obj, encoding='utf8') -> str:
        """
        Examples:
            >>> d = dict(a=1, b=2)
            >>> assert isinstance(SerializeUtils.obj_to_str(d), str)
        """
        b = pickle.dumps(obj)
        return SerializeUtils.bytes_to_str(b, encoding=encoding)

    @staticmethod
    def str_to_obj(s: str, encoding='utf8') -> Any:
        """
        Examples:
            >>> d = dict(a=1, b=2)
            >>> c = SerializeUtils.obj_to_str(d)
            >>> o = SerializeUtils.str_to_obj(c)
            >>> assert d is not o and d == o
        """
        data = SerializeUtils.str_to_bytes(s, encoding=encoding)
        return pickle.loads(data)

    @staticmethod
    def bytes_to_str(b: bytes, encoding='utf8') -> str:
        return base64.b64encode(b).decode(encoding)

    @staticmethod
    def str_to_bytes(s: str, encoding='utf8') -> bytes:
        return base64.b64decode(s.encode(encoding))

    @staticmethod
    def file_to_str(file_path: str, encoding='utf8') -> str:
        with open(file_path, 'rb') as fp:
            return SerializeUtils.bytes_to_str(fp.read(), encoding=encoding)

    @staticmethod
    def str_to_file(s: str, file_path: str, encoding='utf8') -> NoReturn:
        with open(file_path, 'wb') as fp:
            fp.write(SerializeUtils.str_to_bytes(s, encoding))


obj_to_str = SerializeUtils.obj_to_str
str_to_obj = SerializeUtils.str_to_obj
bytes_to_str = SerializeUtils.bytes_to_str
str_to_bytes = SerializeUtils.str_to_bytes
file_to_str = SerializeUtils.file_to_str
str_to_file = SerializeUtils.str_to_file


class __RunWrapper:
    """"""

    def __init__(self):
        """"""
        for k, v in self.__class__.__dict__.items():
            if k.startswith('demo') and isinstance(v, Callable):
                print(f'=== Start "{k}" {{')
                start = time.time()
                v(self)
                print(f'}} End "{k}" - Spend {time.time() - start:f}s===\n')

    def demo_doctest(self):  # noqa
        """"""
        import doctest
        doctest.testmod()

    def demo_xxx(self):  # noqa
        """"""
        test_file = r'_test_data/pok.jpg'
        test_file_cp = r'_test_data/pok_cp.jpg'

        # bytes to str
        b = open(test_file, 'rb').read()
        s = SerializeUtils.bytes_to_str(b)
        assert s[:10] == '/9j/4AAQSk'

        # str to bytes
        b2 = SerializeUtils.str_to_bytes(s)
        assert b == b2

        # file to str
        s2 = SerializeUtils.file_to_str(test_file)
        assert s == s2

        # str to file
        SerializeUtils.str_to_file(s, test_file_cp)
        assert open(test_file, 'rb').read() == open(test_file_cp, 'rb').read()


if __name__ == '__main__':
    """"""
    __RunWrapper()
