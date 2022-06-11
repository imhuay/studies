#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Time: 2022-03-09 5:16 下午

Author: huayang

Subject:

"""
import os  # noqa
import doctest  # noqa

# from collections import defaultdict
# from itertools import islice
# from pathlib import Path
from typing import *

# from tqdm import tqdm

import numpy as np

import torch
import torch.nn as nn
import torch.nn.functional as F  # noqa

__all__ = [
    'mixup',
    'mixup_loss',
    'Mixup',
    'MixupLayer'
]


def mixup(x, y, alpha=1.0, mixup_y=True):
    """"""
    lam = np.random.beta(alpha, alpha)  # noqa
    batch_size = x.shape[0]
    idx = np.random.permutation(batch_size)
    x_shuffle, y_shuffle = x[idx], y[idx]
    x_mixup = lam * x + (1 - lam) * x_shuffle

    if mixup_y:
        y_mixup = lam * y + (1 - lam) * y[idx]
        return x_mixup, y_mixup
    else:
        # for mixup_loss
        return x_mixup, y, y_shuffle, lam


def mixup_loss(loss_fn, x_mixup, y, y_shuffle, lam):
    """"""
    return lam * loss_fn(x_mixup, y) + (1 - lam) * loss_fn(x_mixup, y_shuffle)


class Mixup(nn.Module):
    """@Pytorch Utils
    mixup 数据增强策略

    Examples:
        # 示例1: 在数据中混合 y（论文中的用法）
        ```python
        # train in one step
        mixup = Mixup(manifold_mixup=True)
        for x, y in data_loader:
            x, y = mixup(x, y)
            x = model(x)
            loss = loss_fn(x, y)  # 法1）推荐用法
            # loss = mixup.compute_loss(loss_fn, x, y)  # 法2）when `manifold_mixup` is False
            # 法1 是论文中提出的方法，法2 是论文代码中的实现方式；
            # 以上两种计算 loss 的方法在使用 交叉熵 损失时是等价的；
            #   > https://github.com/facebookresearch/mixup-cifar10/issues/18
            ...
        ```

        # 示例：Manifold Mixup，用于中间层混合
        ```
        class ExampleModel(nn.Module):

            def __init__(self, n_layers):
                super().__init__()

                self.n_layers = n_layers
                self.layers = nn.ModuleList([nn.Linear(3, 5) for _ in range(self.n_layers)])
                self.mixup = Mixup(manifold_mixup=True)
                self.loss_fn = nn.CrossEntropyLoss()

            def forward(self, x, y):
                mixup_layer = np.random.randint(self.n_layers)
                for idx, layer in enumerate(self.layers):
                    # mixup once
                    if idx == mixup_layer:
                        x, y = self.mixup(x, y)
                    x = layer(x)

                return self.loss_fn(x, y)
        ```

    References:
        - https://github.com/facebookresearch/mixup-cifar10/blob/main/train.py
        - https://github.com/vikasverma1077/manifold_mixup/blob/master/supervised/utils.py
    """
    lam: Optional[float] = None
    y_shuffle: Optional[torch.Tensor] = None

    def __init__(self, manifold_mixup=True, alpha=1.0):
        super().__init__()
        assert alpha > 0., '`alpha` should be > 0.'
        self.alpha = alpha
        self.manifold_mixup = manifold_mixup

    def forward(self, x, y):
        """"""
        if not self.training:
            return x, y

        if self.manifold_mixup:
            x_mixup, y_mixup = mixup(x, y, self.alpha, mixup_y=True)
            return x_mixup, y_mixup
        else:
            x_mixup, y, y_shuffle, lam = mixup(x, y, self.alpha, mixup_y=False)
            self.y_shuffle, self.lam = y_shuffle, lam
            return x_mixup, y

    def compute_loss(self, loss_fn, x, y):
        """"""
        if self.manifold_mixup:
            return loss_fn(x, y)
        else:
            return mixup_loss(loss_fn, x, y, self.y_shuffle, self.lam)


class MixupLayer(Mixup):
    """"""

    def __init__(self, alpha=1.0):
        super().__init__(manifold_mixup=True, alpha=alpha)


def _test():
    """"""
    doctest.testmod()


if __name__ == '__main__':
    """"""
    _test()
