#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Time: 2021-10-15 4:37 下午

Author: huayang

Subject:

"""
import os
import abc
import sys
import json
import doctest

from typing import *
from collections import defaultdict

import torch
from torch.nn import Module
from torch.optim import Optimizer
from torch.utils.data import DataLoader

# from my.pytorch.train.data_utils import DataLoaderDeviceWrapper

MULTI_CPU = "MULTI_CPU"
MULTI_GPU = "MULTI_GPU"
DEEP_SPEED = "DEEP_SPEED"
TPU = "TPU"


class Accelerator(abc.ABC):
    """"""

    def backward(self, loss):
        """"""
        raise NotImplementedError

    def prepare(self, *args):
        """"""
        raise NotImplementedError


class SimpleAccelerator(Accelerator):
    """
    References:
        [huggingface/accelerate](https://github.com/huggingface/accelerate)

    Log:
        - [2021.10.15]
    """

    device: str

    def __init__(self, device: str):
        """"""
        self.device = device

    def backward(self, loss):  # noqa
        loss.backward()

    def prepare(self, *args):
        """"""
        result = tuple(self._prepare_one(obj) for obj in args)
        return result if len(result) > 1 else result[0]

    def _prepare_one(self, obj):
        """"""
        if isinstance(obj, DataLoader):
            return self.prepare_data_loader(obj)
        elif isinstance(obj, Module):
            return self.prepare_model(obj)
        # elif isinstance(obj, Optimizer):
        #     return self.prepare_optimizer(obj)
        else:
            return obj

    def prepare_data_loader(self, data_loader):
        """"""
        # return DataLoaderDeviceWrapper(None)(data_loader, self.device)

    def prepare_model(self, model):
        """"""
        return model.to(self.device)

    def prepare_optimizer(self, optimizer):  # noqa
        """"""
        return optimizer


def _test():
    """"""
    doctest.testmod()


if __name__ == '__main__':
    """"""
    _test()
