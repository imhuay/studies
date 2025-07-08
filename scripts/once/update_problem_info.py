#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Time:
    2022-09-29 13:43
Author:
    huayang (imhuay@163.com)
Subject:
    update_problem_info
"""
from __future__ import annotations

import os
import re
# import sys
import json
# import unittest

# from typing import *
# from collections import defaultdict
from pathlib import Path

import yaml

from huaytools_local.utils import NoIndentJSONEncoder

fp_problems = Path(r'../../algorithms/problems')
RE_INFO = re.compile(r'<!--(.*?)-->', flags=re.DOTALL)

new_info_temp = '''<!--info
{info}
-->'''


def json_info(info):
    info['tags'] = NoIndentJSONEncoder.wrap(info['tags'])
    info['companies'] = NoIndentJSONEncoder.wrap(info['companies'])
    return json.dumps(info, indent=4, ensure_ascii=False,
                      cls=NoIndentJSONEncoder)


def yaml_info(info):
    if not info['companies']:
        info['companies'] = []
    tags = info.pop('tags')
    coms = info.pop('companies')
    no = info.pop('number')
    s = str(yaml.safe_dump(info, sort_keys=False, allow_unicode=True))
    s = s.replace('null', '')
    s = s.strip()
    ss = s.split('\n')
    ss.insert(0, f'tags: [{", ".join(tags)}]')
    ss.insert(3, f"number: '{no}'")
    ss.append(f'companies: [{", ".join(coms)}]')
    s = '\n'.join(ss)
    return s


def process(fp):
    from readme.utils import ReadmeUtils
    with fp.open(encoding='utf8') as f:
        txt = f.read()
    # info_str = RE_INFO.search(txt).group(1)
    # info = json.loads(info_str)
    info_str = ReadmeUtils.get_annotation_info(txt)
    try:
        info = yaml.safe_load(info_str)
    except:  # noqa
        raise ValueError(fp)
    new_info = yaml_info(info)
    new_info_str = new_info_temp.format(info=new_info)
    new_txt = RE_INFO.sub(new_info_str, txt, count=1)
    with fp.open('w', encoding='utf8') as f:
        f.write(new_txt)


def main():
    for dp, _, fns in os.walk(fp_problems):
        for fn in fns:
            fp = Path(dp) / fn
            process(fp)


def _test():
    fp = Path(r'../../algorithms/problems/2021/10/LeetCode_0001_简单_两数之和.md')
    process(fp)


if __name__ == '__main__':
    """"""
    # _test()
    main()
