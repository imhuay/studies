#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Time: 2021-10-13 4:01 下午

Author: huayang

Subject:

"""
import doctest

from torch.nn import functional as F  # noqa

from huaytools_local.pytorch._todo._backend.distance_fn import euclidean_distance
from huaytools_local.pytorch._todo._modules.loss._base import BaseLoss

__all__ = [
    'ContrastiveLoss'
]


def contrastive_loss(x1, x2, labels, distance_fn=euclidean_distance, margin=2.0):
    """ 对比损失 (0 <= label <= 1)
        - 当 y=1（即样本相似）时，如果距离较大，则加大损失；
        - 当 y=0（即样本不相似）时，如果距离反而小，也会增大损失；

    Args:
        x1:
        x2:
        labels:
        distance_fn: 默认为欧几里得距离
        margin: 需要根据使用距离函数调整

    Returns:

    """
    labels = labels.float()
    distances = distance_fn(x1, x2)
    return 0.5 * (labels * distances.pow(2) + (1 - labels) * F.relu(margin - distances).pow(2))


class ContrastiveLoss(BaseLoss):
    """@Pytorch Loss
    对比损失（默认距离函数为欧几里得距离）
    """

    def __init__(self, distance_fn=euclidean_distance, margin=1.0, **kwargs):
        """"""
        self.margin = margin
        self.distance_fn = distance_fn
        self.loss_fn = lambda x1, x2, labels: contrastive_loss(x1, x2, labels,
                                                               distance_fn=self.distance_fn,
                                                               margin=self.margin)
        super(ContrastiveLoss, self).__init__(**kwargs)

    def compute_loss(self, x1, x2, labels):
        return self.loss_fn(x1, x2, labels)


def _test():
    """"""
    doctest.testmod()


if __name__ == '__main__':
    """"""
    _test()
