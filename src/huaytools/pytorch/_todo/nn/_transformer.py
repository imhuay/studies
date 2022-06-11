#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Time: 2021-12-24 2:48 下午

Author: huayang

Subject:

References:
    - [The Illustrated Transformer](http://jalammar.github.io/illustrated-transformer/)
    - [The Annotated Transformer](http://nlp.seas.harvard.edu/2018/04/03/attention.html)
"""
import os  # noqa
import doctest  # noqa
import math

# from typing import *
# from itertools import islice
# from collections import defaultdict

# from tqdm import tqdm

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

from torch import Tensor

__all__ = [
    'EncodeLayer',
    'MultiHeadAttention',
    'ScaledDotProductAttention',
    'FeedForwardLayer',
]


def generate_square_subsequent_mask(sz):
    """
    Generate square subsequent mask, and the `True` value means should be attend,
        different from `nn.Transformer.generate_square_subsequent_mask` where 0 value means should be attend

    Args:
        sz: target sequence length

    Returns:
        [sz, sz] bool tensor where `True` value means should be attend

    Examples:
        >>> generate_square_subsequent_mask(3)
        tensor([[ True, False, False],
                [ True,  True, False],
                [ True,  True,  True]])

    References:
        nn.Transformer.generate_square_subsequent_mask
    """
    return torch.triu(torch.ones((sz, sz), dtype=torch.uint8), diagonal=1) == 0


class Transformer(nn.Module):
    """"""

    def __init__(self):
        """"""
        super().__init__()

    def forward(self):
        """"""


class EncodeLayer(nn.Module):
    """"""

    def __init__(self,
                 num_heads,
                 hidden_size,
                 hidden_size_ff,
                 dropout_prob=0.1,
                 dropout_prob_ffn=0.1,
                 dropout_prob_attn=0.1,
                 activation_fn=F.gelu,
                 layer_norm_eps=1e-9,
                 norm_first=False):
        """"""
        super().__init__()

        self.attn = MultiHeadAttention(hidden_size, num_heads, dropout_prob=dropout_prob_attn)
        self.ffn = FeedForwardLayer(hidden_size, hidden_size_ff, dropout_prob=dropout_prob_ffn)
        self.LayerNorm_1 = nn.LayerNorm(hidden_size, eps=layer_norm_eps)
        self.LayerNorm_2 = nn.LayerNorm(hidden_size, eps=layer_norm_eps)
        self.dropout = nn.Dropout(dropout_prob)

        self.act = activation_fn
        self.norm_first = norm_first

    def forward(self, x: Tensor, padding_mask=None, attn_mask=None):
        """
        Args:
            x: [B, L, N]
            padding_mask: [B, L]
            attn_mask:

        Returns:
            [B, L, N]

        Notes:
            Pre-LN:  LN -> SA -> Add -> LN -> FFN -> Add
            Post-LN: SA -> Add -> LN -> FFN -> Add -> LN

        References:
            On Layer Normalization in the Transformer Architecture
        """
        if self.norm_first:
            x = x + self.dropout(self.attn(self.LayerNorm_1(x), padding_mask=padding_mask, attn_mask=attn_mask))
            x = x + self.dropout(self.ffn(self.LayerNorm_2(x)))
        else:  # default
            x = self.LayerNorm_1(x + self.dropout(self.attn(x, padding_mask=padding_mask, attn_mask=attn_mask)))
            x = self.LayerNorm_2(x + self.dropout(self.ffn(x)))
        return x


class DecodeLayer(nn.Module):
    """
    Examples:
        >>> num_heads, hidden_size, hidden_size_ff = 3, 12, 24
        >>> net = DecodeLayer(num_heads, hidden_size, hidden_size_ff)
        >>> x = torch.randn(2, 5, hidden_size)
        >>> m = torch.randn(2, 6, hidden_size)
        >>> o = net(x, m)
        >>> o.shape
        torch.Size([2, 5, 12])

        # Tracing
        >>> traced_net = torch.jit.trace(net.eval(), (x, m))
        >>> x = torch.rand(3, 4, 12)
        >>> m = torch.rand(3, 5, 12)
        >>> torch.equal(traced_net(x, m), net(x, m))
        True

        # >>> print(traced_net.code)
    """

    def __init__(self,
                 num_heads,
                 hidden_size,
                 hidden_size_ff,
                 dropout_prob=0.1,
                 dropout_prob_ffn=0.1,
                 dropout_prob_attn=0.1,
                 use_subsequent_mask=True,
                 activation_fn=F.gelu,
                 layer_norm_eps=1e-9,
                 norm_first=False):
        """"""
        super().__init__()

        self.attn_1 = MultiHeadAttention(hidden_size, num_heads, dropout_prob=dropout_prob_attn)
        self.attn_2 = MultiHeadAttention(hidden_size, num_heads, dropout_prob=dropout_prob_attn)
        self.ffn = FeedForwardLayer(hidden_size, hidden_size_ff, dropout_prob=dropout_prob_ffn)
        self.LayerNorm_1 = nn.LayerNorm(hidden_size, eps=layer_norm_eps)
        self.LayerNorm_2 = nn.LayerNorm(hidden_size, eps=layer_norm_eps)
        self.LayerNorm_3 = nn.LayerNorm(hidden_size, eps=layer_norm_eps)
        self.dropout = nn.Dropout(dropout_prob)

        self.use_subsequent_mask = use_subsequent_mask
        self.act = activation_fn
        self.norm_first = norm_first

    def forward(self, x: Tensor, memory: Tensor, mask=None, memory_mask=None):
        """
        Args:
            x: [B, T, N] 
            memory: [B, S, N]
            mask: int/bool tensor where `1/True` value means should be attend,
                If shape [B, T] means just padding-mask.
                If shape [B, T, T] means subsequent-mask & padding-mask,
                    then `self.use_subsequent_mask` should be set False.
            memory_mask: [B, S]

        Returns:
            [B, T, N]
        """
        if self.use_subsequent_mask:
            subsequent_mask = generate_square_subsequent_mask(x.shape[1]).unsqueeze(0)  # [1, T, T]
            if mask is None:
                mask = subsequent_mask
            else:
                if mask.ndim == 2:
                    mask = mask.unsqueeze(1)  # [B, T] -> [B, 1, T]
                mask = mask & subsequent_mask  # [B, 1, T] & [1, T, T] -> [B, T, T]

        if self.norm_first:
            x = x + self.dropout(self.attn_1(self.LayerNorm_1(x), mask=mask))
            x = x + self.dropout(self.attn_2(self.LayerNorm_2(x), memory, mask=memory_mask))
            x = x + self.dropout(self.ffn(self.LayerNorm_3(x)))
        else:  # default
            x = self.LayerNorm_1(x + self.dropout(self.attn_1(x, mask=mask)))
            x = self.LayerNorm_2(x + self.dropout(self.attn_2(x, memory, mask=memory_mask)))
            x = self.LayerNorm_3(x + self.dropout(self.ffn(x)))
        return x


class MultiHeadAttention(nn.Module):
    """

    Examples:
        >>> net = MultiHeadAttention(8, 2)

        # q != k != v
        >>> q = torch.rand(2, 3, 8)  # seq_len_from = 3
        >>> k = torch.rand(2, 4, 8)  # seq_len_to = 4
        >>> v = torch.rand(2, 4, 8)
        >>> mask = torch.rand(2, 3, 4)
        >>> o = net(q, k, v, mask=mask)
        >>> o.shape
        torch.Size([2, 3, 8])

        # q == k == v
        >>> q = torch.rand(2, 3, 8)
        >>> mask = torch.rand(2, 3)
        >>> o = net(q, q, q, mask=mask)
        >>> o.shape
        torch.Size([2, 3, 8])

        # Tracing
        >>> traced_net = torch.jit.trace(net.eval(), (q, q, q, mask))
        >>> q = torch.rand(5, 6, 8)  # hidden_size should be same
        >>> mask = torch.rand(5, 6)
        >>> torch.equal(traced_net(q, q, q, mask), net(q, q, q, mask))
        True

        # 与官方结果对比
        >>> _test_MultiHeadAttention()

        # >>> print(traced_net.attention.code)

    """
    attention_score: torch.Tensor

    def __init__(self, hidden_size=512, num_heads=8, dropout_prob=0.1):
        """"""
        super().__init__()

        self.num_heads = num_heads
        self.hidden_size = hidden_size

        assert hidden_size % num_heads == 0
        self.hidden_size_per_head = hidden_size // num_heads

        self.attention = ScaledDotProductAttention(dropout_prob=dropout_prob)
        self.linear_q = nn.Linear(self.hidden_size, self.hidden_size)
        self.linear_k = nn.Linear(self.hidden_size, self.hidden_size)
        self.linear_v = nn.Linear(self.hidden_size, self.hidden_size)
        self.linear_o = nn.Linear(self.hidden_size, self.hidden_size)

        self.dropout = nn.Dropout(dropout_prob)
        self.softmax = nn.Softmax(-1)

    def forward(self, q, k=None, v=None, padding_mask=None, attn_mask=None, ignore_value=0):
        """
        Args:
            q: [B, T, hidden_size]
            k: [B, S, hidden_size], default None using q
            v: [B, S, hidden_size], default None using k
            padding_mask: [B, S] or [B, T, S] int/bool/float tensor.
                For a int/bool mask, the value equal to `ignore_idx` is not allowed to attend,
                    while a float mask will be added to the attention weight.
                In Multi-head Attention, a 2D mask will extend to [B, 1, 1, S] broadcast to batch and head dim,
                    while a 3D mask will extend to [B, 1, T, S] broadcast to head dim
                    which allowing a different mask for each entry in the batch.
            attn_mask:
            ignore_value:

        Returns:
            [B, T, hidden_size]
        """
        k = q if k is None else k
        v = k if v is None else v

        # dims
        B = q.shape[0]  # batch_size
        T = q.shape[1]  # target sequence length
        S = k.shape[1]  # source sequence length
        H = self.num_heads
        N = self.hidden_size_per_head

        # multi-head linear
        q = self.linear_q(q).reshape([B, T, H, N]).transpose(1, 2)  # [B, H, T, N]
        k = self.linear_k(k).reshape([B, S, H, N]).transpose(1, 2)  # [B, H, S, N]
        v = self.linear_v(v).reshape([B, S, H, N]).transpose(1, 2)  # [B, H, S, N]

        o = self.attention(q, k, v,
                           padding_mask=padding_mask, attn_mask=attn_mask, ignore_value=ignore_value)  # [B, H, T, N]
        o = self.linear_o(o.transpose(1, 2).reshape([B, T, H * N]))
        return o  # [B, T, hidden_size]


class ScaledDotProductAttention(nn.Module):
    """ Scaled Dot-Product Attention

    References:
        [Attention Is All You Need](https://arxiv.org/abs/1706.03762)
    """
    attention_score: torch.Tensor

    def __init__(self, dropout_prob=0.1, neg_inf=-1e9):
        """"""
        super().__init__()
        self.softmax = nn.Softmax(dim=-1)
        self.dropout = nn.Dropout(dropout_prob)
        self.neg_inf = neg_inf

    def forward(self, q, k, v, padding_mask=None, attn_mask=None, ignore_value=0):
        """
        Args:
            q: [B, *, T, N]
            k: [B, *, S, N]
            v: [B, *, S, N]
            padding_mask: [B, *, S] or [B, *, T, S] int/bool/float tensor.
                For float tensor, the ignore position can be set a big negitive value or `-inf`.
                For int tensor, the ignore position should be equal to `ignore_value`(default 0).
                For bool tensor, when `ignore_value=1` means the `True` position is ignored,
                    any other `ignore_value` means the `False` position is ignored.
            attn_mask:
            ignore_value: default 0

        Returns:
            [B, *, T, N]

        Examples:
            >>> net = ScaledDotProductAttention()
            >>> q1 = torch.randn(2,3,8)
            >>> o = net(q1, q1, q1)
            >>> o.shape
            torch.Size([2, 3, 8])
            >>> q1 = torch.randn(2,3,4,8)
            >>> o = net(q1, q1, q1)
            >>> o.shape
            torch.Size([2, 3, 4, 8])
            >>> q1 = torch.randn(2,3,4,5,8)
            >>> o = net(q1, q1, q1)
            >>> o.shape
            torch.Size([2, 3, 4, 5, 8])

        """
        # [B, *, T, N] x [B, *, N, S] -> [B, *, T, S]
        d_k = q.shape[-1]
        k_T = k.transpose(-2, -1)  # [B, *, S, N] -> [B, *, N, S]
        logits = torch.matmul(q, k_T) / np.sqrt(d_k)  # `math.sqrt` no diff but cause TracerWarning

        if padding_mask is not None:
            # extending mask
            if padding_mask.ndim < q.ndim:
                n_extend = q.ndim - padding_mask.ndim
                for _ in range(n_extend):
                    padding_mask = padding_mask.unsqueeze(1)  # `mask.unsqueeze_(1)` can cause TracingError

            if torch.is_floating_point(padding_mask):
                logits = logits + padding_mask
            else:
                logits = logits.masked_fill(padding_mask == ignore_value, self.neg_inf)

        if attn_mask is not None:
            attn_mask = attn_mask[None, None, :, :]
            logits += attn_mask  # logits.masked_fill(attn_mask == ignore_value, self.neg_inf)

        self.attention_score = self.softmax(logits)  # [B, *, T, S]
        probs = self.dropout(self.attention_score)
        return torch.matmul(probs, v)  # [B, *, T, S] x [B, *, S, N] -> [B, *, T, N]


class FeedForwardLayer(nn.Module):
    """ Position-Wise Feed Forward Network

    References:
        [Attention Is All You Need](https://arxiv.org/abs/1706.03762)
    """

    def __init__(self, d_model=512, d_ff=2048, dropout_prob=0.1, activation_fn=F.relu):
        super().__init__()

        self.W_1 = nn.Linear(d_model, d_ff)
        self.W_2 = nn.Linear(d_ff, d_model)
        self.dropout = nn.Dropout(dropout_prob)
        self.act = activation_fn

    def forward(self, x):
        """
        Args:
            x: [batch_size, *, d_model]

        Returns:
            [batch_size, *, d_model]

        Examples:
            >>> ffn = FeedForwardLayer(6, 10)
            >>> o = ffn(torch.rand(3, 5, 6))
            >>> o.shape
            torch.Size([3, 5, 6])

        """
        return self.dropout(self.W_2(self.dropout(self.act(self.W_1(x)))))


@torch.no_grad()
def _test_MultiHeadAttention():  # noqa
    torch.random.manual_seed(1234)

    attn = MultiHeadAttention(3, 3).eval()
    attnN = nn.MultiheadAttention(3, 3, batch_first=True).eval()

    # === 替换参数 ===
    in_weight = torch.concat([attn.linear_q.weight, attn.linear_k.weight, attn.linear_v.weight], dim=0)
    in_bias = torch.concat([attn.linear_q.bias, attn.linear_k.bias, attn.linear_v.bias], dim=0)
    attnN.in_proj_weight = nn.Parameter(in_weight)
    attnN.in_proj_bias = nn.Parameter(in_bias)
    attnN.out_proj.weight = attn.linear_o.weight
    attnN.out_proj.bias = attn.linear_o.bias
    # ===

    # === 构造输入 ===
    padding_mask = torch.randn(2, 5) > 0
    attn_mask_b = torch.randn(5, 5) > 0
    attn_mask = torch.zeros(5, 5).masked_fill(attn_mask_b, -1e9)
    print(attn_mask)
    # mask = torch.bitwise_or(padding_mask[:, None, None, :], attn_mask_b[None, None, :, :])
    x = torch.arange(1, 31).view(2, 5, 3).to(torch.float)

    o = attn(x, padding_mask=padding_mask, attn_mask=None, ignore_value=1)
    o2, a = attnN(x, x, x, key_padding_mask=padding_mask, attn_mask=None)
    print(o)
    print(o2)
    print(attn.attention.attention_score)
    print(a)
    assert torch.allclose(o, o2, atol=1e-5)


def _test():
    """"""
    # doctest.testmod()

    _test_MultiHeadAttention()


if __name__ == '__main__':
    """"""
    _test()
