#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Time:
    2021-02-01 21:21
    
Author:
    huayang
    
Subject:
    一个使用多线程下载的示例

Notes:
    - 最后一定要执行 p.close()，否则在命令行中使用时会一直 wait（在 pycharm 中执行正常）；
    - 或者使用 with 语法，但要注意，ret_iter 要在 with 内跑完；
    - 禁止写成 ThreadPool(n_thread).xxx 的形式，这样会连 pool 对象都拿不到，永远处于等待状态
"""
import os
import time

import requests

from tqdm import tqdm
from multiprocessing.pool import ThreadPool

ALLOW_FORMATS = ('.jpg', '.jpeg', '.png', '.gif', '.bmp')


def file_download(args, timeout=3, n_retry_max=5):
    """数据下载"""

    def _get_ext(url: str):
        for ext in ALLOW_FORMATS:
            if -1 != url.find(ext):
                return ext

        return '.jpg'

    url, dir_path, file_name = args
    n_retry = 0
    response = None
    while n_retry < n_retry_max:
        try:
            response = requests.get(url=url, timeout=timeout)
            break
        except:
            pass
        finally:
            n_retry += 1

    ext = _get_ext(url)
    save_path = os.path.join(dir_path, file_name + ext)

    if response:
        with open(save_path, 'wb') as fw:
            fw.write(response.content)

    return save_path


def data_download(main_path, url_ls, label_ls=None, name_ls=None, n_thread=None):
    """数据下载（多线程）

    Args:
        main_path:
        url_ls:
        label_ls:
        name_ls:
        n_thread:
    """
    os.makedirs(main_path, exist_ok=True)

    if label_ls is None:
        label_ls = [''] * len(url_ls)
    else:
        assert len(url_ls) == len(label_ls)
        label_st = set(label_ls)
        for label in label_st:
            os.makedirs(os.path.join(main_path, label), exist_ok=True)

    if name_ls is None:
        name_ls = list(str(i) for i in range(1, len(url_ls) + 1))

    args_ls = [(url, os.path.join(main_path, label), file_name)
               for file_name, url, label in zip(name_ls, url_ls, label_ls)]

    # 一定要执行 p.close()，否则在命令行中运行时会一直 wait（在 pycharm 中执行正常）
    # 或者使用 with 语法，但要注意，ret_iter 要在 with 内跑完
    with ThreadPool(n_thread) as p:
        ret_iter = p.imap_unordered(file_download, args_ls)
        ret_ls = []
        for ret in tqdm(ret_iter):
            ret_ls.append(ret)

    # p = ThreadPool(n_thread)
    # ret_iter = p.imap_unordered(file_download, args_ls)
    # ret_ls = []
    # for ret in tqdm(ret_iter):
    #     """"""
    #     ret_ls.append(ret)
    # p.close()

    return ret_ls


def tst_data_download():
    """"""
    main_path = 'out/test'
    url_ls = ['https://p0.meituan.net/dpmerchantpic/543d27fe7f877ea881c61ec859c6ddaa63445.jpg'] * 6
    label_ls = ['a', 'b', 'c'] * 2
    name_ls = ['a', 'b', 'c', 'd', 'e', 'f']
    ret = data_download(main_path, url_ls, label_ls=label_ls, name_ls=name_ls)


cnt = 0
def tst_speed():
    """"""
    n_iter = 3000000
    txt = ['ababababab'] * n_iter

    def func(t: str):
        global cnt

        cnt += 1
        t = t.replace('b', 'B')
        return '%s_%s' % (cnt, t)

    beg = time.time()
    ret = []
    with ThreadPool(10) as p:
        ret_iter = p.map(func, txt, chunksize=100)
        for it in ret_iter:
            ret.append(it)
    print('消耗时间：', time.time() - beg)  # map: 2.3
    print(ret[:3])

    # global cnt
    # cnt = 0
    # beg = time.time()
    # ret = []
    # with ThreadPool(10) as p:
    #     ret_iter = p.imap(func, txt)
    #     for it in ret_iter:
    #         ret.append(it)
    # print('消耗时间：', time.time() - beg)  # 2.3
    # print(ret[:3])


if __name__ == '__main__':
    """"""
    tst_speed()
