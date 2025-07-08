#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Time:
    2021-07-02 10:16 上午
    
Author:
    huayang
    
Subject:
    孪生网络

References:
    - [adambielski/siamese-triplet: Siamese and triplet networks with online pair/triplet mining in PyTorch](https://github.com/adambielski/siamese-triplet)
    - [PyTorch练手项目四：孪生网络（Siamese Network） - 天地辽阔 - 博客园](https://www.cnblogs.com/inchbyinch/p/12116339.html)
"""

from huaytools_local.pytorch.loss import ContrastiveLoss
from huaytools_local.pytorch._todo._modules import DualNet
from huaytools_local.pytorch._todo._backend.distance_fn import euclidean_distance

__all__ = [
    'SiameseNet'
]


class SiameseNet(DualNet):
    """@Pytorch Models
    孪生网络，基于双塔结构
    """

    def __init__(self, encoder, **kwargs):
        kwargs.setdefault('loss_fn', ContrastiveLoss(distance_fn=euclidean_distance, margin=2.0))
        super(SiameseNet, self).__init__(encoder_q=encoder, **kwargs)


def _test():
    """"""

    def _test_bert():
        """"""
        from huaytools_local.pytorch._todo._modules import get_bert_pretrained
        bert = get_bert_pretrained()

        sn = SiameseNet(encoder=bert)

    _test_bert()


if __name__ == '__main__':
    """"""
