#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Time: 2021-09-24 4:38 下午

Author: huayang

Subject: 自定义字典

"""
import os
import json

import doctest

from typing import *
from dataclasses import dataclass, fields
from collections import OrderedDict

__all__ = [
    'ArrayDict',
    'ValueArrayDict',
    'BunchDict',
    'FieldBunchDict',
]


# class DefaultOrderedDict(defaultdict, OrderedDict):
#
#     def __init__(self, default_factory=None, *a, **kw):
#         for cls in DefaultOrderedDict.mro()[1:-2]:
#             cls.__init__(self, *a, **kw)
#
#         super(DefaultOrderedDict, self).__init__()


class ArrayDict(OrderedDict):
    """@Python 自定义数据结构
    数组字典，支持 slice

    Examples:
        >>> d = ArrayDict(a=1, b=2)
        >>> d
        ArrayDict([('a', 1), ('b', 2)])
        >>> d['a']
        1
        >>> d[1]
        ArrayDict([('b', 2)])
        >>> d['c'] = 3
        >>> d[0] = 100
        Traceback (most recent call last):
            ...
        TypeError: ArrayDict cannot use `int` as key.
        >>> d[1: 3]
        ArrayDict([('b', 2), ('c', 3)])
        >>> print(*d)
        a b c
        >>> d.setdefault('d', 4)
        4
        >>> print(d)
        ArrayDict([('a', 1), ('b', 2), ('c', 3), ('d', 4)])
        >>> d.pop('a')
        1
        >>> d.update({'b': 20, 'c': 30})
        >>> def f(**d): print(d)
        >>> f(**d)
        {'b': 20, 'c': 30, 'd': 4}

    """

    @property
    def tuple(self) -> Tuple[Any]:
        """
        Convert self to a tuple containing all the attributes/keys that are not ``None``.
        """
        return tuple(self.items())

    def __getitem__(self, key):
        """"""
        if isinstance(key, (int,)):
            return self.__class__.__call__([self.tuple[key]])
        elif isinstance(key, (slice,)):
            return self.__class__.__call__(list(self.tuple[key]))
        else:
            # return self[k]  # err: RecursionError
            # inner_dict = {k: v for (k, v) in self.items()}
            # return inner_dict[k]
            return super().__getitem__(key)

    def __setitem__(self, key, value):
        """"""
        if isinstance(key, (int,)):
            raise TypeError(f'{self.__class__.__name__} cannot use `{type(key).__name__}` as key.')
        else:
            super().__setitem__(key, value)


class ValueArrayDict(ArrayDict):
    """@Python 自定义数据结构
    数组字典，支持 slice，且操作 values

    Examples:
        >>> d = ValueArrayDict(a=1, b=2)
        >>> d
        ValueArrayDict([('a', 1), ('b', 2)])
        >>> assert d[1] == 2
        >>> d['c'] = 3
        >>> assert d[2] == 3
        >>> d[1:]
        (2, 3)
        >>> print(*d)  # 注意打印的是 values
        1 2 3
        >>> del d['a']
        >>> d.update({'a':10, 'b': 20})
        >>> d
        ValueArrayDict([('b', 20), ('c', 3), ('a', 10)])

    """

    @property
    def tuple(self) -> Tuple[Any]:
        """
        Convert self to a tuple containing all the attributes/keys that are not ``None``.
        """
        return tuple(self.values())

    def __getitem__(self, key):
        """"""
        if isinstance(key, (int, slice)):
            return self.tuple[key]
        else:
            # return self[k]  # err: RecursionError
            # inner_dict = {k: v for (k, v) in self.items()}
            # return inner_dict[k]
            return super().__getitem__(key)

    # def setdefault(self, *args, **kwargs):
    #     """ 不支持 setdefault 操作 """
    #     raise Exception(f"Cannot use ``setdefault`` on a {self.__class__.__name__} instance.")

    # def pop(self, *args, **kwargs):
    #     """ 不支持 pop 操作 """
    #     raise Exception(f"Cannot use ``pop`` on a {self.__class__.__name__} instance.")

    # def update(self, *args, **kwargs):
    #     """ 不支持 update 操作 """
    #     raise Exception(f"Cannot use ``update`` on a {self.__class__.__name__} instance.")

    def __iter__(self):
        """ dict 默认迭代的对象是 keys，重写使迭代 values

        Examples:
            >>> sd = ValueArrayDict(a=1, b=2)
            >>> # 没有重写 __iter__ 时：
            >>> # print(*sd)  # a b
            >>> # 重写 __iter__ 后：
            >>> print(*sd)
            1 2

        """
        return iter(self.tuple)


class BunchDict(Dict):
    """@Python 自定义数据结构
    基于 dict 实现 Bunch 模式

    Examples:
        # 直接使用
        >>> d = BunchDict(a=1, b=2)
        >>> d
        {'a': 1, 'b': 2}
        >>> d.c = 3
        >>> assert 'c' in d and d.c == 3
        >>> dir(d)
        ['a', 'b', 'c']
        >>> assert 'a' in d
        >>> del d.a
        >>> assert 'a' not in d
        >>> d.dict
        {'b': 2, 'c': 3}

        # 批量导入新配置
        >>> kwargs = {'d': 4, 'e': 5}
        >>> d.update(kwargs)
        >>> d.dict
        {'b': 2, 'c': 3, 'd': 4, 'e': 5}
        >>> d.e
        5

        # 从字典加载
        >>> x = {'d': 4, 'e': {'a': 1, 'b': 2, 'c': 3}}
        >>> y = BunchDict.from_dict(x)
        >>> y
        {'d': 4, 'e': {'a': 1, 'b': 2, 'c': 3}}

        # 预定义配置
        >>> class Config(BunchDict):
        ...     def __init__(self, **config_items):
        ...         from datetime import datetime
        ...         self.a = 1
        ...         self.b = 2
        ...         self.c = datetime(2012, 1, 1)  # 注意是一个特殊对象，默认 json 是不支持的
        ...         super().__init__(**config_items)
        >>> args = Config(b=20)
        >>> args.a = 10
        >>> args
        {'a': 10, 'b': 20, 'c': datetime.datetime(2012, 1, 1, 0, 0)}
        >>> args == args.dict
        True
        >>> # 添加默认中不存的配置项
        >>> args.d = 40
        >>> print(args.get_pretty_dict())  # 注意 'c' 保存成了特殊形式
        {
            "a": 10,
            "b": 20,
            "c": "datetime.datetime(2012, 1, 1, 0, 0)__@AnyEncoder@__gASVKgAAAAAAAACMCGRhdGV0aW1llIwIZGF0ZXRpbWWUk5...",
            "d": 40
        }

        # 保存/加载
        >>> fp = r'./-test/test_save_config.json'
        >>> os.makedirs(os.path.dirname(fp), exist_ok=True)
        >>> args.save(fp)  # 保存
        >>> x = Config.load(fp)  # 重新加载
        >>> assert x == args.dict
        >>> _ = os.system('rm -rf ./-test')

    References:
        - bunch（pip install bunch）
    """

    # 最简单实现 Bunch 模式的方法，可以不用重写 __setattr__ 等方法
    # def __init__(self, *args, **kwargs):
    #     super(BunchDict, self).__init__(*args, **kwargs)
    #     self.__dict__ = self

    def __dir__(self):
        """ 屏蔽其他属性或方法 """
        return self.keys()

    def __getattr__(self, key):
        """ 使 o.key 等价于 o[key] """
        try:
            return object.__getattribute__(self, key)
        except AttributeError:
            try:
                return self[key]
            except KeyError:
                raise AttributeError(key)

    def __setattr__(self, name, value):
        """ 使 o.name = value 等价于 o[name] = value """
        try:
            # Throws exception if not in prototype chain
            object.__getattribute__(self, name)
        except AttributeError:
            self[name] = value
        else:
            object.__setattr__(self, name, value)

    def __delattr__(self, key):
        """ 支持 del x.y """
        try:
            # Throws exception if not in prototype chain
            object.__getattribute__(self, key)
        except AttributeError:
            try:
                del self[key]
            except KeyError:
                raise AttributeError(key)
        else:
            object.__delattr__(self, key)

    @classmethod
    def from_dict(cls, d: dict):
        return _bunch(d, cls)

    @property
    def dict(self):
        """"""
        return dict(self)

    def get_pretty_dict(self, sort_keys=True, print_cls_name=False):
        """"""
        from huaytools.utils import AnyJSONEncoder
        pretty_dict = json.dumps(self.dict, cls=AnyJSONEncoder, indent=4, ensure_ascii=False, sort_keys=sort_keys)
        if print_cls_name:
            pretty_dict = f'{self.__class__.__name__}: {pretty_dict}'

        return pretty_dict

    # def __str__(self):
    #     """"""
    #     return str(self.dict)

    def save(self, fp: str, sort_keys=True):
        """ 保存配置到文件 """
        with open(fp, 'w', encoding='utf8') as fw:
            fw.write(self.get_pretty_dict(sort_keys=sort_keys))

    @classmethod
    def load(cls, fp: str):
        """"""
        from huaytools.utils import AnyJSONDecoder
        config_items = json.load(open(fp, encoding='utf8'), cls=AnyJSONDecoder)
        return cls(**config_items)


@dataclass()
class FieldBunchDict(BunchDict):
    """@Python 自定义数据结构
    基于 dataclass 的 BunchDict

    原来预定义的参数，需要写在 __init__ 中：
        ```
        class Args(BunchDict):
            def __init__(self):
                a = 1
                b = 2
        ```
    现在可以直接当作 dataclass 来写：
        ```
        @dataclass()
        class Args(BunchDict):
            a: int = 1
            b: int = 2
        ```

    Examples:
        # 预定义配置
        >>> @dataclass()
        ... class Config(FieldBunchDict):
        ...     from datetime import datetime
        ...     a: int = 1
        ...     b: int = 2
        ...     c: Any = datetime(2012, 1, 1)  # 注意是一个特殊对象，默认 json 是不支持的
        >>> args = Config(b=20)
        >>> args.a = 10
        >>> args
        Config(a=10, b=20, c=datetime.datetime(2012, 1, 1, 0, 0))
        >>> args.dict
        {'a': 1, 'b': 20, 'c': datetime.datetime(2012, 1, 1, 0, 0)}
        >>> args.d = 40  # 默认中没有的配置项（不推荐，建议都定义在继承类中，并设置默认值）
        Traceback (most recent call last):
            ...
        KeyError: '`d` not in fields. If it has to add new field, recommend to use `BunchDict`'

        # 保存/加载
        >>> fp = r'./-test/test_save_config.json'
        >>> os.makedirs(os.path.dirname(fp), exist_ok=True)
        >>> args.save(fp)  # 保存
        >>> x = Config.load(fp)  # 重新加载
        >>> assert x == args.dict
        >>> _ = os.system('rm -rf ./-test')

    """

    def __post_init__(self):
        """"""
        # 获取所有 field
        class_fields = fields(self)
        # 依次添加到 dict 中
        for f in class_fields:
            self[f.name] = getattr(self, f.name)

    def __setattr__(self, key, value):
        field_set = set(f.name for f in fields(self))
        if key not in field_set:
            raise KeyError(
                f'`{key}` not in fields. If it has to add new field, recommend to use `{BunchDict.__name__}`')
        else:
            super().__setattr__(key, value)


class BunchArrayDict(ArrayDict, BunchDict):
    """ 
    
    Examples:
        >>> d = BunchArrayDict(a=1, b=2)
        >>> isinstance(d, dict)
        True
        >>> print(d, d.a, d[1])
        BunchArrayDict([('a', 1), ('b', 2)]) 1 BunchArrayDict([('b', 2)])
        >>> d.a, d.b, d.c = 10, 20, 30
        >>> print(d, d[1:])
        BunchArrayDict([('a', 10), ('b', 20), ('c', 30)]) BunchArrayDict([('b', 20), ('c', 30)])
        >>> print(*d)
        a b c
        >>> dir(d)
        ['a', 'b', 'c']
        >>> assert 'a' in d
        >>> del d.a
        >>> assert 'a' not in d
        >>> getattr(d, 'a', 100)
        100

        # 测试嵌套
        >>> x = BunchArrayDict(d=40, e=d)
        >>> x
        BunchArrayDict([('d', 40), ('e', BunchArrayDict([('b', 20), ('c', 30)]))])
        >>> print(x.d, x.e.b)
        40 20

        >>> z = {'d': 4, 'e': {'a': 1, 'b': 2, 'c': 3}}
        >>> y = BunchArrayDict.from_dict(z)
        >>> y
        BunchArrayDict([('d', 4), ('e', BunchArrayDict([('a', 1), ('b', 2), ('c', 3)]))])
        >>> y.e.c
        3

    """


class BunchValueArrayDict(ValueArrayDict, BunchDict):
    """

    Examples:
        >>> d = BunchValueArrayDict(a=1, b=2)
        >>> isinstance(d, dict)
        True
        >>> print(d, d.a, d[1])
        BunchValueArrayDict([('a', 1), ('b', 2)]) 1 2
        >>> d.a, d.b, d.c = 10, 20, 30
        >>> print(d, d[2], d[1:])
        BunchValueArrayDict([('a', 10), ('b', 20), ('c', 30)]) 30 (20, 30)
        >>> print(*d)
        10 20 30
        >>> dir(d)
        ['a', 'b', 'c']
        >>> assert 'a' in d
        >>> del d.a
        >>> assert 'a' not in d
        >>> getattr(d, 'a', 100)
        100

        # 测试嵌套
        >>> x = BunchValueArrayDict(d=40, e=d)
        >>> x
        BunchValueArrayDict([('d', 40), ('e', BunchValueArrayDict([('b', 20), ('c', 30)]))])
        >>> print(x.d, x.e.b)
        40 20

        >>> z = {'d': 4, 'e': {'a': 1, 'b': 2, 'c': 3}}
        >>> y = BunchValueArrayDict.from_dict(z)
        >>> y
        BunchValueArrayDict([('d', 4), ('e', BunchValueArrayDict([('a', 1), ('b', 2), ('c', 3)]))])
        >>> y.e.c
        3

    """


@dataclass()
class ArrayFields(FieldBunchDict, BunchValueArrayDict):
    """
    References:
        transformers.file_utils.ModelOutput

    Examples:
        >>> @dataclass()
        ... class Test(ArrayFields):
        ...     c1: str = 'c1'
        ...     c2: int = 0
        ...     c3: list = None

        >>> r = Test()
        >>> r
        Test(c1='c1', c2=0, c3=None)
        >>> r.tuple
        ('c1', 0, None)
        >>> r.c1  # r[0]
        'c1'
        >>> r[1]  # r.c2
        0
        >>> r[1:]
        (0, None)

        >>> r = Test(c1='a', c3=[1,2,3])
        >>> r.c1
        'a'
        >>> r[-1]
        [1, 2, 3]
        >>> for it in r:
        ...     print(it)
        a
        0
        [1, 2, 3]

    """


def _bunch(x, cls):
    """ Recursively transforms a dictionary into a Bunch via copy.

        >>> b = _bunch({'urmom': {'sez': {'what': 'what'}}}, BunchDict)
        >>> b.urmom.sez.what
        'what'

        bunchify can handle intermediary dicts, lists and tuples (as well as
        their subclasses), but ymmv on custom datatypes.

        >>> b = _bunch({ 'lol': ('cats', {'hah':'i win'}), 'hello': [{'french':'salut', 'german':'hallo'}]}, BunchDict)
        >>> b.hello[0].french
        'salut'
        >>> b.lol[1].hah
        'i win'

        nb. As dicts are not hashable, they cannot be nested in sets/frozensets.
    """
    if isinstance(x, dict):
        return cls((k, _bunch(v, cls)) for k, v in x.items())
    elif isinstance(x, (list, tuple)):
        return type(x)(_bunch(v, cls) for v in x)
    else:
        return x


def _unbunch(x):  # noqa
    """ Recursively converts a Bunch into a dictionary.

        >>> b = BunchDict(foo=BunchDict(lol=True), hello=42, ponies='are pretty!')
        >>> _unbunch(b)
        {'foo': {'lol': True}, 'hello': 42, 'ponies': 'are pretty!'}

        unbunchify will handle intermediary dicts, lists and tuples (as well as
        their subclasses), but ymmv on custom datatypes.

        >>> b = BunchDict(foo=['bar', BunchDict(lol=True)], hello=42, ponies=('pretty!', BunchDict(lies='trouble!')))
        >>> _unbunch(b)
        {'foo': ['bar', {'lol': True}], 'hello': 42, 'ponies': ('pretty!', {'lies': 'trouble!'})}

        nb. As dicts are not hashable, they cannot be nested in sets/frozensets.
    """
    if isinstance(x, dict):
        return dict((k, _unbunch(v)) for k, v in x.items())
    elif isinstance(x, (list, tuple)):
        return type(x)(_unbunch(v) for v in x)
    else:
        return x


def _test_Fields():  # noqa
    """"""
    from datetime import datetime

    @dataclass()
    class Args(FieldBunchDict):
        """"""
        a: int = 100
        b: float = a * 0.1
        c: Any = datetime.now()

        if b > 10:
            d = a * 20
        else:
            d = a

    args = Args()
    print(args)
    for k, v in args.items():
        print(k, v)

    print(args.dict)
    print(args.get_pretty_dict())
    print(args.b)
    print(args.c)
    print(args.d)
    fp = r'./test.json'
    args.save(fp)

    del args

    args = Args.load(fp)
    print(args.b)
    print(args.c)
    print(args.d)


if __name__ == '__main__':
    """"""
    doctest.testmod(optionflags=doctest.ELLIPSIS)
