#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Time: 2021-10-13 4:04 下午

Author: huayang

Subject:

"""
import doctest

from torch import nn as nn
from torch.nn import functional as F  # noqa

from huaytools_local.pytorch._todo._modules.loss._base import BaseLoss

__all__ = [
    'RDropLoss'
]


class RDropLoss(BaseLoss):
    """

    References:

    """

    def __init__(self, kl_alpha=1.0, reduction='mean', kl_reduction='sum', **base_kwargs):
        """"""
        super().__init__(reduction=reduction, **base_kwargs)

        self.kl_alpha = kl_alpha
        self.ce = nn.CrossEntropyLoss(reduction='none')
        kld_loss = nn.KLDivLoss(reduction='none')
        if kl_reduction == 'sum':
            self.kld = lambda x1, x2: kld_loss(x1, x2).sum(-1)
        elif kl_reduction == 'mean':
            self.kld = lambda x1, x2: kld_loss(x1, x2).mean(-1)
        else:
            raise ValueError('`kl_reduction` should be one of {"sum", "mean"}')

    def compute_loss(self, logits1, logits2, labels):
        """"""
        ce_loss = (self.ce(logits1, labels) + self.ce(logits2, labels)) / 2
        kl_loss1 = self.kld(F.log_softmax(logits1, dim=-1), F.softmax(logits2, dim=-1))
        kl_loss2 = self.kld(F.log_softmax(logits2, dim=-1), F.softmax(logits1, dim=-1))
        return ce_loss + self.kl_alpha * (kl_loss1 + kl_loss2) / 2


def _test():
    """"""
    doctest.testmod()


if __name__ == '__main__':
    """"""
    _test()
