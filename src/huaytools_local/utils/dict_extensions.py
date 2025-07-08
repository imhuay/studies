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
from dataclasses import dataclass, fields, field
from collections import OrderedDict


@dataclass
class FieldDict(dict):
    """
    兼顾 dataclass 和 dict 的功能；
    主要为了代替以下场景：
        ```python
        from copy import deepcopy
        default_info = {
            'f1': 1,
            'f2': '2',
            'f3': set()
        }

        one_info = deepcopy(default_info)
        one_info['f1'] = ...
        one_info['f2'] = ...
        one_info['f3'] = ...

        infos = [one_info, ...]
        json.dumps(infos)

        # 使用 FixedFieldDict 代替上述流程
        @dataclass
        class DefaultInfo(FixedFieldDict):
            f1: int = 1
            f2: str = '2'
            f3: set = field(default_factory=set)

        one_info = DefaultInfo()
        one_info.f1 = ...
        one_info.f2 = ...
        one_info.f3 = ...

        infos = [one_info, ...]
        json.dumps(infos)
        ```

    Notes:
        - 可以为动态地为 FieldDict 添加新的 attr，但是这些 attr 不会作为新的 field；
            也不会保存到 dict 中，详见 `__setattr__` 和 `__setitem__`

    Examples:
        >>> @dataclass
        ... class Features(FieldDict):
        ...     a: int = 1
        ...     b: str = 'B'
        ...     c: list = field(default_factory=list)
        ...     d = Any  # d 因为没有注释，所以不会被 fields 捕获
        >>> f = Features()
        >>> print(f)
        Features(a=1, b='B', c=[])
        >>> list(f.items())
        [('a', 1), ('b', 'B'), ('c', [])]
        >>> f.a = 2
        >>> f['a'] = 3
        >>> f.d = 'D'  # ok, d is attr, not field
        >>> getattr(f, 'd')
        'D'
        >>> 'd' not in f.field_names
        True
        >>> f['d'] = 'D'  # err
        Traceback (most recent call last):
            ...
        KeyError: 'd not in fields'
        >>> 'd' not in f and 'd' not in f.field_names
        True
        >>> json.dumps(f)  # 可以直接当做 dict 处理
        '{"a": 3, "b": "B", "c": []}'
    """

    def __post_init__(self):
        """"""
        # 把 field 依次添加到 dict 中
        for f in fields(self):
            self[f.name] = getattr(self, f.name)

    def __setattr__(self, key, value):
        """"""
        super().__setattr__(key, value)
        if key in self.field_names:
            super().__setitem__(key, value)

    def __setitem__(self, key, value):
        """"""
        if key not in self.field_names:
            raise KeyError(f'{key} not in fields')
        else:
            super().__setattr__(key, value)
            super().__setitem__(key, value)

    @property
    def field_names(self) -> list[str]:
        return [f.name for f in fields(self)]


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


