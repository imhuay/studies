#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Time: 2022-05-18 10:57 上午

Author: huayang

Subject:

"""
import math

# from collections import defaultdict
# from itertools import islice
# from pathlib import Path
from typing import *

# from tqdm import tqdm

import torch
import torch.nn as nn
import torch.nn.functional as F  # noqa

from torch import Tensor

from huaytools_local.pytorch.backend.loss_fn import (
    compute_triplet_loss,
    compute_kl_loss
)
from huaytools_local.pytorch.backend.activation_fn import (
    gelu,
    gelu_quick,
    gelu_approximate
)
from huaytools_local.pytorch.backend.simple_etf import simplex_equiangular_tight_frame


def truncated_normal(x: Tensor, mean=0., std=1., a=-2., b=2.):
    """"""
    nn.init.trunc_normal_(x, mean=mean, std=std, a=a, b=b)
    return x


def identity(x):
    """
    恒等

    Args:
        x:

    Returns:
        x
    """
    return x


def permute(x: Tensor, dims: Union[list, tuple]):
    """
    对比 `transpose()`, `transpose()` 一次只能调整两个维度，而 permute 可以调整多个

    Examples: x.shape = [2, 3, 4, 5]
        dims=[0, 2, 1, 3]   -> [2, 4, 3, 5]  # 等价于 x.transpose(2, 1)
        dims=[1, 0, 3, 2]   -> [3, 2, 5, 4]
        dims=[0, 1, -1, -2] -> [2, 3, 5, 4]  # 等价于 x.transpose(-1, -2)
    """
    return x.permute(*dims)


def repeat(x: Tensor, sizes: Union[list, tuple]):
    """
    按 sizes 的顺序成倍扩充数据，需要注意顺序
        similar to `np.tile()`, but differently from `np.repeat()`
    Examples: x = torch.tensor([1, 2, 3])  # shape=[3]
        sizes=[3, 2]    -> 依次对 dim=-1 扩充至 2倍，dim=-2 扩充至 3倍 -> [3, 6]
        sizes=[3, 2, 1] -> 依次对 dim=-1 保持不变，dim=1 扩充至 2倍，dim=2 扩充至 3 倍 -> [3, 2, 3]

    References:
        https://pytorch.org/docs/stable/generated/torch.Tensor.repeat.html
    """
    return x.repeat(*sizes)


def squeeze(x: Tensor, dim: Optional[int] = None):
    """
    Examples: x.shape = [B, 1, N, 1]
        dim=None    -> [B, N]
        dim=1       -> [B, N, 1]
        dim=-1      -> [B, 1, N]
        dim=0       -> [B, 1, N, 1]
    """
    return x.squeeze(dim)


def unsqueeze(x: Tensor, dim):
    """
    Examples:
        dim=0:  [B, N, ..] -> [1, B, N, ..]
        dim=1:  [B, N, ..] -> [B, 1, N, ..]
        dim=-1: [B, N, ..] -> [B, N, .., 1]
    """
    return x.unsqueeze(dim)


def transpose(x: Tensor, dim0: int, dim1: int):
    """
    Examples: x.shape = [B, L, N, C]
        x.transpose(1, 2)   -> [B, N, L, C]
        x.transpose(1, 3)   -> [B, C, N, L]
        x.transpose(-1, -2) -> [B, L, C, N]
        x.transpose(-2, -1) -> [B, L, C, N]
    """
    return x.transpose(dim0, dim1)


def l2_norm(x: Tensor, dim=-1, eps=1e-12):
    """
    L2 归一化

    Args:
        x: [B, N] or [N]
        dim:
        eps:

    """
    # return F.normalize(x, p=2.0, dim=dim)  # F.normalize 默认就是 L2 正则
    norm = x.norm(p=2.0, dim=dim, keepdim=True).clamp_min(eps).expand_as(x)
    return x / norm


def inf_norm(x: Tensor, dim=-1, eps=1e-12):
    """

    Args:
        x:
        dim:
        eps:

    """
    # return F.normalize(x, p=float('inf'), dim=dim)
    norm = x.norm(p=float('inf'), dim=dim, keepdim=True).clamp_min(eps).expand_as(x)
    return x / norm


class __distance_or_similarity_fn__:  # noqa
    """分隔线，无实际意义"""


def euclidean_distance(x1, x2, sqrt=True):
    """
    欧氏距离
        same as `F.pairwise_distance(p=2)`

    Args:
        x1: [B, N] or [N]
        x2: same shape as x1
        sqrt: 是否对结果开放，默认 True

    Returns:
        [B] vector or scalar
    """
    r = (x1 - x2).pow(2).sum(-1)
    return r.pow(0.5) if sqrt else r


def euclidean_distance_nosqrt(x1, x2):  # noqa
    """"""
    return euclidean_distance(x1, x2, False)


def cosine_similarity(x1, x2, dim=-1):
    """
    cosine 相似度
        same as `F.cosine_similarity`

    Args:
        x1: [B, N] or [N]
        x2: same shape as x1
        dim: 默认 -1

    Returns:
        [B] vector or scalar

    Examples:
        >>> x = torch.as_tensor([1, 2, 3]).to(torch.float)
        >>> y = torch.as_tensor([9, 8, 7]).to(torch.float)
        >>> torch.allclose(cosine_similarity(x, y), F.cosine_similarity(x, y, dim=0))
        True
        >>> x = torch.as_tensor([[1, 2, 3], [4, 5, 6], [7, 8, 9]]).to(torch.float)
        >>> y = torch.as_tensor([[9, 8, 7], [6, 5, 4], [3, 2, 1]]).to(torch.float)
        >>> torch.allclose(cosine_similarity(x, y), F.cosine_similarity(x, y, dim=1))
        True
        >>>
    """
    x1_normalized = l2_norm(x1, dim=dim)
    x2_normalized = l2_norm(x2, dim=dim)
    return (x1_normalized * x2_normalized).sum(dim)


def cosine_distance(x1, x2, dim=-1):
    """
    cosine 距离
        same as `1 - cosine_similarity(x1, x2)`
    """
    return 1 - cosine_similarity(x1, x2, dim=dim)


def cosine_similarity_dense(x1, x2):
    """
    cosine 距离（全连接）
        即 x1 中每个向量与 x2 中每个向量计算 cosine 距离，相当于计算一个 attention 矩阵
        等价于 `F.cosine_similarity(x1.unsqueeze(1), x1.unsqueeze(0), dim=-1)`
    Args:
        x1: [B1, N]
        x2: [B2, N]

    Returns:
        [B1, B2] matrix
    """
    assert x1.ndim == x2.ndim == 2

    x1_normalized = l2_norm(x1, dim=-1)  # [B1, N]
    x2_normalized_T = l2_norm(x2, dim=-1).T  # [N, B2]
    return torch.matmul(x1_normalized, x2_normalized_T)  # [B1, B2]
