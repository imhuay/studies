#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Time: 2021-10-13 11:13 上午

Author: huayang

Subject:

"""

from ._base import BaseLoss
from .contrastive import ContrastiveLoss
from .cross_entropy import CrossEntropyLoss
from .r_drop import RDropLoss
from .triplet import TripletLoss
