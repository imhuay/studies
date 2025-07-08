#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Time: 2022-06-05 2:39 上午

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

import torch
import torch.nn as nn


def default_optimizer(model, optimizer_type, learning_rate, weight_decay, no_decay_params):
    """"""
    parameters = get_parameters_for_weight_decay(model, learning_rate,
                                                 weight_decay, no_decay_params)
    optimizer = get_optimizer_by_name(optimizer_type)(parameters)
    return optimizer


def default_scheduler(optimizer, num_warmup_steps, num_train_steps):
    """"""
    from huaytools_local.pytorch.train.scheduler import get_linear_schedule_with_warmup
    scheduler = get_linear_schedule_with_warmup(optimizer, num_warmup_steps, num_train_steps)
    return scheduler


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


def get_optimizer_by_name(opt: Union[str, type]):
    """"""
    if isinstance(opt, type):
        return opt
    else:
        try:
            return getattr(torch.optim, opt)
        except:
            raise ValueError(f'No Optimizer named `{opt}` in `torch.optim`.')


if __name__ == '__main__':
    """"""
    doctest.testmod()
