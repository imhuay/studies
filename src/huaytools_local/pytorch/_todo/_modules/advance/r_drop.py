#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Time: 2021-10-11 4:02 下午

Author: huayang

Subject:

"""
import doctest

import torch.nn as nn
import torch.nn.functional as F  # noqa

from huaytools_local.pytorch._todo._modules import RDropLoss


class RDrop(nn.Module):

    def __init__(self, encoder, kl_alpha=1.0):
        super().__init__()

        self.encoder = encoder
        self.kl_alpha = kl_alpha
        self.ce = nn.CrossEntropyLoss()
        self.kl = nn.KLDivLoss()

    def forward(self, x, labels):
        logits1 = self.encoder(x)
        logits2 = self.encoder(x)
        ce_loss = (self.ce(logits1, labels) + self.ce(logits2, labels)) / 2
        kl_loss1 = self.kl(F.log_softmax(logits1, dim=-1), F.softmax(logits2, dim=-1))
        kl_loss2 = self.kl(F.log_softmax(logits2, dim=-1), F.softmax(logits1, dim=-1))
        return ce_loss + self.kl_alpha * (kl_loss1 + kl_loss2) / 2


class RDrop_(nn.Module):
    """"""

    def __init__(self, encoder, **loss_kwargs):
        """"""
        super().__init__()

        self.encoder = encoder
        self.loss_fn = RDropLoss(**loss_kwargs)

    def forward(self, inputs, labels=None):
        """"""
        logits1 = self.encoder(**inputs)

        if labels is not None:
            logits2 = self.encoder(**inputs)
            loss = self.loss_fn(logits1, logits2, labels)

            return logits1, logits2, loss

        return logits1


def _test():
    """"""
    doctest.testmod()


if __name__ == '__main__':
    """"""
    _test()
