#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Time: 2022-05-18 11:31 上午

Author: huayang

Subject:

"""
import os  # noqa
import doctest  # noqa
import itertools

# from collections import defaultdict
# from itertools import islice
# from pathlib import Path
# from typing import *

# from tqdm import tqdm

import torch
import torch.nn as nn
import torch.nn.functional as F  # noqa

import huaytools_local.pytorch.backend as K  # noqa


class ETFLinear(nn.Module):
    """
    References:
        [[2203.09081] Do We Really Need a Learnable Classifier at the End of Deep Neural Network?](https://arxiv.org/abs/2203.09081)
    """

    def __init__(self, d_in, d_out, bias=False, random_seed=None, requires_grad=False):
        """"""
        super().__init__()

        self.weight = torch.nn.Parameter(
            K.simplex_equiangular_tight_frame(d_out, d_in, random_seed=random_seed))
        if bias:
            self.bias = torch.nn.Parameter(torch.zeros(d_out))
        else:
            self.register_parameter('bias', None)
        self.requires_grad_(requires_grad)

    def forward(self, x):
        """"""
        return F.linear(x, self.weight, self.bias)
