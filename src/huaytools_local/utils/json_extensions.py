#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Time:
    2021-06-24 12:39 上午

Author: huayang

Subject: 一些自定义的 json Encoder 或 Decoder
"""

import json
import doctest

from typing import Iterator
from _ctypes import PyObj_FromPtr


class NoIndentJSONEncoder(json.JSONEncoder):
    """
    对指定的对象不应用缩进

    注意：
        使用该 Json 解释器会显著降低写入速度，因此只限于小文件的写入；读取速度不受影响

    Examples:
        # 使用方法：将不想缩进的对象用 `NoIndentJSONEncoder.wrap` 包裹；
        >>> o = dict(a=1, b=NoIndentJSONEncoder.wrap([1, 2, 3]))
        >>> s = json.dumps(o, indent=4, cls=NoIndentJSONEncoder)
        >>> print(s)  # 注意 "b" 的 列表没有展开缩进
        {
            "a": 1,
            "b": [1, 2, 3]
        }
    """

    FORMAT_SPEC = '@@{}@@'

    class Value(object):
        """ Value wrapper. """

        def __init__(self, value):
            self.value = value

    def __init__(self, *args, **kwargs):
        super(NoIndentJSONEncoder, self).__init__(*args, **kwargs)
        self.kwargs = kwargs
        del self.kwargs['indent']
        # self._replacement_map = {}  # 缓存 id(obj) -> obj
        self._no_indent_obj_ids = set()  # 使用 PyObj_FromPtr，保存 id(obj) 即可

    def default(self, o):
        if isinstance(o, NoIndentJSONEncoder.Value):
            # self._replacement_map[id(o)] = json.dumps(o.value, **self.kwargs)
            self._no_indent_obj_ids.add(id(o))
            return self.FORMAT_SPEC.format(id(o))
        else:
            return super(NoIndentJSONEncoder, self).default(o)

    def encode(self, o) -> str:
        """for json.dumps"""
        result = super(NoIndentJSONEncoder, self).encode(o)
        return self._replace(result)

    def iterencode(self, o, _one_shot=False) -> Iterator[str]:
        """for json.dump"""
        iterator = super().iterencode(o, _one_shot)
        for it in iterator:
            yield self._replace(it)

    def _replace(self, s):
        """"""
        for oid in self._no_indent_obj_ids:
            tmp_str = json.dumps(PyObj_FromPtr(oid).value, **self.kwargs)
            s = s.replace('"{}"'.format(self.FORMAT_SPEC.format(oid)), tmp_str)
        return s

    @staticmethod
    def wrap(v):
        return NoIndentJSONEncoder.Value(v)


class AnyJSONEncoder(json.JSONEncoder):
    """ 支持任意对象的 Encoder，如果是非 json 默认支持对象，会转为二进制字符串；
        还原时需配合 AnyDecoder 一起使用

    Examples:
        >>> from datetime import datetime
        >>> o = dict(a=1, b=datetime(2021, 1, 1, 0, 0), c=dict(d=datetime(2012, 1, 1, 0, 0)))  # datetime 不是 json 支持的对象
        >>> s = json.dumps(o, cls=AnyJSONEncoder)
        >>> print(s[:100])  # 省略一部分输出
        {"a": 1, "b": "datetime.datetime(2021, 1, 1, 0, 0)__@AnyEncoder@__gASVKgAAAAAAAACMCGRhdGV0aW1llIwIZG
        >>> x = json.loads(s, cls=AnyJSONDecoder)
        >>> x
        {'a': 1, 'b': datetime.datetime(2021, 1, 1, 0, 0), 'c': {'d': datetime.datetime(2012, 1, 1, 0, 0)}}
        >>> assert o is not x and o == x  # o 和 x 不是同一个对象，但值是相同的
    """

    FLAG = '__@AnyEncoder@__'

    def default(self, o):
        from huaytools_local.utils.serialize_utils import obj_to_str

        try:
            return super(AnyJSONEncoder, self).default(o)
        except:  # noqa
            return repr(o) + AnyJSONEncoder.FLAG + obj_to_str(o)


class AnyJSONDecoder(json.JSONDecoder):
    """"""

    @staticmethod
    def scan(o):
        """ 递归遍历 o 中的对象，如果发现 AnyEncoder 标志，则对其还原 """
        from huaytools_local.utils.serialize_utils import str_to_obj

        if isinstance(o, str):
            if o.find(AnyJSONEncoder.FLAG) != -1:  # 如果字符串中存在 AnyEncoder 标识符，说明是个特殊对象
                o = str_to_obj(o.split(AnyJSONEncoder.FLAG)[-1])  # 提取二进制字符串并转化为 python 对象
        elif isinstance(o, list):
            for i, it in enumerate(o):
                o[i] = AnyJSONDecoder.scan(it)  # 递归调用
        elif isinstance(o, dict):
            for k, v in o.items():
                o[k] = AnyJSONDecoder.scan(v)  # 递归调用

        return o

    def decode(self, s: str, **kwargs):
        """"""
        obj = super(AnyJSONDecoder, self).decode(s)
        obj = AnyJSONDecoder.scan(obj)
        return obj


if __name__ == '__main__':
    doctest.testmod()
