#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Time: 2021-10-13 8:32 下午

Author: huayang

Subject:

"""
import os
import sys
import json
import doctest

from typing import *
from collections import defaultdict

import torch.nn.functional as F  # noqa


def kl_div_loss(p, q, masks=None):
    """"""
    p_loss = F.kl_div(F.log_softmax(p, dim=-1), F.softmax(q, dim=-1), reduction='none')
    q_loss = F.kl_div(F.log_softmax(q, dim=-1), F.softmax(p, dim=-1), reduction='none')

    # pad_mask is for seq-level tasks
    if masks is not None:
        p_loss.masked_fill_(masks, 0.)
        q_loss.masked_fill_(masks, 0.)

    # You can choose whether to use function "sum" and "mean" depending on your task
    p_loss = p_loss.sum()
    q_loss = q_loss.sum()

    loss = (p_loss + q_loss) / 2
    return loss


def _test():
    """"""
    doctest.testmod()


if __name__ == '__main__':
    """"""
    _test()
