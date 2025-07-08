#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Time:
    2023-06-26 21:30
Author:
    huayang (imhuay@163.com)
Subject:
    inline
References:
    None
"""

from __future__ import annotations

# from typing import *
# from pathlib import Path
# from itertools import islice
# from collections import defaultdict


def ifn(any, default):
    """if None"""
    return default if any is None else any