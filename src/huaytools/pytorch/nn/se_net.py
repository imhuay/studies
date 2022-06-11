#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Time: 2022-03-15 5:13 下午

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

import torch
import torch.nn as nn
import torch.nn.functional as F  # noqa


class SENet1D(nn.Module):
    """@Pytorch Models
    SENETLayer used in FiBiNET.

    References:
        https://github.com/shenweichen/DeepCTR-Torch/blob/master/deepctr_torch/layers/interaction.py#L64
    """

    def __init__(self, filed_size, embedding_size, reduction_ratio=3,
                 mode='mean', use_bias=False):
        """
        Args:
            filed_size: number of feature groups
            embedding_size:
            reduction_ratio: dimensionality of the attention network output space
            mode: 'mean' or 'max'
            use_bias:
        """
        super().__init__()

        self.filed_size = filed_size
        self.reduction_size = max(1, filed_size // reduction_ratio)
        self.excitation = nn.Sequential(
            nn.Linear(self.filed_size, self.reduction_size, bias=use_bias),
            nn.ReLU(),
            nn.Linear(self.reduction_size, self.filed_size, bias=use_bias),
            nn.ReLU()
        )
        if mode == 'mean':
            self.pooling = nn.AvgPool1d(embedding_size)
        elif mode == 'max':
            self.pooling = nn.MaxPool1d(embedding_size)
        else:
            assert mode in ('mean', 'max'), f'`mode` should be one of ("max", "mean"), but {mode}'

    def forward(self, inputs):
        """
        Args:
            inputs: [B, filed_size, embedding_size]

        Returns:
            [B, filed_size, embedding_size]
        """
        assert inputs.ndim == 3, f'`inputs` should to be 3 dim, but {inputs.ndim}'
        Z = self.pooling(inputs).squeeze(-1)  # [B, L, N] -> [B, L]
        A = self.excitation(Z)  # [B, L] -> [B, L]
        return inputs * A.unsqueeze(-1)  # [B, L, N] * [B, L, 1]


class SENet2D(nn.Module):  # TODO
    """"""

    def __init__(self):
        """"""
        super().__init__()


if __name__ == '__main__':
    """"""
    doctest.testmod()
