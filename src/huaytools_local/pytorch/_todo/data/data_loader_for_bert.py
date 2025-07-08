#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Time: 2021-11-19 11:15 上午

Author: huayang

Subject:

"""
import os  # noqa
import doctest  # noqa

from typing import *
# from itertools import islice
# from collections import defaultdict

from dataclasses import dataclass

# from tqdm import tqdm

import torch
from torch.utils.data import DataLoader

from huaytools_local.nlp.bert.tokenization import tokenizer as _tokenizer
from huaytools_local.pytorch.utils import default_device

__all__ = [
    'BertSample',
    'MultiBertSample',
    'BertDataLoader',
]


@dataclass()
class BertSample:
    """Bert 样本类 for 单句/双句分类

    Examples:
        >>> it = BertSample('1', '2', 0.1)
        >>> print(it)
        BertSample(text='1', text_next='2', label=0.1)
    """
    text: str
    text_next: str = None
    label: Union[int, float] = None


@dataclass()
class MultiBertSample:
    """Bert 样本类 for 双塔/多塔训练

    References:
        sentence_transformers.InputExample
    """
    texts: List[str]
    label: Union[int, float] = None


class BertDataLoader(DataLoader):
    """@Pytorch Utils
    简化 Bert 训练数据的加载

    Examples:
        # 单句判断
        >>> file = ['我爱Python', '我爱机器学习', '我爱NLP']
        >>> ds = []
        >>> for t in file:
        ...     it = BertSample(t)
        ...     ds.append(it)
        >>> dl = BertDataLoader(ds, batch_size=2)
        >>> first_batch = next(iter(dl))
        >>> first_batch['token_ids'].shape
        torch.Size([2, 8])
        >>> first_batch['token_ids'][0, :]  # 我爱Python
        tensor([ 101, 2769, 4263, 9030,  102,    0,    0,    0])
        >>> first_batch['token_ids'][1, :]  # 我爱机器学习
        tensor([ 101, 2769, 4263, 3322, 1690, 2110,  739,  102])

        # 句间关系
        >>> file = [('我爱Python', '测试1'), ('我爱机器学习', '测试2'), ('我爱NLP', '测试3')]
        >>> ds = [BertSample(t[0], t[1], label=1) for t in file]
        >>> dl = BertDataLoader(ds, batch_size=2)
        >>> for b in dl:
        ...     features, labels = b
        ...     print('max_len:', features['token_ids'].shape[1])
        ...     print('token_ids:', features['token_ids'][0, :10])
        ...     print('labels:', labels)
        ...     print()
        max_len: 12
        token_ids: tensor([ 101, 2769, 4263, 9030,  102, 3844, 6407,  122,  102,    0])
        labels: tensor([1., 1.])
        <BLANKLINE>
        max_len: 10
        token_ids: tensor([  101,  2769,  4263,   156, 10986,   102,  3844,  6407,   124,   102])
        labels: tensor([1.])
        <BLANKLINE>

        # 双塔
        >>> file = [('我爱Python', '测试1'), ('我爱机器学习', '测试2'), ('我爱NLP', '测试3')]
        >>> ds = [MultiBertSample(list(t)) for t in file]
        >>> dl = BertDataLoader(ds, batch_size=2)
        >>> first_batch = next(iter(dl))
        >>> len(first_batch)
        2
        >>> [it['token_ids'].shape for it in first_batch]  # noqa
        [torch.Size([2, 8]), torch.Size([2, 5])]

        # 多塔
        >>> file = [('我爱Python', '测试1', '1'), ('我爱机器学习', '测试2', '2'), ('我爱NLP', '测试3', '3')]
        >>> ds = [MultiBertSample(list(t)) for t in file]
        >>> dl = BertDataLoader(ds, batch_size=2)
        >>> first_batch = next(iter(dl))
        >>> len(first_batch)
        3
        >>> [it['token_ids'].shape for it in first_batch]  # noqa
        [torch.Size([2, 8]), torch.Size([2, 5]), torch.Size([2, 3])]

        # 异常测试
        >>> ds = ['我爱自然语言处理', '我爱机器学习', '测试']
        >>> dl = BertDataLoader(ds, batch_size=2)  # noqa
        Traceback (most recent call last):
            ...
        TypeError: Unsupported sample type=<class 'str'>

    References:
        sentence_transformers.SentenceTransformer.smart_batching_collate
    """

    def __init__(self, dataset: List[Union[BertSample, MultiBertSample]],
                 *, batch_size, max_len=None,
                 tokenizer=None, device=None, **kwargs):
        """"""
        self.max_len = max_len

        if device is None:
            device = default_device()
        self.device = device

        if tokenizer is None:
            tokenizer = _tokenizer
        self.tokenizer = tokenizer

        if isinstance(dataset[0], BertSample):
            collate_fn = self.collate_fn_for_bert
        elif isinstance(dataset[0], MultiBertSample):
            collate_fn = self.collate_fn_for_bert_bi_encoder
        else:
            raise TypeError(f'Unsupported sample type={type(dataset[0])}')

        super().__init__(dataset,  # noqa
                         batch_size=batch_size, collate_fn=collate_fn, **kwargs)

    def collate_fn_for_bert(self, batch: List[BertSample]):
        """"""
        has_label = batch[0].label is not None

        texts = [(it.text, it.text_next) for it in batch]
        token_ids, token_type_ids, token_masks = _tokenizer.batch_encode(texts, max_len=self.max_len,
                                                                         return_token_type_ids=True,
                                                                         return_token_masks=True)
        features = {
            'token_ids': torch.as_tensor(token_ids).to(self.device),
            'token_type_ids': torch.as_tensor(token_type_ids).to(self.device),
            'token_masks': torch.as_tensor(token_masks).to(self.device),
        }

        if has_label:
            labels = [it.label for it in batch]
            labels = torch.as_tensor(labels).float().to(self.device)
            return features, labels

        return features

    def collate_fn_for_bert_bi_encoder(self, batch: List[MultiBertSample]):
        """"""
        num_text = len(batch[0].texts)
        has_label = batch[0].label is not None

        features = []
        for i in range(num_text):
            """"""
            texts = [sample.texts[i] for sample in batch]
            token_ids, token_type_ids, token_masks = _tokenizer.batch_encode(texts, max_len=self.max_len,
                                                                             return_token_type_ids=True,
                                                                             return_token_masks=True)
            features_one = {
                'token_ids': torch.as_tensor(token_ids).to(self.device),
                'token_type_ids': torch.as_tensor(token_type_ids).to(self.device),
                'token_masks': torch.as_tensor(token_masks).to(self.device),
            }
            features.append(features_one)

        if has_label:
            labels = [it.label for it in batch]
            labels = torch.as_tensor(labels).float().to(self.device)
            return features, labels

        return features


def _test():
    """"""
    doctest.testmod()


if __name__ == '__main__':
    """"""
    _test()
