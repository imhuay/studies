#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Time: 2022-06-09 5:57 下午

Author: huayang

Subject:

"""
import os  # noqa
import doctest  # noqa

# from collections import defaultdict
# from itertools import islice
# from pathlib import Path
# from typing import *

# from tqdm import tqdm


from datasets import load_dataset


def load_data(path, name=None, **kwargs):
    """
    Examples:
        data = load_data('rotten_tomatoes')
        data = load_data('glue', 'sst2')

    Args:
        path:
        name:

    Returns:

    """
    data = load_dataset(path=path, name=name, **kwargs)
    return data


if __name__ == '__main__':
    """"""
    doctest.testmod()

    d = load_data('rotten_tomatoes')
    t = d['test']
    print(type(t))
