#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Time: 2022-03-02 7:27 下午

Author: huayang

Subject:

"""
import os
import sys
import json
import logging
import platform
import doctest
import math

import requests

from typing import *
from datetime import datetime

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
                    datefmt='%Y.%m.%d %H:%M:%S',
                    level=logging.INFO)

from huaytools.utils.xls_helper import XLSHelper
from huaytools.utils.find_best_threshold import find_best_threshold_binary
from huaytools.utils.special_json import (
    CustomIndentJSONEncoder,
    AnyJSONEncoder,
    AnyJSONDecoder
)
from huaytools.utils.simple_argparse import simple_argparse
from huaytools.utils.special_dict import BunchDict
from huaytools.utils.file_helper import list_dir_recur
from huaytools.utils.multi_thread_helper import multi_thread_run
from huaytools.utils.config_loader import load_config, load_config_file
from huaytools.utils.serialize_helper import (
    obj_to_str,
    str_to_obj,
    bytes_to_str,
    str_to_bytes,
    file_to_str,
    str_to_file
)


def merge_intersected_sets(src: List[Set]):
    """合并有交集的集合"""
    pool = set(map(frozenset, src))  # 去重
    groups = []
    while pool:
        groups.append(set(pool.pop()))
        while True:
            for s in pool:
                if groups[-1] & s:
                    groups[-1] |= s
                    pool.remove(s)
                    break
            else:
                break
    return groups


def list_split(ls, per_size=None, n_chunk=None):
    """ [0, 1, 2, 3, 4, 5, 6] -> [[0, 1], [2, 3], [4, 5], [6]] """
    assert (per_size or n_chunk) and not (per_size and n_chunk), '`per_size` and `n_chunk` must be set only one.'

    if n_chunk is not None:
        per_size = math.ceil(len(ls) / n_chunk)

    ret = []
    for i in range(0, len(ls), per_size):
        ret.append(ls[i: i + per_size])

    return ret


def list_flatten(lss):
    """ [[0, 1], [2, 3], [4, 5], [6]] -> [0, 1, 2, 3, 4, 5, 6] """
    ret = []
    for it in lss:
        ret.extend(it)

    return ret


def remove_duplicates(src: Sequence, ordered=True) -> List:
    """
    remove duplicates

    Args:
        src:
        ordered:

    Examples:
        >>> ls = [1,2,3,3,2,4,2,3,5]
        >>> remove_duplicates(ls)
        [1, 2, 3, 4, 5]

    """
    ret = list(set(src))

    if ordered:
        ret.sort(key=src.index)

    return ret


def get_caller_name(num_back=2) -> str:
    """@Python Utils
    获取调用者的名称

    如果是方法，则返回方法名；
    如果是模块，则返回文件名；
    如果是类，返回类名，但要作为类属性，而不是定义在 __init__ 中

    说明：如果在方法内使用，那么直接调用 `sys._getframe().f_code.co_name` 就是输出了本身的函数名；
        这里因为是作为工具函数，所以实际上输出的调用本方法的函数名，所以需要 `f_back` 一次

    Args:
        num_back: 回溯层级，大于 0，默认为 2

    Examples:
        >>> def f():  # 不使用本方法
        ...     return sys._getframe().f_code.co_name  # noqa
        >>> f()
        'f'
        >>> def foo():
        ...     return get_caller_name(1)
        >>> foo()
        'foo'

        # 使用场景：查看是谁调用了 `bar` 方法
        >>> def bar():
        ...     return get_caller_name()
        >>> def zoo():
        ...     return bar()
        >>> zoo()
        'zoo'

        # 使用场景：自动设置 logger name
        >>> def _get_logger(name=None):
        ...     name = name or get_caller_name()
        ...     return logging.getLogger(name)
        >>> class T:
        ...     cls_name = get_caller_name(1)  # level=1
        ...     logger = _get_logger()  # get_logger 中使用了 get_caller_name
        >>> T.cls_name
        'T'
        >>> T.logger.name
        'T'

        # 使用场景：自动从字典中获取属性值
        >>> class T:
        ...     default = {'a': 1, 'b': 2}
        ...     def _get_attr(self):
        ...         name = get_caller_name()
        ...         return self.default[name]
        ...     @property
        ...     def a(self):
        ...         # return default['a']
        ...         return self._get_attr()
        ...     @property
        ...     def b(self):
        ...         # return default['b']
        ...         return self._get_attr()
        >>> t = T()
        >>> t.a
        1
        >>> t.b
        2

    """
    assert num_back >= 1

    frame = sys._getframe()  # noqa
    while num_back > 0:
        frame = frame.f_back
        num_back -= 1

    co_name = frame.f_code.co_name

    if co_name == '<module>':  # 当调用方是一个模块，此时返回模块的文件名
        filename, _ = os.path.splitext(os.path.basename(frame.f_code.co_filename))
        return filename

    return co_name


def set_stdout_null():
    """ 抑制标准输出 """
    sys.stdout = open(os.devnull, 'w')


def get_print_json(obj, **json_kwargs):
    """ 生成 printable json"""
    obj = obj if isinstance(obj, dict) else obj.__dict__

    json_kwargs.setdefault('cls', AnyJSONEncoder)
    json_kwargs.setdefault('indent', 4)
    json_kwargs.setdefault('ensure_ascii', False)
    json_kwargs.setdefault('sort_keys', True)
    return json.dumps(obj, **json_kwargs)


def set_default(obj, name: str, default: Any) -> Any:
    """ 行为类似 dict.setdefault，可以作用于一般类型（兼容 dict） """
    if isinstance(obj, dict):
        return obj.setdefault(name, default)

    if not hasattr(obj, name):
        return setattr(obj, name, default)
    return getattr(obj, name)


def get_attr(args, name: str, default=None) -> Any:
    """ 等价于 getattr（兼容 dict）；跟 set_default 的区别是，如果 obj 中不存在 name 这个参数，不会将其添加到对象中 """
    if isinstance(args, dict):
        if default is not None:
            return args.get(name, default)
        else:
            return args[name]  # args.get 不会报异常
    else:
        if default is not None:
            return getattr(args, name, default)
        else:
            return getattr(args, name)


def set_attr(args, name: str, value) -> None:
    """ 等价于 setattr（兼容 dict） """
    if isinstance(args, dict):
        args[name] = value
    else:
        setattr(args, name, value)


def get_typename(o):
    """
    References: torch.typename
    """
    module = ''
    if hasattr(o, '__module__') and o.__module__ != 'builtins' \
            and o.__module__ != '__builtin__' and o.__module__ is not None:
        module = o.__module__ + '.'

    if hasattr(o, '__qualname__'):
        class_name = o.__qualname__
    elif hasattr(o, '__name__'):
        class_name = o.__name__
    else:
        class_name = o.__class__.__name__

    return module + class_name


def set_env(key: str, value: str):
    """ 设置环境变量 """
    os.environ[key] = value


def get_env(key, default=None):
    """
    Examples:
        >>> get_env('HOME')
        '/Users/huayang'
    """
    return os.environ.get(key, default)


def get_env_dict():
    """ 获取环境变量（字典）

    Examples:
        >>> env = get_env_dict()
        >>> env['ttt'] = 'ttt'
        >>> env['ttt']
        'ttt'
    """
    return os.environ


def get_logger(name=None):
    """"""
    name = name or get_caller_name()
    return logging.getLogger(name)


def get_time_string(fmt="%Y%m%d%H%M%S"):
    """获取当前时间（格式化）"""
    return datetime.now().strftime(fmt)


def get_system_type():
    """获取当前系统类型"""
    return platform.system()


def _system_is(sys_name: str):
    """"""
    sys_name = sys_name.lower()
    if sys_name in {'mac', 'macos'}:
        sys_name = 'Darwin'
    elif sys_name in {'win', 'window', 'windows'}:
        sys_name = 'Windows'
    elif sys_name in {'linux'}:
        sys_name = 'Linux'

    return get_system_type() == sys_name


def is_mac():
    """判断是否为 mac os 系统"""
    return _system_is('Darwin')


def is_linux():
    """判断是否为 linux 系统"""
    return _system_is('Linux')


def is_windows():
    """判断是否为 windows 系统"""
    return _system_is('Windows')


def get_response(url,
                 timeout=3,
                 n_retry_max=5,
                 return_content=True,
                 check_func=None):
    """
    Args:
        url:
        timeout: 超时时间，单位秒
        n_retry_max: 最大重试次数
        return_content: 是否返回 response.content
        check_func: 内容检查函数，函数接收单个 response 对象作为参数
    """
    n_retry = 0
    response = None
    while n_retry < n_retry_max:
        try:
            response = requests.get(url=url, timeout=timeout)
            if return_content:
                response = response.content
            if check_func is None or check_func(response):
                break
        except:
            pass
        finally:
            n_retry += 1

    return response


def download_file(url,
                  save_path=None,
                  **kwargs):
    """
    下载指定 url 内容

    Args:
        url:
        save_path: 保存路径
        kwargs: get_response 相关参数

    """
    kwargs['return_content'] = kwargs.pop('return_content', False)
    response = get_response(url, **kwargs)

    if response and save_path:
        with open(save_path, mode='wb') as f:
            f.write(response.content)

    return save_path


if __name__ == '__main__':
    """"""
    doctest.testmod()
