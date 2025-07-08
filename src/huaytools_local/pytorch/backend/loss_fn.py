#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Time: 2022-06-05 2:58 上午

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
import torch.nn as nn
import torch.nn.functional as F  # noqa


def compute_triplet_loss(anchor, positive, negative, distance_fn=None, margin=2.0, reduce_fn=None):
    """  triplet 损失

    Examples:
        >>> from huaytools_local.pytorch.backend import cosine_distance
        >>> a, p, n = torch.randn(10, 12), torch.randn(10, 12), torch.randn(10, 12)
        >>> # 官方 triplet_loss
        >>> tl = nn.TripletMarginLoss(margin=2.0, p=2, reduction='none')
        >>> assert torch.allclose(compute_triplet_loss(a, p, n), tl(a, p, n), atol=1e-5)
        >>> # 官方支持自定义距离的 triplet_loss
        >>> tld = nn.TripletMarginWithDistanceLoss(distance_function=cosine_distance, margin=2.0, reduction='none')
        >>> assert torch.allclose(compute_triplet_loss(a, p, n, distance_fn=cosine_distance), tld(a, p, n), atol=1e-5)

    Args:
        anchor:
        positive:
        negative:
        distance_fn:
        margin:
        reduce_fn: such `torch.mean` or `torch.sum`

    Returns:
        [B] tensor

    """
    if distance_fn is None:
        distance_fn = F.pairwise_distance

    distance_pos = distance_fn(anchor, positive)
    distance_neg = distance_fn(anchor, negative)
    loss = torch.relu(distance_pos - distance_neg + margin)

    if reduce_fn is not None:
        loss = reduce_fn(loss)
    return loss


def compute_kl_loss(p, q, masks=None, mask_value=0, reduce_fn=None):
    """
    References:
        [dropreg/R-Drop](https://github.com/dropreg/R-Drop)

    Args:
        p:
        q:
        masks:
        mask_value:
        reduce_fn: torch.sum or torch.mean

    Returns:
    """
    p_loss = F.kl_div(F.log_softmax(p, dim=-1), F.softmax(q, dim=-1), reduction='none')
    q_loss = F.kl_div(F.log_softmax(q, dim=-1), F.softmax(p, dim=-1), reduction='none')

    if masks is not None:
        p_loss.masked_fill_(masks, mask_value)
        q_loss.masked_fill_(masks, mask_value)

    if reduce_fn is not None:
        p_loss = reduce_fn(p_loss)
        q_loss = reduce_fn(q_loss)

    return 0.5 * (p_loss + q_loss)


if __name__ == '__main__':
    """"""
    doctest.testmod()
