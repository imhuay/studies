#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Time: 2022-06-05 3:05 上午

Author: huayang

Subject:

"""
import os  # noqa
import doctest  # noqa
import math

# from collections import defaultdict
# from itertools import islice
# from pathlib import Path
# from typing import *

# from tqdm import tqdm


import torch
import torch.nn.functional as F  # noqa

from torch import Tensor


def gelu(x: Tensor):
    """
    Examples:
         >>> inputs = torch.rand(3, 2)
         >>> assert torch.allclose(gelu(inputs), F.gelu(inputs))  # 会有一点微小的误差

     References: https://arxiv.org/pdf/1606.08415.pdf
    """
    return x * 0.5 * (1 + torch.erf(x / math.sqrt(2)))


def gelu_approximate(x: Tensor):
    """
    Approximation of gelu.

    Examples:
        >>> inputs = torch.rand(3, 2)
        >>> assert torch.allclose(gelu_approximate(inputs), F.gelu(inputs), atol=1e-3)

    References: https://arxiv.org/pdf/1606.08415.pdf
    """
    # 0.7978845608 ~= math.sqrt(2.0 / math.pi)
    return 0.5 * x * (1.0 + torch.tanh(0.7978845608 * (x + 0.044715 * x.pow(3.0))))


def gelu_quick(x):
    """
    Approximation of gelu.

    Examples:
        >>> inputs = torch.rand(3, 2)
        >>> assert torch.allclose(gelu_quick(inputs), F.gelu(inputs), atol=1e-2)

    References: https://arxiv.org/pdf/1606.08415.pdf
    """
    return x * torch.sigmoid(1.702 * x)


if __name__ == '__main__':
    """"""
    doctest.testmod()
