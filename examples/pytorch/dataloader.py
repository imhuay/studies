#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Time: 2022-06-09 5:52 下午

Author: huayang

Subject:

"""
import os  # noqa
import doctest  # noqa

# from collections import defaultdict
# from itertools import islice
# from pathlib import Path
# from typing import *

# from tqdm import tqdm


import torch
import torch.nn as nn

from huaytools_local.pytorch.utils import ToyDataLoader


def demo_map_one():
    """"""
    import numpy as np

    data = np.random.rand(12, 3)  # 12 条数据

    def map_one(one):
        return torch.as_tensor(one).to(torch.float)  # 把每条数据转换成 torch 张量

    dl = ToyDataLoader(data, batch_size=2, map_one_fn=map_one)

    for b in dl:
        print(b)


def demo_map_batch():
    """"""
    from transformers import AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained('bert-base-chinese')

    ss = ['我是谁', '自然语言处理', '深度学习'] * 10

    def map_batch(batch):
        batch = tokenizer(batch, padding=True, truncation=True, return_tensors='pt')
        return batch

    dl = ToyDataLoader(ss, batch_size=2, collate_fn=map_batch)

    for b in dl:
        print(b)


def demo_iter():
    """"""

    def it():
        for i in range(12):
            yield i

    # print(len(it()))

    def map_one(one):
        return torch.as_tensor(one).to(torch.float)  # 把每条数据转换成 torch 张量

    # ds = AnyDataset(it(), map_fn=map_one)

    dl = ToyDataLoader(list(it()), batch_size=4, map_fn=map_one)

    for b in dl:
        print(b)

    dl = ToyDataLoader(it(), batch_size=4, map_fn=map_one, shuffle=False)

    for b in dl:
        print(b)


if __name__ == '__main__':
    """"""
    doctest.testmod()

    # demo_map_one()
    # demo_map_batch()
    demo_iter()
