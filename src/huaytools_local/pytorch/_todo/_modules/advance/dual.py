#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Time:
    2021-09-03 6:47 下午

Author:
    huayang

Subject:

"""
from typing import Callable

from torch import nn as nn

from huaytools_local.pytorch._todo._backend.distance_fn import cosine_distance
from huaytools_local.pytorch.loss import ContrastiveLoss

__all__ = [
    'DualNet'
]


class DualNet(nn.Module):
    """@Pytorch Models
    双塔结构
    """

    def __init__(self,
                 encoder_q,
                 encoder_d=None,
                 loss_fn=ContrastiveLoss(distance_fn=cosine_distance, margin=0.5),
                 encode_wrapper_q: Callable = None,
                 encode_wrapper_d: Callable = None):
        """
        
        Args:
            encoder_q: encoder for query
            encoder_d: encoder for doc
            loss_fn:
        """
        super(DualNet, self).__init__()

        self.encoder_q = encoder_q
        self.encoder_d = encoder_d
        self.loss_fn = loss_fn

        if encode_wrapper_q is not None:
            self.encode_wrapper_q = encode_wrapper_q
        if encode_wrapper_d is not None:
            self.encode_wrapper_d = encode_wrapper_d

    def forward(self, x1, x2, labels):
        """ assert 0 <= label <= 1 """
        o1 = self.get_embedding_q(x1)
        o2 = self.get_embedding_d(x2)
        return self.loss_fn(o1, o2, labels)

    def get_embedding_q(self, x):
        return self.encode_wrapper_q(self.encoder_q, x)

    def get_embedding_d(self, x):
        encoder = self.encoder_d if self.encoder_d is not None else self.encoder_q
        return self.encode_wrapper_d(encoder, x)

    def encode_wrapper_q(self, encoder, inputs):
        """ Overwrite when `inputs` not match the `encoder` """
        try:
            return encoder(*inputs)
        except:
            raise NotImplementedError(f'It seems that `inputs` not match the `encoder`, '
                                      f'overwrite the `{self.encode_wrapper.__name__}` function.')

    def encode_wrapper_d(self, encoder, inputs):
        """ default same as encode_wrapper_q """
        return self.encode_wrapper_q(encoder, inputs)


def _test():
    """"""

    def _test_base():
        """"""
        from huaytools_local.pytorch._todo._modules import get_bert_pretrained
        bert = get_bert_pretrained()

        def fn():
            print(1)

        ds = DualNet(encoder_q=bert, encode_wrapper_q=fn)

        sd = ds.state_dict()
        print(len(sd))

        ds.encode_wrapper_q()

    _test_base()


if __name__ == '__main__':
    """"""
    _test()
