#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Time: 2021-11-04 7:25 下午

Author: huayang

Subject:

"""
import os
import sys
import json
import doctest

from typing import *
from collections import defaultdict

import torch
import torch.nn as nn

from ._bert import Bert
from ..crf import CRF


class BertCRF(nn.Module):
    """"""

    def __init__(self, bert: Bert, n_classes: int,
                 dropout_prob=0.2,
                 hidden_size=768):
        """"""
        super().__init__()

        self.bert = bert
        self.dropout = nn.Dropout(dropout_prob)
        self.clf = nn.Linear(hidden_size, n_classes)
        self.crf = CRF(num_tags=n_classes)

    def forward(self, token_ids, token_type_ids, token_masks, labels=None):
        """"""
        x = self.bert(token_ids, token_type_ids, token_masks, return_value='token_embeddings')  # [B, L, H]
        x = self.dropout(x)  # [B, L, H]
        logits = self.clf(x)  # [B, L, n_classes]

        if labels is not None:
            loss = -1.0 * self.crf(emissions=logits, tags=labels, masks=token_masks)
            return logits, loss

        return logits

    def decode(self, logits, token_masks=None):
        """"""
        return self.crf.decode(logits, token_masks)


def _test():
    """"""
    doctest.testmod()


if __name__ == '__main__':
    """"""
    _test()
