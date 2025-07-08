#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Time: 2021-11-22 11:43 上午

Author: huayang

Subject:

"""
import os  # noqa
import doctest  # noqa

# from typing import *
# from itertools import islice
# from collections import defaultdict

# from tqdm import tqdm

import torch
from torch.utils.data import DataLoader
from huaytools_local.pytorch._todo.data import MultiBertSample, BertDataLoader


def _test_single():
    """"""
    from sentence_transformers import InputExample, SentenceTransformer

    from huaytools_local.pytorch._todo.nn import get_CKPT_DIR
    pt_ckpt_path = os.path.join(get_CKPT_DIR(), 'bert-base-chinese')
    st = SentenceTransformer(pt_ckpt_path)
    file = ['我爱python', '我爱机器学习', '我爱nlp'] * 3  # 9

    # SentenceTransformer
    ds_st = [InputExample(texts=[row], label=1) for row in file]
    dl_st = DataLoader(ds_st, batch_size=4, collate_fn=st.smart_batching_collate)  # noqa

    ds_my = [MultiBertSample(texts=[row], label=1) for row in file]
    dl_my = BertDataLoader(ds_my, batch_size=4)

    for b_st, b_my in zip(dl_st, dl_my):
        assert torch.equal(b_st[0][0]['input_ids'], b_my[0][0]['token_ids'])


def _test():
    """"""
    doctest.testmod()
    _test_single()


if __name__ == '__main__':
    """"""
    _test()
