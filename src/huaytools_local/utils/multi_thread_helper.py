#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Time:
    2021-08-31 6:00 下午

Author:
    huayang

Subject:

"""
import functools
from multiprocessing.pool import ThreadPool
from typing import Callable, Union, Iterable

from tqdm import tqdm


def multi_thread_run(func: Callable,
                     args_iter: Union[Callable, Iterable],
                     n_thread=None,
                     ordered=False,
                     use_imap=False,
                     star_args=False,
                     ret_flatten=False):
    """
    Args:
        func: 回调函数
        args_iter: 参数序列
        n_thread: 线程数，默认 None
        ordered: 是否有序，默认 False；
            经测试即使为 False 也是有序的，可能与具体解释器有关；
        use_imap: 是否使用 imap，默认 False；
            使用 imap 可以利用 tqdm 估算进度，但是速度比 map 慢；
        star_args: 是否需要展开参数，默认 False，即默认 func 只接受一个参数；
            如果 func 形如 func(a, b, c)，则需要展开，而 func([a, b, c]) 则不需要；
        ret_flatten: 将结果展开，默认为 False；如果 func 本身就一次处理多条数据，如 func([a,b]) —> [A,B]
            那么当 ret_flatten=True 时，会将结果展开，即 [[A,B], [C,D], [E]] —> [A,B,C,D,E]

    Returns:
        func(args) 的结果集合
    """
    if star_args:
        _func = lambda a: func(*a)
    else:
        _func = func

    ret = []
    with ThreadPool(n_thread) as p:
        if use_imap:
            map_func = p.imap_unordered
        else:
            map_func = p.map

        if ordered:
            _func_new = lambda a: (a[0], _func(a[1]))
            args_ls_new = [(i, args) for i, args in enumerate(args_iter)]
            ret_iter = map_func(_func_new, args_ls_new)
        else:
            ret_iter = map_func(_func, args_iter)

        if use_imap:
            ret_iter = tqdm(ret_iter)

        for it in ret_iter:
            ret.append(it)

    if ordered:
        ret = [it[1] for it in sorted(ret, key=lambda x: x[0])]

    if ret_flatten:
        tmp = []
        for it in ret:
            tmp.extend(it)
        ret = tmp

    return ret


def multi_thread_run_dn(args_iter, **kwargs):
    """
    多线程执行装饰器

    Args:
        args_iter: 参数序列，也可以是一个函数
        kwargs: 详见 multi_thread_run 相关参数
    """

    def decorator(func):
        """"""

        @functools.wraps(func)
        def decorated_func():
            _args_iter = args_iter() if isinstance(args_iter, Callable) else args_iter
            return multi_thread_run(func, _args_iter, **kwargs)

        return decorated_func

    return decorator


def _test():
    """"""
    import os
    os.makedirs('-out', exist_ok=True)

    def _test_multi_download():
        """ 测试多线程下载 """
        from huaytools_local.utils import download_file

        args_ls = [('https://www.baidu.com/', './-out/baidu1.html'),
                   ('https://www.baidu.com/', './-out/baidu2.html'),
                   ('https://www.baidu.com/', './-out/baidu3.html')]

        ret = multi_thread_run(download_file, args_ls, star_args=True)
        print(ret)
        assert ret == ['./-out/baidu1.html', './-out/baidu2.html', './-out/baidu3.html']

    _test_multi_download()

    def _test_multi_thread_run():
        """ star_args 参数测试 """

        def some_func(s, x):
            """一个简单的测试函数，输入 s 加一个后缀"""
            # time.sleep(math.sqrt(int(s)))
            return s + '-' + x

        # 构造参数序列
        args_ls = list([(str(i), str(i + 1)) for i in range(1000)])
        ret1 = multi_thread_run(some_func, args_ls, star_args=True)
        assert ret1[:5] == ['0-1', '1-2', '2-3', '3-4', '4-5']

        # star_args 与否的区别
        def ss_func(a):  # 包成一个参数
            s, x = a
            return some_func(s, x)

        ret2 = multi_thread_run(ss_func, args_ls, star_args=False)
        # print(ret2)
        assert ret1 == ret2

    _test_multi_thread_run()


if __name__ == '__main__':
    """"""
    _test()
