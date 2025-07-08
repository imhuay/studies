#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Time: 2022-05-20 12:28 下午

Author: huayang

Subject:

"""
import os  # noqa
import doctest  # noqa


# from collections import defaultdict
# from itertools import islice
# from pathlib import Path
# from typing import *

# from tqdm import tqdm

import torch
import torch.nn.functional as F

from huaytools_local.pytorch._todo.modules import RDropLoss


def rdrop_loss_official(logits, logits2, label, alpha=1.0):
    def compute_kl_loss(p, q, pad_mask=None):

        p_loss = F.kl_div(F.log_softmax(p, dim=-1), F.softmax(q, dim=-1), reduction='none')
        q_loss = F.kl_div(F.log_softmax(q, dim=-1), F.softmax(p, dim=-1), reduction='none')

        # pad_mask is for seq-level tasks
        if pad_mask is not None:
            p_loss.masked_fill_(pad_mask, 0.)
            q_loss.masked_fill_(pad_mask, 0.)

        # You can choose whether to use function "sum" and "mean" depending on your task
        p_loss = p_loss.mean()
        q_loss = q_loss.mean()

        loss = (p_loss + q_loss) / 2
        return loss

    # cross entropy loss for classifier
    ce_loss = 0.5 * (F.cross_entropy(logits, label, reduction='sum') + F.cross_entropy(logits2, label, reduction='sum'))
    kl_loss = compute_kl_loss(logits, logits2)
    # carefully choose hyper-parameters
    loss = ce_loss + alpha * kl_loss
    return loss


def test_RDropLoss():
    alpha = 0.8
    logits1 = torch.randn(3, 5, requires_grad=True)
    logits2 = torch.randn(3, 5, requires_grad=True)
    labels = torch.empty(3, dtype=torch.long).random_(5)
    rl = RDropLoss(alpha, ce_reduce_fn=torch.sum, kl_reduce_fn=torch.mean)
    o1 = rl(logits1, logits2, labels)
    o2 = rdrop_loss_official(logits1, logits2, labels, alpha)
    assert torch.allclose(o1, o2)






class Demo:
    def __init__(self):
        """"""
        doctest.testmod()


if __name__ == '__main__':
    """"""
    Demo()
