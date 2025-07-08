#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Time: 2021-11-16 11:35 上午

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
import torch.nn as nn

from ._bert import Bert
from ..pooling import MaskPooling

__all__ = [
    'SentenceBert'
]


class SentenceBert(nn.Module):
    """@Pytorch Models
    Bert 句向量

    References:
        [Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks](https://arxiv.org/abs/1908.10084)
    """

    def __init__(self, bert: Bert, pool_mode='mean'):
        """"""
        super().__init__()

        self.bert = bert
        self.pooling = MaskPooling(mode=pool_mode)

    def forward(self, token_ids, token_masks=None):
        """"""
        if token_masks is None:
            token_masks = (token_ids > 0).to(torch.uint8)  # [B, L]

        token_embeddings = self.bert(token_ids, token_masks=token_masks, return_value='token_embeddings')
        return self.pooling(token_embeddings, token_masks)



def _test():
    """"""
    doctest.testmod()


if __name__ == '__main__':
    """"""
    _test()
