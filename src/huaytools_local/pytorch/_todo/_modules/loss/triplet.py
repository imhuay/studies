#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Time: 2021-10-13 4:02 下午

Author: huayang

Subject:

"""
import doctest

import torch
import torch.nn as nn
import torch.nn.functional as F  # noqa

from huaytools_local.pytorch._todo._backend.distance_fn import euclidean_distance_nosqrt
from huaytools_local.pytorch._todo._modules.loss._base import BaseLoss

__all__ = [
    'TripletLoss'
]


def triplet_loss(anchor, positive, negative, distance_fn=F.pairwise_distance, margin=2.0):
    """  triplet 损失

    Examples:
        >>> a = torch.randn(100, 128)
        >>> p = torch.randn(100, 128)
        >>> n = torch.randn(100, 128)
        >>> # 官方提供的 triplet_loss
        >>> tl = nn.TripletMarginLoss(margin=2.0, p=2, reduction='none')
        >>> assert torch.allclose(triplet_loss(a, p, n), tl(a, p, n), atol=1e-5)
        >>> # 官方提供的 triplet_loss: 自定义距离函数
        >>> from huaytools_local.pytorch.backend import cosine_distance
        >>> tld = nn.TripletMarginWithDistanceLoss(distance_function=cosine_distance, margin=2.0, reduction='none')
        >>> assert torch.allclose(triplet_loss(a, p, n, distance_fn=cosine_distance), tld(a, p, n), atol=1e-5)

    Args:
        anchor:
        positive:
        negative:
        distance_fn:
        margin:

    Returns:
        [B] tensor

    Examples:
        anchor = torch.randn(100, 128)
        positive = torch.randn(100, 128)
        negative = torch.randn(100, 128)

        # 自定义距离
        from my.pytorch.backend.distance_fn import cosine_distance

        # 官方
        tld = nn.TripletMarginWithDistanceLoss(distance_function=cosine_distance, margin=2.0, reduction='none')
        o = tld(anchor, positive, negative)

        # my
        triplet_loss(anchor, positive, negative, distance_fn=cosine_distance)

    """
    distance_pos = distance_fn(anchor, positive)
    distance_neg = distance_fn(anchor, negative)
    return torch.relu(distance_pos - distance_neg + margin)


class TripletLoss(BaseLoss):
    """@Pytorch Loss
    Triplet 损失，常用于无监督学习、few-shot 学习

    Examples:
        >>> anchor = torch.randn(100, 128)
        >>> positive = torch.randn(100, 128)
        >>> negative = torch.randn(100, 128)

        # my_tl 默认 euclidean_distance_nosqrt
        >>> tl = TripletLoss(margin=2., reduction='none')
        >>> tld = nn.TripletMarginWithDistanceLoss(distance_function=euclidean_distance_nosqrt,
        ...                                        margin=2., reduction='none')
        >>> assert torch.allclose(tl(anchor, positive, negative), tld(anchor, positive, negative), atol=1e-5)

        # 自定义距离函数
        >>> from huaytools_local.pytorch.backend.distance_fn import cosine_distance
        >>> my_tl = TripletLoss(distance_fn=cosine_distance, margin=0.5, reduction='none')
        >>> tl = nn.TripletMarginWithDistanceLoss(distance_function=cosine_distance, margin=0.5, reduction='none')
        >>> assert torch.allclose(my_tl(anchor, positive, negative), tl(anchor, positive, negative), atol=1e-5)

    """

    def __init__(self, distance_fn=euclidean_distance_nosqrt, margin=1.0, **kwargs):
        """"""
        self.margin = margin
        self.distance_fn = distance_fn

        super(TripletLoss, self).__init__(**kwargs)

    def compute_loss(self, anchor, positive, negative):
        return triplet_loss(anchor, positive, negative,
                            distance_fn=self.distance_fn, margin=self.margin)


def _test():
    """"""
    doctest.testmod()


if __name__ == '__main__':
    """"""
    _test()
