#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Time: 2022-06-07 3:21 下午

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


from huaytools_local.huggingface import set_offline, download_model

from transformers import AutoModelForSequenceClassification, AutoConfig, AutoTokenizer


# def ex_download_model(model_name, save_path, ):
#     model_name = 'facebook/muppet-roberta-base'
#     save_path = r'/Users/huayang/workspace/models/transformers/muppet-roberta-base'
#     download_model(model_name, save_path, model_type=AutoModelForSequenceClassification)


def ex_offline(model_name, save_path):
    """"""
    download_model(model_name, save_path, model_type=AutoModelForSequenceClassification)

    set_offline()

    model = AutoModelForSequenceClassification.from_pretrained(save_path)
    config = AutoConfig.from_pretrained(save_path)
    tokenizer = AutoTokenizer.from_pretrained(save_path)

    s = "We are very happy to show you the 🤗 Transformers library."
    inputs = tokenizer(s, return_tensors='pt')
    o = model(**inputs)
    print(o.logits)


if __name__ == '__main__':
    """"""
    doctest.testmod()
    from pathlib import Path

    model_name = r'roberta-large'
    save_path = rf'/Users/huayang/workspace/models/transformers/{Path(model_name).name}'
    ex_offline(model_name, save_path)
