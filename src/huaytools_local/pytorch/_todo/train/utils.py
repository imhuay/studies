#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Time: 2021-10-18 11:56 上午

Author: huayang

Subject:

"""
import os
from typing import Iterable

import torch
import torch.nn as nn
from torch import optim

from huaytools_local._python import get_time_string
from huaytools_local.pytorch.utils import default_device

__all__ = [
    'get_optimizer_by_name',
    'get_parameters_for_weight_decay',
    'get_model_save_dir',
    'default_device',
    'STR2OPT'
]


def get_parameters_for_weight_decay(model: nn.Module, learning_rate, weight_decay, no_decay_params: Iterable[str]):
    """"""
    named_parameters = list(model.named_parameters())
    # apply weight_decay
    parameters = [
        {
            'params': [p for n, p in named_parameters if not any(nd in n for nd in no_decay_params)],
            'weight_decay': weight_decay,
            'lr': learning_rate
        },
        {
            'params': [p for n, p in named_parameters if any(nd in n for nd in no_decay_params)],
            'weight_decay': 0.0,
            'lr': learning_rate
        }
    ]

    return parameters


DEFAULT_SAVE_DIR = os.path.join(os.environ['HOME'], 'out/models')


def get_model_save_dir():
    return os.path.join(DEFAULT_SAVE_DIR, f'model-{get_time_string(fmt="%Y%m%d%H%M%S")}')


STR2OPT = {
    'Adam': optim.Adam,
    'AdamW': optim.AdamW,
    'SGD': optim.SGD,
}


def get_optimizer_by_name(opt_name: str):
    """"""
    if opt_name in STR2OPT:
        return STR2OPT[opt_name]

    try:
        return getattr(optim, opt_name)
    except:
        raise ValueError(f'No Optimizer named `{opt_name}` in `torch.optim`.')
