#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Time: 2021-12-21 7:22 下午

Author: huayang

Subject:

"""
import os  # noqa
import doctest  # noqa

from typing import Union, Sequence
# from itertools import islice
# from collections import defaultdict

# from tqdm import tqdm

import torch
import torch.nn as nn

__all__ = [
    'LayerNorm'
]


class LayerNorm(nn.Module):
    """@Pytorch Models
    Layer Normalization

    Almost same as `nn.LayerNorm`
    """

    def __init__(self, norm_shape: Union[int, Sequence[int]], eps=1e-5) -> None:
        """
        Args:
            norm_shape: inputs shape = [*, norm_shape[0], norm_shape[1], .., norm_shape[-1]].
                If norm_shape is int, it will normalize over the last dimension.
                e.g. inputs shape = [2,3,4,5], than norm_shape should be one of {5, [5], [4,5], [3,4,5]}
            eps:

        Examples:
            >>> _ = torch.manual_seed(123)
            >>> t = torch.rand((3,4,5))
            >>> # 把最后一维归一化
            >>> ln = LayerNorm(5)
            >>> o = ln(t)
            >>> torch.allclose(torch.sum(o[0, 0]), torch.tensor(0.), atol=1e-5)
            True
            >>> # 把最后两维归一化
            >>> ln = LayerNorm((4,5))
            >>> o = ln(t)
            >>> torch.allclose(torch.sum(o[0, 0]), torch.tensor(0.), atol=1e-5)
            False
            >>> torch.allclose(torch.sum(o[0]), torch.tensor(0.), atol=1e-5)
            True
        """
        super().__init__()
        if isinstance(norm_shape, int):
            norm_shape = (norm_shape,)
        self.gamma = torch.nn.Parameter(torch.ones(norm_shape))
        self.beta = torch.nn.Parameter(torch.zeros(norm_shape))
        self.dims = tuple(-i for i in range(len(norm_shape), 0, -1))
        self.eps = eps

    def forward(self, inputs: torch.Tensor):
        """"""
        mean = inputs.mean(self.dims, keepdim=True)
        std = inputs.std(self.dims, unbiased=False, keepdim=True)
        return self.gamma * (inputs - mean) / (std + self.eps) + self.beta


def _test():
    """"""
    doctest.testmod()


if __name__ == '__main__':
    """"""
    _test()
