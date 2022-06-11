#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Time:
    2021-06-30 5:32 下午
    
Author:
    huayang
    
Subject:
    
"""

import torch
import torch.nn as nn
import torch.nn.functional as F  # noqa
from torch import Tensor

from .multi_head_attention import MultiHeadAttention
from .feed_forward import FeedForward

__all__ = [
    'Transformer',
]


class Transformer(nn.Module):
    """

    Examples:
        >>> hidden_size = 4
        >>> cell = Transformer(hidden_size, 2, 10)

        >>> inputs = torch.randn(2, 3, hidden_size)
        >>> masks = torch.randn(2, 3)
        >>> o = cell(inputs, masks=masks)
        >>> o.shape
        torch.Size([2, 3, 4])

        # Tracing
        >>> _ = cell.eval()  # avoid TracerWarning
        >>> traced_cell = torch.jit.trace(cell, (inputs, masks))
        >>> inputs = torch.rand(5, 6, hidden_size)
        >>> masks = torch.rand(5, 6)
        >>> torch.equal(traced_cell(inputs, masks), cell(inputs, masks))
        True

    References:
        "Attention is all you need"
    """

    def __init__(self,
                 hidden_size=768,
                 num_attention_heads=12,
                 intermediate_size=3072,
                 activation_fn=F.gelu,
                 dropout_prob=0.1,
                 attention_dropout_prob=0.1,
                 layer_norm_eps=1e-12,
                 mode='post_ln'):
        """"""
        super().__init__()
        assert hidden_size > num_attention_heads and hidden_size % num_attention_heads == 0
        self.attention = MultiHeadAttention(num_attention_heads, hidden_size // num_attention_heads,
                                            dropout_prob=attention_dropout_prob)
        self.attention_LayerNorm = nn.LayerNorm(hidden_size, eps=layer_norm_eps)

        self.ffn = FeedForward(hidden_size, intermediate_size, activation_fn)
        self.ffn_LayerNorm = nn.LayerNorm(hidden_size, eps=layer_norm_eps)

        self.dropout = nn.Dropout(dropout_prob)

        """
        Post-LN: Attn -> Drop -> Add -> LN -> FFN -> Drop -> Add -> LN
        Pre-LN:  LN -> Attn -> Add -> Drop -> LN -> FFN -> Add -> Drop
        
        两者区别参考：On Layer Normalization in the Transformer Architecture
        """
        assert mode in ('post_ln', 'pre_ln')
        self.forward_fn = getattr(self, mode)
        self.mode = mode

    def forward(self, inputs: Tensor, masks: Tensor = None):
        """
        Args:
            inputs: [B, L, N]
            masks: 0/1 value tensor with shape [B, L]
        """
        return self.forward_fn(inputs, masks)

    def post_ln(self, inputs, masks):
        """"""
        x = inputs
        x = self.attention(x, x, x, masks)
        x = self.dropout(x) + inputs
        x = self.attention_LayerNorm(x)

        inputs = x
        x = self.ffn(x)
        x = self.dropout(x) + inputs
        x = self.ffn_LayerNorm(x)
        return x

    def pre_ln(self, inputs, masks):
        """"""
        x = inputs
        x = self.attention_LayerNorm(x)
        x = self.attention(x, x, x, masks)
        x = self.dropout(x) + inputs

        inputs = x
        x = self.ffn_LayerNorm(x)
        x = self.ffn(x)
        x = self.dropout(x) + inputs
        return x
