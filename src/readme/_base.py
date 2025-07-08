#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Time:
    2022-10-13 20:58
Author:
    huayang (imhuay@163.com)
Subject:
    _base
"""
from __future__ import annotations


# import os
# import sys
# import json
# import unittest

# from typing import *
# from pathlib import Path
# from collections import defaultdict


class Builder:

    def build(self):
        raise NotImplementedError

    @property
    def readme_append(self):
        raise NotImplementedError


def build(*readmes: Builder):
    [r.build() for r in readmes]
