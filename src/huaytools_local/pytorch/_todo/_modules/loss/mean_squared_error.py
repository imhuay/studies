#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Time: 2021-10-13 8:33 下午

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
import torch.nn.functional as F  # noqa


def mean_squared_error_loss(inputs, targets):
    """ 平方差损失

    Examples:
        >>> i = torch.randn(3, 5)
        >>> t = torch.randn(3, 5)

        # 与官方结果比较
        >>> my_ret = mean_squared_error_loss(i, t)
        >>> official_ret = F.mse_loss(i, t, reduction='none')
        >>> assert torch.allclose(my_ret, official_ret, atol=1e-5)

    Args:
        inputs: [B, N]
        targets: same shape as inputs

    Returns:
        [B, N]
    """
    return (inputs - targets).pow(2.0)


def _test():
    """"""
    doctest.testmod()


if __name__ == '__main__':
    """"""
    _test()
