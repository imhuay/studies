#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Time: 2022-06-07 3:22 下午

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

from transformers import AutoConfig, AutoTokenizer, AutoModel


def set_offline():
    """"""
    os.environ['TRANSFORMERS_OFFLINE'] = '1'  # 模型
    os.environ['HF_DATASETS_OFFLINE'] = '1'  # 数据


def download_model(model_name, save_dir,
                   model_type=AutoModel,
                   config_type=AutoConfig,
                   tokenizer_type=AutoTokenizer):
    """"""
    model = model_type.from_pretrained(model_name)
    config = config_type.from_pretrained(model_name)
    tokenizer = tokenizer_type.from_pretrained(model_name)

    model.save_pretrained(save_dir)
    config.save_pretrained(save_dir)
    tokenizer.save_pretrained(save_dir)
    return save_dir


if __name__ == '__main__':
    """"""
    doctest.testmod()
