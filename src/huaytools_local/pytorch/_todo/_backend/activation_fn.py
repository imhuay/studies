#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Time:
    2021-08-12 10:43 上午

Author:
    huayang

Subject:

"""
import math
import doctest

import torch
import torch.nn.functional as F

from torch import Tensor

from huaytools_local.pytorch.utils import get_torch_version


def gelu(x: Tensor):
    """
    Examples:
         >>> inputs = torch.rand(3, 2)
         >>> assert torch.allclose(gelu(inputs), F.gelu(inputs))  # 会有一点微小的误差

     References: https://arxiv.org/pdf/1606.08415.pdf
    """
    return x * 0.5 * (1 + torch.erf(x / math.sqrt(2)))


def gelu_approximate(x: Tensor):
    """ Approximation of gelu.

    Examples:
        >>> inputs = torch.rand(3, 2)
        >>> assert torch.allclose(gelu_approximate(inputs), F.gelu(inputs), atol=1e-3)

    References: https://arxiv.org/pdf/1606.08415.pdf
    """
    # 0.7978845608 ~= math.sqrt(2.0 / math.pi)
    return 0.5 * x * (1.0 + torch.tanh(0.7978845608 * (x + 0.044715 * x.pow(3.0))))


def gelu_quick(x):
    """ Approximation of gelu.

    Examples:
        >>> inputs = torch.rand(3, 2)
        >>> assert torch.allclose(gelu_quick(inputs), F.gelu(inputs), atol=1e-2)

    References: https://arxiv.org/pdf/1606.08415.pdf
    """
    return x * torch.sigmoid(1.702 * x)


def linear(x: Tensor):
    """"""
    return x


ACT_STR2FN = {
    'relu': F.relu,
    'gelu': F.gelu,
    'gelu_approximate': gelu_approximate,
    'gelu_quick': gelu_quick,
    'linear': linear,
    'sigmoid': torch.sigmoid,
    'tanh': torch.tanh,
}

if get_torch_version() >= '1.7.0':
    ACT_STR2FN['silu'] = F.silu

if get_torch_version() >= '1.9.0':
    ACT_STR2FN['mish'] = F.mish


def _test():
    """"""
    doctest.testmod()


if __name__ == '__main__':
    """"""
    _test()
