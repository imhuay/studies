#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Time:
    2021-06-27 8:32 下午
    
Author:
    huayang
    
Subject:
    
"""
import math

import torch
import torch.nn as nn

__all__ = [
    'MultiHeadAttention',
]


class MultiHeadAttention(nn.Module):
    """

    Examples:
        >>> cell = MultiHeadAttention(2, 4)

        # q == k == v
        >>> q = torch.rand(2, 3, 8)  # 2 * 4 == 8
        >>> masks = torch.rand(2, 3)
        >>> o = cell(q, q, q, masks=masks)
        >>> o.shape
        torch.Size([2, 3, 8])

        # q != k != v
        >>> q = torch.rand(2, 3, 8)  # seq_len_from = 3
        >>> k = torch.rand(2, 4, 8)  # seq_len_to = 4
        >>> v = torch.rand(2, 4, 8)
        >>> masks = torch.rand(2, 3, 4)
        >>> o = cell(q, k, v, masks=masks)
        >>> o.shape
        torch.Size([2, 3, 8])

        # Tracing
        >>> _ = cell.eval()  # avoid TracerWarning
        >>> ex_q = torch.rand(3, 5, 8)
        >>> ex_masks = torch.rand(3, 5)
        >>> traced_cell = torch.jit.trace(cell, (ex_q, ex_q, ex_q, ex_masks))
        >>> q = torch.rand(5, 6, 8)
        >>> masks = torch.rand(5, 6)
        >>> torch.equal(traced_cell(q, q, q, masks), cell(q, q, q, masks))
        True

        # >>> print(traced_attn.code)

    References:
        "Attention is All You Need"
    """
    attention_score: torch.Tensor = None

    def __init__(self,
                 num_attention_heads=12,
                 hidden_size_per_head=64,  # default 64*12=768
                 dropout_prob=0.1):
        """"""
        super().__init__()

        self.num_attention_heads = num_attention_heads
        self.hidden_size_per_head = hidden_size_per_head
        self.hidden_size = self.num_attention_heads * self.hidden_size_per_head  # equal to `hidden_size`

        self.q_dense = nn.Linear(self.hidden_size, self.hidden_size)
        self.k_dense = nn.Linear(self.hidden_size, self.hidden_size)
        self.v_dense = nn.Linear(self.hidden_size, self.hidden_size)
        self.o_dense = nn.Linear(self.hidden_size, self.hidden_size)

        self.dropout = nn.Dropout(dropout_prob)
        self.softmax = nn.Softmax(-1)

    def forward(self, q, k, v, masks=None):
        """
        Args:
            q: [B, F, hidden_size]
            k: [B, T, hidden_size], `F == T` mostly
            v: same shape as k
            masks: 0/1 value tensor with
                [B, F] or [B, 1, 1, F] when `F == T`
                [B, F, T] or [B, 1, F, T] when `F != T`
        """
        if masks is not None:
            assert 2 <= masks.ndim <= 4
            if masks.ndim == 2:  # [B, F]
                masks = masks[:, None, None, :]  # [B, 1, 1, F]
            elif masks.ndim == 3:  # [B, F, T]
                masks = masks[:, None, :, :]  # [B, 1, F, T]

        # dims
        B = q.shape[0]  # batch_size
        LF = q.shape[1]  # seq_len_from (query)
        LT = v.shape[1]  # seq_len_to (key, value)
        N = self.hidden_size_per_head
        H = self.num_attention_heads

        # multi-head linear
        q = self.q_dense(q).reshape([B, LF, H, N]).transpose(1, 2)  # [B, H, LF, N]
        k = self.k_dense(k).reshape([B, LT, H, N]).transpose(1, 2)  # [B, H, LT, N]
        v = self.v_dense(v).reshape([B, LT, H, N]).transpose(1, 2)  # [B, H, LT, N]

        # multi-head scaled dot-product attention
        a = torch.matmul(q, k.transpose(-1, -2))  # [B, H, LF, N] x [B, H, N, LT] -> [B, H, LF, LT]
        a = a / math.sqrt(self.hidden_size_per_head)  # scale

        if masks is not None:
            a = a.masked_fill(masks == 0, -1e12)

        self.attention_score = self.softmax(a)  # [B, H, LF, LT]
        a = self.dropout(self.attention_score)

        # outputs
        o = torch.matmul(a, v)  # [B, H, LF, LT] x [B, H, LT, N] -> [B, H, LF, N]
        o = o.transpose(1, 2).reshape([B, LF, H * N])  # [B, H, LF, N] -> [B, LF, H, N] -> [B, LF, H*N]
        o = self.o_dense(o)  # linear

        return o
