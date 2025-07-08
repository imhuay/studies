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

TRANSFORMERS_OFFLINE = 'TRANSFORMERS_OFFLINE'
HF_DATASETS_OFFLINE = 'HF_DATASETS_OFFLINE'


class HFUtils:

    @staticmethod
    def set_offline():
        """"""
        os.environ[TRANSFORMERS_OFFLINE] = '1'  # 模型
        os.environ[HF_DATASETS_OFFLINE] = '1'  # 数据

    @staticmethod
    def download_model(model_name: str, save_dir: str,
                       complete_path=True,
                       model_type=AutoModel,
                       config_type=AutoConfig,
                       tokenizer_type=AutoTokenizer):
        """"""
        if complete_path and not save_dir.endswith(model_name):
            save_dir = os.path.join(save_dir, model_name)

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