class BunchDict(dict):
    """@Python 自定义数据结构
    基于 dict 实现 Bunch 模式

    实现方法：
        - 通过重写 __getattr__、__setattr__、__delattr__ 同步 o.x 和 o['x'] 的行为
        - 为了防止与内部成员冲突，比如 __dict__，会预先调用 __getattribute__（优先级高于 __getattr__）

    Notes:
        - [2022.08.25] 通过将 __dict__ property 化限制了以下行为：
            - 如果直接向 __dict__ 添加属性，且存在同名 key，将导致 o.x 和 o['x'] 不一致；
                ```python
                o = BunchDict(a=1, b=2)
                o.__dict__['a'] = 10
                print(o.a, o['a'])  # 10, 1
                ```

    Examples:
        # 示例 1
        >>> x = BunchDict(a=1, b=2)
        >>> x
        {'a': 1, 'b': 2}
        >>> x.c = 3  # x['c'] = 3
        >>> 'c' in x
        True
        >>> x['c']
        3
        >>> x['d'] = {'bar': 6}  # x.d = {'bar': 6}
        >>> hasattr(x, 'd')
        True
        >>> x.d.bar
        6
        >>> dir(x)
        ['a', 'b', 'c', 'd']
        >>> vars(x)
        {'a': 1, 'b': 2, 'c': 3, 'd': {'bar': 6}}
        >>> del x.a
        >>> x.a
        Traceback (most recent call last):
            ...
        AttributeError: a
        >>> # x.__dict__ = {'a': 123}  # err
        >>> x.__dict__
        {'b': 2, 'c': 3, 'd': {'bar': 6}}
        >>> x.a = 456
        >>> x
        {'b': 2, 'c': 3, 'd': {'bar': 6}, 'a': 456}
        >>> 'a' in x
        True
        >>> hasattr(x, 'a')
        True

        # 示例 2
        >>> y = {'foo': {'a': 1, 'bar': {'c': 'C'}}, 'b': 2}
        >>> y == BunchDict.from_dict(y) == BunchDict(y)
        True
        >>> x = BunchDict(y, d={'z': 26})
        >>> x.foo
        {'a': 1, 'bar': {'c': 'C'}}
        >>> x.foo.bar
        {'c': 'C'}
        >>> all(type(it) == BunchDict for it in [x.foo, x.foo.bar, x.d])  # noqa
        True

    References:
        - bunch（pip install bunch）
    """

    # __slots__ = ()

    __dict__ = property(lambda self: self)
    """ 禁止直接修改 __dict__ """

    def __dir__(self):
        """ 屏蔽其他属性或方法 """
        return self.keys()

    def __init__(self, seq: Union[Mapping, Iterable] = None, /, **kwargs):
        # 初始化 self 为一个空 dict
        super().__init__()

        # 模拟向 dict 中添加元素的过程：https://docs.python.org/zh-cn/3/library/stdtypes.html#mapping-types-dict
        #   通过手动添加元素，确保每个类型为 dict 的值会被初始化为 BunchDict
        if seq is not None:
            if isinstance(seq, Mapping):
                seq = seq.items()
            for k, v in seq:
                self[k] = BunchDict.bunching(v)  # 如果 v 的类型为 dict，将被修改为 BunchDict

        for k, v in kwargs.items():
            self[k] = BunchDict.bunching(v)

    def __getattr__(self, name: str):
        """ make `o.name` equivalent to `o[name]` """
        try:
            # Throws exception if not in prototype chain
            return super().__getattribute__(name)
        except AttributeError:
            try:
                return self[name]
            except KeyError:
                raise AttributeError(name)

    def __setattr__(self, name: str, value):
        """ make `o.name = value` equivalent to `o[name] = value` """
        try:
            # Throws exception if not in prototype chain
            super().__getattribute__(name)
        except AttributeError:
            self[name] = value
        else:
            object.__setattr__(self, name, value)

    def __delattr__(self, name: str):
        """ make `del o.name` equivalent to `del o[name]` """
        try:
            # Throws exception if not in prototype chain
            super().__getattribute__(name)
        except AttributeError:
            try:
                del self[name]
            except KeyError:
                raise AttributeError(name)
        else:
            super().__delattr__(name)

    def __setitem__(self, key: str, value):
        """ make behavior consistent with `__init__` """
        super().__setitem__(key, BunchDict.bunching(value))

    @classmethod
    def from_dict(cls, d: dict) -> 'BunchDict':
        """ create from dict """
        return cls.bunching(d)

    @classmethod
    def bunching(cls, x: Union[Mapping, Any]) -> Union['BunchDict', Any]:
        return _bunching(x)


def _bunching(x) -> Union[BunchDict, Any]:
    """
    Recursively transforms a dictionary into a Bunch.

    Bunchify can handle intermediary dicts, lists and tuples (
    as well as their subclasses), but ymmv on custom datatypes.

    Examples:
        >>> b = _bunching({'urmom': {'sez': {'what': 'what'}}})
        >>> b.urmom.sez.what
        'what'
        >>> b = _bunching({ 'lol': ('cats', {'hah':'i win'}), 'hello': [{'french':'salut', 'german':'hallo'}]})
        >>> b.hello[0].french
        'salut'
        >>> b.lol[1].hah
        'i win'
    """
    if isinstance(x, Mapping):
        return BunchDict((k, _bunching(v)) for k, v in x.items())
    elif isinstance(x, (list, tuple)):
        return type(x)(_bunching(v) for v in x)
    else:
        return x


