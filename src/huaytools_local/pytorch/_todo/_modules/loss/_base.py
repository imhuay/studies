#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Time: 2021-10-13 11:45 上午

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
from torch import nn as nn

_EPSILON = 1e-8


class BaseLoss(nn.Module):
    """@Pytorch Loss
    Loss 基类
    """

    def __init__(self, reduction='mean', temperature=1.0):
        """
        Args:
            reduction: 约减类型，以下三者之一：{'mean', 'sum', 'none'}
            temperature: 对 loss 进行缩放，值在 (0, +] 之间，即 `loss = loss / temperature`
        """
        super(BaseLoss, self).__init__()

        if reduction == 'none':
            reduce_fn = lambda x: x
        elif reduction == 'mean':
            reduce_fn = torch.mean
        elif reduction == 'sum':
            reduce_fn = torch.sum
        else:
            raise ValueError(f"reduction={reduction} not in ('mean', 'sum', 'none').")
        self.reduce_fn = reduce_fn

        self.temperature = temperature
        assert self.temperature > 0, f'`temperature` should greater than 0, but {self.temperature}'

    def compute_loss(self, *args, **kwargs):
        raise NotImplementedError

    def forward(self, *args, **kwargs):
        """"""
        loss = self.compute_loss(*args, **kwargs)
        loss = self.reduce_fn(loss)  # reduction
        loss /= self.temperature  # scale
        return loss


def _test():
    """"""
    doctest.testmod()


if __name__ == '__main__':
    """"""
    _test()
