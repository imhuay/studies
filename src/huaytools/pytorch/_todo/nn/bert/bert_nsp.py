#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Time: 2021-11-03 5:31 下午

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

__all__ = [
    'BertNSP',
    'NextSentencePrediction'
]


class BertNSP(nn.Module):
    """"""
    # TODO


class NextSentencePrediction(nn.Module):
    """ Bert Next sentence Prediction（未测试） """

    def __init__(self, hidden_size=768, num_classes=2):
        """"""
        super().__init__()
        self.dense = nn.Linear(hidden_size, num_classes)

    def forward(self, cls_embedding, labels=None):
        """"""
        logits = self.dense(cls_embedding)

        if labels is not None:
            loss = self.loss_fn(logits, labels)
            return logits, loss

        return logits


def _test():
    """"""
    doctest.testmod()


if __name__ == '__main__':
    """"""
    _test()
