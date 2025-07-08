#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Time:
    2022-10-13 0:55
Author:
    huayang (imhuay@163.com)
Subject:
    add_section_for_notes
"""
from __future__ import annotations

import os
# import os
# import sys
# import json
# import unittest

# from typing import *
from pathlib import Path


# from collections import defaultdict


def main():
    """"""
    cnt = 0
    n_modify = 0
    for dp, _, fns in os.walk(r'../../notes/_archives'):
        for fn in fns:
            fp = Path(dp) / fn
            if fp.suffix != '.md':
                continue
            cnt += 1
            n_modify += foo_one(fp)

    assert cnt == n_modify


def foo_one(fp: Path):
    """"""
    with fp.open(encoding='utf8') as f:
        txt = f.read()

    lns = txt.split('\n', maxsplit=2)
    if lns[1].strip() != '===':
        print(fp)
        return 0
    lns.insert(2, '<!--START_SECTION:badge-->\n<!--END_SECTION:badge-->')

    with fp.open('w', encoding='utf8') as f:
        f.write('\n'.join(lns))

    return 1


def _test():
    """"""
    fp = Path(r'../../notes/_archives/2022/10/XGBoost备忘.md')
    foo_one(fp)


if __name__ == '__main__':
    """"""
    # _test()
    main()
