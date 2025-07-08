#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Time:
    2022-07-28 14:25
Author:
    HuaYang(imhuay@163.com)
Subject:
    Demo for AutoPhrase
"""
import os
import sys
import json
import doctest

from typing import *
from pathlib import Path
from itertools import islice
from collections import defaultdict
import opencc

# requirements.txt
from autophrasex import *


def demo():
    """"""
    n_gram = 4
    epochs = 10
    top_k = 100000

    ap = AutoPhrase(
        reader=DefaultCorpusReader(tokenizer=JiebaTokenizer()),
        selector=DefaultPhraseSelector(),
        extractors=[
            NgramsExtractor(N=n_gram),
            IDFExtractor(),
            EntropyExtractor()
        ]
    )

    predictions = ap.mine(
        corpus_files=[r'/Users/huay/Workspace/data/dishes/all_dishes_20220727.txt'],
        quality_phrase_files='/Users/huay/Workspace/shopee_workspace/projects/01-菜品体系建设/crawler_wikipedia/data/quality_words.txt',
        N=n_gram,
        topk=top_k,
        epochs=epochs,
        callbacks=[
            LoggingCallback(),
            ConstantThresholdScheduler(),
            EarlyStopping(patience=2, min_delta=1)
        ],
    )

    # 输出挖掘结果
    save_path = rf'/Users/huay/Workspace/data/dishes/candidates_N{n_gram}_Epoch{epochs}_Top{top_k}.csv'
    import csv
    with open(save_path, 'w', newline='', encoding='utf8') as fw:
        w = csv.writer(fw, quoting=csv.QUOTE_ALL)
        w.writerow(['candidate', 'score'])
        w.writerows(predictions)


class __DoctestWrapper:
    """"""

    def __init__(self):
        """"""
        doctest.testmod()

        for k, v in self.__class__.__dict__.items():
            if k.startswith('demo') and isinstance(v, Callable):
                v(self)

    def demo_base(self):  # noqa
        """"""
        demo()


if __name__ == '__main__':
    """"""
    __DoctestWrapper()