# class ConfigDict(BunchDict):
#     """
#     Examples:
#         # 从字典加载
#         >>> x = {'d': 4, 'e': {'a': 1, 'b': 2, 'c': 3}}
#         >>> y = BunchDict.from_dict(x)
#         >>> y
#         {'d': 4, 'e': {'a': 1, 'b': 2, 'c': 3}}
#
#         # 预定义配置
#         >>> class Config(BunchDict):
#         ...     def __init__(self, **config_items):
#         ...         from datetime import datetime
#         ...         self.a = 1
#         ...         self.b = 2
#         ...         self.c = datetime(2012, 1, 1)  # 注意是一个特殊对象，默认 json 是不支持的
#         ...         super().__init__(**config_items)
#         >>> args = Config(b=20)
#         >>> args.a = 10
#         >>> args
#         {'a': 10, 'b': 20, 'c': datetime.datetime(2012, 1, 1, 0, 0)}
#         >>> args == args.dict
#         True
#         >>> # 添加默认中不存的配置项
#         >>> args.d = 40
#         >>> print(args.get_pretty_dict())  # 注意 'c' 保存成了特殊形式
#         {
#             "a": 10,
#             "b": 20,
#             "c": "datetime.datetime(2012, 1, 1, 0, 0)__@AnyEncoder@__gASVKgAAAAAAAACMCGRhdGV0aW1llI...",
#             "d": 40
#         }
#
#         # 保存/加载
#         # >>> fp = r'./-test/test_save_config.json'
#         # >>> os.makedirs(os.path.dirname(fp), exist_ok=True)
#         # >>> args.save(fp)  # 保存
#         # >>> x = Config.load(fp)  # 重新加载
#         # >>> assert x == args.dict
#         # >>> _ = os.system('rm -rf ./-test')
#
#     """
#
#     @classmethod
#     def from_dict(cls, d: dict):
#         return _bunch(d, cls)
#
#     @property
#     def dict(self):
#         """"""
#         return dict(self)
#
#     def get_pretty_dict(self, sort_keys=True, print_cls_name=False):
#         """"""
#         from huaytools.utils import AnyJSONEncoder
#         pretty_dict = json.dumps(self.dict, cls=AnyJSONEncoder, indent=4, ensure_ascii=False, sort_keys=sort_keys)
#         if print_cls_name:
#             pretty_dict = f'{self.__class__.__name__}: {pretty_dict}'
#
#         return pretty_dict
#
#     # def __str__(self):
#     #     """"""
#     #     return str(self.dict)
#
#     def save(self, fp: str, sort_keys=True):
#         """ 保存配置到文件 """
#         with open(fp, 'w', encoding='utf8') as fw:
#             fw.write(self.get_pretty_dict(sort_keys=sort_keys))
#
#     @classmethod
#     def load(cls, fp: str):
#         """"""
#         from huaytools.utils import AnyJSONDecoder
#         config_items = json.load(open(fp, encoding='utf8'), cls=AnyJSONDecoder)
#         return cls(**config_items)


# @dataclass()
# class FieldBunchDict(BunchDict):
#     """@Python 自定义数据结构
#     基于 dataclass 的 BunchDict
#
#     原来预定义的参数，需要写在 __init__ 中：
#         ```
#         class Args(BunchDict):
#             def __init__(self):
#                 a = 1
#                 b = 2
#         ```
#     现在可以直接当作 dataclass 来写：
#         ```
#         @dataclass()
#         class Args(BunchDict):
#             a: int = 1
#             b: int = 2
#         ```
#
#     Examples:
#         # 预定义配置
#         >>> @dataclass()
#         ... class Config(FieldBunchDict):
#         ...     from datetime import datetime
#         ...     a: int = 1
#         ...     b: int = 2
#         ...     c: Any = datetime(2012, 1, 1)  # 注意是一个特殊对象，默认 json 是不支持的
#         >>> args = Config(b=20)
#         >>> args.a = 10
#         >>> args
#         Config(a=10, b=20, c=datetime.datetime(2012, 1, 1, 0, 0))
#         >>> args.dict
#         {'a': 1, 'b': 20, 'c': datetime.datetime(2012, 1, 1, 0, 0)}
#         >>> args.d = 40  # 默认中没有的配置项（不推荐，建议都定义在继承类中，并设置默认值）
#         Traceback (most recent call last):
#             ...
#         KeyError: '`d` not in fields. If it has to add new field, recommend to use `BunchDict`'
#
#         # 保存/加载
#         >>> fp = r'./-test/test_save_config.json'
#         >>> os.makedirs(os.path.dirname(fp), exist_ok=True)
#         >>> args.save(fp)  # 保存
#         >>> x = Config.load(fp)  # 重新加载
#         >>> assert x == args.dict
#         >>> _ = os.system('rm -rf ./-test')
#
#     """
#
#     def __post_init__(self):
#         """"""
#         # 获取所有 field
#         class_fields = fields(self)
#         # 依次添加到 dict 中
#         for f in class_fields:
#             self[f.name] = getattr(self, f.name)
#
#     def __setattr__(self, key, value):
#         field_set = set(f.name for f in fields(self))
#         if key not in field_set:
#             raise KeyError(
#                 f'`{key}` not in fields. If it has to add new field, recommend to use `{BunchDict.__name__}`')
#         else:
#             super().__setattr__(key, value)


