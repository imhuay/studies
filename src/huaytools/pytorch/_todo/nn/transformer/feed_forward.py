#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Time: 2021-11-03 10:32 上午

Author: huayang

Subject:

"""
import os
import sys
import json
import doctest

from typing import *
from collections import defaultdict

import torch.nn as nn


class FeedForward(nn.Module):
    """ Position Wise Feed Forward """

    def __init__(self, hidden_size, intermediate_size, activation_fn):
        super().__init__()

        self.W1 = nn.Linear(hidden_size, intermediate_size)
        self.W2 = nn.Linear(intermediate_size, hidden_size)
        self.act = activation_fn

    def forward(self, inputs):
        """"""
        x = self.W2(self.act(self.W1(inputs)))
        return x
