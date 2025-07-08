#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Time:
    2021-07-01 11:10 上午
    
Author:
    huayang
    
Subject:
    torch.Tensor 相关操作（备忘，有些操作的智能提示不完善）

References:
    [torch.Tensor](https://pytorch.org/docs/stable/tensors.html)
"""
import doctest

import torch
import torch.nn as nn

from typing import *

from torch import Tensor

from torch.nn import functional as F

List = Union[list, tuple]


def concat(tensors, dim=-1):
    """"""
    return torch.cat(tensors, dim=dim)


def l2_normalize(x: Tensor, dim=-1):
    """ L2 归一化

    Args:
        x: [B, N] or [N]
        dim:

    """
    return F.normalize(x, p=2.0, dim=dim)  # F.normalize 默认就是 L2 正则


def ndim(x: Tensor):
    """ same as x.dim()
    Examples:
        x.shape = [B, N]    -> x.ndim = 2
        x.shape = [B, L, C] -> x.ndim = 3
    """
    return x.ndim


def permute(x: Tensor, dims: List):
    """ 对比 `transpose()`, `transpose()` 一次只能调整两个维度，而 permute 可以调整多个
    Examples: x.shape = [2, 3, 4, 5]
        dims=[0, 2, 1, 3]   -> [2, 4, 3, 5]  # 等价于 x.transpose(2, 1)
        dims=[1, 0, 3, 2]   -> [3, 2, 5, 4]
        dims=[0, 1, -1, -2] -> [2, 3, 5, 4]  # 等价于 x.transpose(-1, -2)
    """
    return x.permute(*dims)


def repeat(x: Tensor, sizes: List):
    """ 按 sizes 的顺序成倍扩充数据，需要注意顺序
        similar to `np.tile()`, but differently from `np.repeat()`
    Examples: x = torch.tensor([1, 2, 3])  # shape=[3]
        sizes=[3, 2]    -> 依次对 dim=-1 扩充至 2倍，dim=-2 扩充至 3倍 -> [3, 6]
        sizes=[3, 2, 1] -> 依次对 dim=-1 保持不变，dim=1 扩充至 2倍，dim=2 扩充至 3 倍 -> [3, 2, 3]

    References:
        https://pytorch.org/docs/stable/generated/torch.Tensor.repeat.html
    """
    return x.repeat(*sizes)


def reshape(x: Tensor, new_shape: List):
    """
    assert np.prod(x.shape) == np.prod(new_shape)  # np.prod() 表示连乘
    """
    return x.reshape(new_shape)


def shape(x: Tensor):
    """ same as x.size()
    Assert:
        x.shape == x.size
        x.shape[0] == x.size(0)
        x.shape[-1] == x.size(-1)
    """
    return x.shape


def squeeze(x: Tensor, dim: Optional[int] = None):
    """
    Examples: x.shape = [B, 1, N, 1]
        dim=None    -> [B, N]
        dim=1       -> [B, N, 1]
        dim=-1      -> [B, 1, N]
        dim=0       -> [B, 1, N, 1]
    """
    return x.squeeze(dim)


def truncated_normal(x: Tensor, mean=0., std=1., a=-2., b=2.):
    """"""
    nn.init.trunc_normal_(x, mean=mean, std=std, a=a, b=b)
    return x


def to_dtype(x: Tensor, dtype):
    """ convert tensor dtype """
    return x.to(dtype)


def transpose(x: Tensor, dim0: int, dim1: int):
    """
    Examples: x.shape = [B, L, N, C]
        x.transpose(1, 2)   -> [B, N, L, C]
        x.transpose(1, 3)   -> [B, C, N, L]
        x.transpose(-1, -2) -> [B, L, C, N]
        x.transpose(-2, -1) -> [B, L, C, N]
    """
    return x.transpose(dim0, dim1)


def unsqueeze(x: Tensor, dim):
    """
    Examples:
        dim=0:  [B, N, ..] -> [1, B, N, ..]
        dim=1:  [B, N, ..] -> [B, 1, N, ..]
        dim=-1: [B, N, ..] -> [B, N, .., 1]
    """
    return x.unsqueeze(dim)


def _test():
    """"""

    def _test_permute():
        """"""
        t = torch.randn([2, 3, 4])
        x = permute(t, (1, 0))
        print(x.shape)

    _test_permute()


if __name__ == '__main__':
    """"""
    _test()
