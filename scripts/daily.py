#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Time:
    2022-08-22 20:14
Author:
    huayang (imhuay@163.com)
Subject:
    build_readme
"""
import os
import sys
import json
import time
import doctest
import subprocess

from typing import *
from pathlib import Path
from itertools import islice
from collections import defaultdict

from huaytools.utils import get_logger

# try:
#     sys.path.insert(0, f'{Path(__file__).parent.parent / "src"}')
# except:  # noqa
#     exit(1)
# else:
from readme.build import BuildReadme

logger = get_logger()

if __name__ == '__main__':
    """"""
    br = BuildReadme()
    br.build()
    br.git_push()
    logger.info(f'Update Success!')
