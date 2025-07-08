#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Time: 2022-05-19 2:30 下午

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


def test_ETFLinear():  # noqa
    import torch
    import torch.nn as nn
    from huaytools_local.pytorch._todo.modules import ETFLinear

    l1 = ETFLinear(4, 5)
    l2 = nn.Linear(4, 5, bias=False)
    # for k, v in l1.named_parameters():
    #     print(k, v)
    # for k, v in l2.named_parameters():
    #     print(k, v)
    l2.weight = l1.weight
    # for k, v in l2.named_parameters():
    #     print(k, v)
    x = torch.randn(3, 4)
    o1 = l1(x)
    o2 = l2(x)
    assert torch.allclose(o1, o2)
