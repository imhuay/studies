#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Time: 2021-11-04 8:34 下午

Author: huayang

Subject:

"""
import os
import sys
import json
import doctest

from typing import List

import torch.nn as nn
from torch import Tensor

from ._bert import Bert

__all__ = [
    'BertTextClassification'
]


class BertTextClassification(nn.Module):
    """@Pytorch Models
    Bert 文本分类
    """

    def __init__(self, bert: Bert, n_classes: int,
                 dropout_prob=0.2,
                 hidden_size=768):
        """"""
        super().__init__()

        self.bert = bert
        self.dropout = nn.Dropout(dropout_prob)
        self.clf = nn.Linear(hidden_size, n_classes)
        self.loss_fn = nn.CrossEntropyLoss()

    def forward(self,
                token_ids: Tensor,
                token_type_ids: Tensor = None,
                token_masks: Tensor = None,
                labels=None):
        """"""
        x = self.bert(token_ids, token_type_ids, token_masks, return_value='cls_embedding')
        x = self.dropout(x)
        logits = self.clf(x)

        if labels is not None:
            loss = self.loss_fn(logits, labels)
            return logits, loss

        return logits
