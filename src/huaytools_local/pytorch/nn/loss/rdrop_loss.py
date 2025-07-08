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


class RDropLoss(nn.Module):
    """
    References:
        [dropreg/R-Drop](https://github.com/dropreg/R-Drop)
    """

    def __init__(self, alpha=1.0, ce_reduce_fn=torch.mean, kl_reduce_fn=torch.sum, mask_value=0):
        """"""
        super().__init__()

        self.alpha = alpha
        self.cross_entropy = nn.CrossEntropyLoss(reduction='none')
        self.ce_reduce_fn = ce_reduce_fn
        self.kl_reduce_fn = kl_reduce_fn
        self.mask_value = mask_value

    def compute_ce_loss(self, logits1, logits2, labels):
        ce_loss = 0.5 * (self.cross_entropy(logits1, labels) + self.cross_entropy(logits2, labels))
        return self.ce_reduce_fn(ce_loss)

    def compute_kl_loss(self, logits1, logits2, masks):
        kl_loss = K.compute_kl_loss(logits1, logits2, masks, self.mask_value)
        return self.kl_reduce_fn(kl_loss)

    def forward(self, logits1, logits2, labels, masks=None):
        """"""
        ce_loss = self.compute_ce_loss(logits1, logits2, labels)
        kl_loss = self.compute_kl_loss(logits1, logits2, masks)
        return ce_loss + self.alpha * kl_loss
