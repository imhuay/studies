#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Time:
    2022-08-19 18:35
Author:
    huayang (imhuay@163.com)
Subject:
    init_utils
"""
import os
import sys
import json
import time
import doctest

from typing import *
from pathlib import Path
from itertools import islice
from collections import defaultdict

import torch
import torch.nn as nn


class InitUtils:
    """"""

    @staticmethod
    def init_weights(module: nn.Module, normal_std=0.02):
        """@Pytorch Utils
        默认参数初始化

        Examples:
            >>> model = nn.Transformer()
            >>> _ = model.apply(init_weights)

        Args:
            module:
            normal_std:

        References: Bert
        """
        if isinstance(module, nn.Linear):
            # truncated_normal
            nn.init.trunc_normal_(module.weight.data, std=normal_std)
            if module.bias is not None:
                module.bias.data.zero_()
        elif isinstance(module, nn.Embedding):
            # truncated_normal
            nn.init.trunc_normal_(module.weight.data, std=normal_std)
            if module.padding_idx is not None:
                module.weight.data[module.padding_idx].zero_()
        elif isinstance(module, nn.LayerNorm):
            module.weight.data.fill_(1.0)
            module.bias.data.zero_()
        else:
            pass  # default


class __Test:
    """"""

    def __init__(self):
        """"""
        for k, v in self.__class__.__dict__.items():
            if k.startswith('_test') and isinstance(v, Callable):
                print(f'\x1b[32m=== Start "{k}" {{\x1b[0m')
                start = time.time()
                v(self)
                print(f'\x1b[32m}} End "{k}" - Spend {time.time() - start:3f}s===\x1b[0m\n')

    def _test_doctest(self):  # noqa
        """"""
        import doctest
        doctest.testmod()

    def _test_xxx(self):  # noqa
        """"""
        pass


if __name__ == '__main__':
    """"""
    __Test()
