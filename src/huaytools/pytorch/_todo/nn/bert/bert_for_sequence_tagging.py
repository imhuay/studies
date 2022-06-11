#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Time: 2021-11-09 8:35 下午

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

from torch import Tensor

from ._bert import Bert

__all__ = [
    'BertSequenceTagging'
]


class BertSequenceTagging(nn.Module):
    """@Pytorch Models
    Bert 序列标注
    """

    def __init__(self, bert: Union[str, nn.Module],
                 n_classes: int,
                 dropout_prob=0.2):
        """"""
        super().__init__()

        if isinstance(bert, str):
            self.bert = Bert.from_pretrained(bert)
        else:
            self.bert = bert
        self.dropout = nn.Dropout(dropout_prob)
        self.n_classes = n_classes
        self.clf = nn.Linear(self.bert.hidden_size, self.n_classes)

        self.loss_fn = nn.CrossEntropyLoss()
        # 注册到模型变量而非参数，可以享受到 device 的转换
        self.register_buffer("ignore_index", torch.tensor(self.loss_fn.ignore_index))

    def forward(self,
                token_ids: Tensor,
                token_type_ids: Tensor = None,
                token_masks: Tensor = None,
                labels: Tensor = None):
        """
        Args:
            token_ids: [B, L]
            token_type_ids: [B, L]
            token_masks: [B, L]
            labels: [B, L]
        """
        x = self.bert(token_ids,
                      token_type_ids=token_type_ids,
                      token_masks=token_masks,
                      return_value='token_embeddings')  # [B, L, N]
        x = self.dropout(x)  # [B, L, N]
        logits = self.clf(x)  # [B, L, C]

        if labels is not None:
            if token_masks is not None:
                # 把 mask 位置的 label 替换成 ignore_index
                labels = torch.where(token_masks > 0, labels, self.ignore_index.type_as(labels))
            loss = self.loss_fn(logits.view(-1, self.n_classes), labels.view(-1))
            return logits, loss

        return logits


def _test():
    """"""
    doctest.testmod()


if __name__ == '__main__':
    """"""
    _test()
