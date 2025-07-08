#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Time: 2022-06-05 3:08 上午

Author: huayang

Subject:

"""
import os  # noqa
import doctest  # noqa

# from collections import defaultdict
# from itertools import islice
# from pathlib import Path
# from typing import *

# from tqdm import tqdm


import numpy as np
import torch

from scipy import linalg


def simplex_equiangular_tight_frame(k, d, as_tensor=True, random_seed=None):
    """
    生成单纯型等角紧框架
    返回矩阵 M（k 个 d 维向量）
    满足如下性质：对任意 i,j
        当 i == j 时，有 M[i] @ M[j].T == 1
        当 i != j 时，有 M[i] @ M[j].T == -1/(k-1)

    Examples:
        >>> k, d = 4, 5  # noqa
        >>> M = simplex_equiangular_tight_frame(k, d)  # noqa
        >>> for i in range(k):
        ...     for j in range(k):
        ...         if i == j: assert np.isclose(M[i] @ M[j].T, 1.)  # noqa
        ...         else: assert np.isclose(M[i] @ M[j].T, -1/(k-1))

    Args:
        k: k 个向量
        d: 每个向量的维度，assert k <= d + 1
        as_tensor:
        random_seed:

    Returns:
        shape [k, d]

    References:
        Do We Really Need a Learnable Classifier at the End of Deep Neural Network?
    """
    assert k <= d + 1, 'assert k <= d + 1'
    # 生成随机矩阵
    # A = np.random.normal(k, d)
    rs = np.random.RandomState(seed=random_seed)
    A = rs.normal(size=(k, d))
    # 通过极分解得到酉矩阵 U
    U, _ = linalg.polar(A)  # [k, d]
    # 计算 EFT
    M = np.sqrt(k / (k - 1)) * (np.eye(k) - np.ones(k) / k) @ U  # [k, d]
    return torch.as_tensor(M, dtype=torch.float32) if as_tensor else M


if __name__ == '__main__':
    """"""
    doctest.testmod()
