#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Time:
    2021-08-31 5:51 下午

Author:
    huayang

Subject:
    序列化、反序列化
"""
import base64
import pickle
import doctest


def obj_to_str(obj, encoding='utf8') -> str:
    """
    Examples:
        >>> d = dict(a=1, b=2)
        >>> assert isinstance(obj_to_str(d), str)
    """
    b = pickle.dumps(obj)
    return bytes_to_str(b, encoding=encoding)


def str_to_obj(s: str, encoding='utf8'):
    """
    Examples:
        >>> d = dict(a=1, b=2)
        >>> s = obj_to_str(d)
        >>> o = str_to_obj(s)
        >>> assert d is not o and d == o
    """
    data = str_to_bytes(s, encoding=encoding)
    return pickle.loads(data)


def bytes_to_str(b: bytes, encoding='utf8') -> str:
    return base64.b64encode(b).decode(encoding)


def str_to_bytes(s: str, encoding='utf8') -> bytes:
    return base64.b64decode(s.encode(encoding))


def file_to_str(file_path: str, encoding='utf8') -> str:
    with open(file_path, 'rb') as fp:
        return bytes_to_str(fp.read(), encoding=encoding)


def str_to_file(s: str, file_path: str, encoding='utf8') -> None:
    with open(file_path, 'wb') as fp:
        fp.write(str_to_bytes(s, encoding))


def _test():
    """"""
    doctest.testmod()

    def _test_serialize():
        """ 序列化、反序列化 """
        test_file = r'_test_data/pok.jpg'
        test_file_cp = r'_out/pok_cp.jpg'

        # bytes to str
        b = open(test_file, 'rb').read()
        s = bytes_to_str(b)
        assert s[:10] == '/9j/4AAQSk'

        # str to bytes
        b2 = str_to_bytes(s)
        assert b == b2

        # file to str
        s2 = file_to_str(test_file)
        assert s == s2

        # str to file
        str_to_file(s, test_file_cp)
        assert open(test_file, 'rb').read() == open(test_file_cp, 'rb').read()

    _test_serialize()


if __name__ == '__main__':
    """"""
    _test()
