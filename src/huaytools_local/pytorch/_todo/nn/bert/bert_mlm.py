#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Time: 2021-11-03 5:31 下午

Author: huayang

Subject:

"""
import os
import sys
import json
import doctest

from typing import *
from collections import defaultdict

import torch
import torch.nn as nn
import torch.nn.functional as F  # noqa
from torch import Tensor

__all__ = [
    'BertMLM',
    'MaskedLanguageModel'
]


class BertMLM(nn.Module):
    """"""
    # TODO


class MaskedLanguageModel(nn.Module):
    """ Bert Masked Language Model（未测试） """

    def __init__(self, hidden_size,
                 word_embeddings: Tensor,
                 share_word_embeddings=False,
                 activation_fn=F.gelu,
                 layer_norm_eps=1e-12):
        """"""
        super().__init__()

        self.act_fn = activation_fn
        self.dense = nn.Linear(hidden_size, hidden_size)
        self.LayerNorm = nn.LayerNorm(hidden_size, eps=layer_norm_eps)

        # 如果 word_embeddings_weight 不为 None
        vocab_size, embedding_size = word_embeddings.shape[0], word_embeddings.shape[1]
        assert hidden_size == embedding_size

        self.decoder = nn.Linear(embedding_size, vocab_size, bias=False)
        self.embedding_size = embedding_size

        # transformers 的实现是没有共享的，只是用来初始化；而 unilm 里是共享的
        self.share_word_embeddings = share_word_embeddings
        if not self.share_word_embeddings:
            word_embeddings = word_embeddings.clone()

        self.decoder.weight.data = word_embeddings
        self.decoder.bias = nn.Parameter(torch.zeros(vocab_size))
        # self.decoder.weight.data = word_embeddings
        # 这里 embedding_size 不需要参与训练，所以直接覆盖 weight，而不是 weight.data

        self.loss_fn = nn.CrossEntropyLoss()

    def forward(self, token_embeddings, labels=None):
        """
        Args:
            token_embeddings: [B, L, N]
            labels: [B, L]
        """
        x = token_embeddings  # [B L N]
        x = self.dense(x)  # [B L N]
        x = self.act_fn(x)  # [B L N]
        x = self.LayerNorm(x)  # [B L N]
        logits = self.decoder(x)  # [B L N] x [N V] = [B L V] where V = vocab_size

        if labels is not None:
            loss = self.loss_fn(logits.view(-1, self.embedding_size), labels.view(-1))
            return logits, loss

        return logits


def _test():
    """"""
    doctest.testmod()


if __name__ == '__main__':
    """"""
    _test()