# class BunchArrayDict(ArrayDict, BunchDict):
#     """
#
#     Examples:
#         >>> d = BunchArrayDict(a=1, b=2)
#         >>> isinstance(d, dict)
#         True
#         >>> print(d, d.a, d[1])
#         BunchArrayDict([('a', 1), ('b', 2)]) 1 BunchArrayDict([('b', 2)])
#         >>> d.a, d.b, d.c = 10, 20, 30
#         >>> print(d, d[1:])
#         BunchArrayDict([('a', 10), ('b', 20), ('c', 30)]) BunchArrayDict([('b', 20), ('c', 30)])
#         >>> print(*d)
#         a b c
#         >>> dir(d)
#         ['a', 'b', 'c']
#         >>> assert 'a' in d
#         >>> del d.a
#         >>> assert 'a' not in d
#         >>> getattr(d, 'a', 100)
#         100
#
#         # 测试嵌套
#         >>> x = BunchArrayDict(d=40, e=d)
#         >>> x
#         BunchArrayDict([('d', 40), ('e', BunchArrayDict([('b', 20), ('c', 30)]))])
#         >>> print(x.d, x.e.b)
#         40 20
#
#         >>> z = {'d': 4, 'e': {'a': 1, 'b': 2, 'c': 3}}
#         >>> y = BunchArrayDict.from_dict(z)
#         >>> y
#         BunchArrayDict([('d', 4), ('e', BunchArrayDict([('a', 1), ('b', 2), ('c', 3)]))])
#         >>> y.e.c
#         3
#
#     """


# class BunchValueArrayDict(ValueArrayDict, BunchDict):
#     """
#
#     Examples:
#         >>> d = BunchValueArrayDict(a=1, b=2)
#         >>> isinstance(d, dict)
#         True
#         >>> print(d, d.a, d[1])
#         BunchValueArrayDict([('a', 1), ('b', 2)]) 1 2
#         >>> d.a, d.b, d.c = 10, 20, 30
#         >>> print(d, d[2], d[1:])
#         BunchValueArrayDict([('a', 10), ('b', 20), ('c', 30)]) 30 (20, 30)
#         >>> print(*d)
#         10 20 30
#         >>> dir(d)
#         ['a', 'b', 'c']
#         >>> assert 'a' in d
#         >>> del d.a
#         >>> assert 'a' not in d
#         >>> getattr(d, 'a', 100)
#         100
#
#         # 测试嵌套
#         >>> x = BunchValueArrayDict(d=40, e=d)
#         >>> x
#         BunchValueArrayDict([('d', 40), ('e', BunchValueArrayDict([('b', 20), ('c', 30)]))])
#         >>> print(x.d, x.e.b)
#         40 20
#
#         >>> z = {'d': 4, 'e': {'a': 1, 'b': 2, 'c': 3}}
#         >>> y = BunchValueArrayDict.from_dict(z)
#         >>> y
#         BunchValueArrayDict([('d', 4), ('e', BunchValueArrayDict([('a', 1), ('b', 2), ('c', 3)]))])
#         >>> y.e.c
#         3
#
#     """


# @dataclass()
# class ArrayFields(FieldBunchDict, BunchValueArrayDict):
#     """
#     References:
#         transformers.file_utils.ModelOutput
#
#     Examples:
#         >>> @dataclass()
#         ... class Test(ArrayFields):
#         ...     c1: str = 'c1'
#         ...     c2: int = 0
#         ...     c3: list = None
#
#         >>> r = Test()
#         >>> r
#         Test(c1='c1', c2=0, c3=None)
#         >>> r.tuple
#         ('c1', 0, None)
#         >>> r.c1  # r[0]
#         'c1'
#         >>> r[1]  # r.c2
#         0
#         >>> r[1:]
#         (0, None)
#
#         >>> r = Test(c1='a', c3=[1,2,3])
#         >>> r.c1
#         'a'
#         >>> r[-1]
#         [1, 2, 3]
#         >>> for it in r:
#         ...     print(it)
#         a
#         0
#         [1, 2, 3]
#
#     """


def _unbunch(x: BunchDict) -> dict:  # noqa
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


class __Test:
    """"""

    def __init__(self):
        """"""
        import time
        for k, v in self.__class__.__dict__.items():
            if k.startswith('_test') and isinstance(v, Callable):
                print(f'\x1b[32m=== Start "{k}" {{\x1b[0m')
                start = time.time()
                v(self)
                print(f'\x1b[32m}} End "{k}" - Spend {time.time() - start:3f}s===\x1b[0m\n')

    def _test_doctest(self):  # noqa
        """"""
        import doctest
        doctest.testmod(optionflags=doctest.ELLIPSIS)

    def _test_FixedFieldDict(self):  # noqa
        """"""

    def _test_BunchDict(self):  # noqa
        """"""
        o = BunchDict(a=1, b=2)
        # o.__dict__['a'] = 10
        print(vars(o))
        print(f'o.a={o.a}, o["a"]={o["a"]}')  # 10, 1


if __name__ == '__main__':
    """"""
    __Test()
