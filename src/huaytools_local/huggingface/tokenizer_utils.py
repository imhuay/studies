#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Time:
    2022-07-21 11:53
Author:
    huayang (imhuay@163.com)
Subject:
    tokenizer_wrap
"""
import os
import sys
import json
import time
import doctest

from typing import *
from pathlib import Path
from itertools import islice
from collections import defaultdict

from huaytools_local.utils import get_logger

from transformers import PreTrainedTokenizerBase, AutoTokenizer
from transformers.utils import TensorType
from transformers.utils.generic import PaddingStrategy
from transformers.tokenization_utils_base import TruncationStrategy

_logger = get_logger()


class TokenizerWrap:
    """
    对 Tokenizer 的简单包装，以符合自己的使用习惯
    """

    def __init__(self, tokenizer: Union[str, PreTrainedTokenizerBase]):
        """"""
        if isinstance(tokenizer, str):
            tokenizer = AutoTokenizer.from_pretrained(tokenizer)
        self.tokenizer = tokenizer

    # def __call__(self, *args, **kwargs):
    #     return self.encode(*args, **kwargs)

    def encode(self, inputs: Union[str, List[str]],
               padding: str = PaddingStrategy.LONGEST,
               truncation: str = TruncationStrategy.LONGEST_FIRST,
               max_length: int = None,
               add_special_tokens: bool = None,
               return_tensors: str = None,
               return_token_type_ids: bool = None,
               return_attention_mask: bool = None,
               return_tokens: bool = None):
        """
        Convert text to ids.

        Args:
            inputs:
            padding: 填充策略，默认为 'longest'
            truncation: 截断策略，默认为 'longest_first'
            max_length: 当 padding='max_length' 时生效，默认使用模型配置的最大值，一般为 512
            add_special_tokens: 默认 True，当输入为一个单词时为 False
            return_tensors: 默认返回 Pytorch 格式的张量，但只有一句时不转换
            return_token_type_ids: 默认 False
            return_attention_mask: 默认 True，但只有一句时为 False
            return_tokens: 默认 False，但只有一句时为 True

        Returns:

        """
        is_single = isinstance(inputs, str)  # 单句的情况
        is_word = is_single and len(inputs.split()) == 1
        add_special_tokens = add_special_tokens or not is_word
        return_tensors = TensorType.PYTORCH if not is_single else return_tensors
        return_token_type_ids = return_token_type_ids or False
        return_attention_mask = return_attention_mask or not is_single
        return_tokens = return_tokens or is_single

        ret = self.tokenizer(inputs,
                             padding=padding,
                             truncation=truncation,
                             max_length=max_length,
                             add_special_tokens=add_special_tokens,
                             return_tensors=return_tensors,
                             return_token_type_ids=return_token_type_ids,
                             return_attention_mask=return_attention_mask)

        if return_tokens:
            if is_single:
                ret['tokens'] = ret.tokens(0)
            else:
                ret['tokens'] = [ret.tokens(i) for i in range(len(inputs))]

        return ret

    def decode(self, inputs,
               skip_special_tokens=True,
               clean_up_tokenization_spaces=False):
        """"""
        return self.tokenizer.decode(inputs,
                                     skip_special_tokens=skip_special_tokens,
                                     clean_up_tokenization_spaces=clean_up_tokenization_spaces)

    def tokenize(self, inputs: Union[str, List[str]], add_special_tokens=False, **kwargs):
        """"""
        ret = list()
        if isinstance(inputs, str):
            inputs = [inputs]
        outs = self.tokenizer(inputs, add_special_tokens=add_special_tokens, **kwargs)
        for i, line in enumerate(inputs):
            ret.append((line, outs.tokens(i)))
        return ret

    @property
    def special_tokens(self) -> Dict[str, int]:
        d = {}
        for v in self.tokenizer.special_tokens_map.values():
            d[v] = self.vocab[v]
        return d

    @property
    def vocab(self):
        return self.tokenizer.get_vocab()

    @property
    def mask_token_id(self):
        return self.tokenizer.mask_token_id

    def id2token(self, token_id: int):
        assert isinstance(token_id, int), 'Use `decode()` method to decode more than one token_id.'
        return self.decode(token_id)

    def token2id(self, token: str):
        """
        注意：一些模型会对 token 做一些预处理。
            比如 xlm_roberta，会对很多 token 加上 '▁' 前缀
        """
        tokens = self.encode(token, add_special_tokens=False).tokens()
        if not tokens or len(tokens) > 1:
            _logger.info(f'No "{token}" in vocab.')
            return -1
        return self.vocab[tokens[0]]


class __Test:
    """"""

    def __init__(self):
        """"""
        for k, v in self.__class__.__dict__.items():
            if k.startswith('_test') and isinstance(v, Callable):
                print(f'\x1b[32m=== Start "{k}" {{\x1b[0m')
                start = time.time()
                v(self)
                print(f'\x1b[32m}} End "{k}" - Spend {time.time() - start:3f}s===\x1b[0m\n')

    def _test_doctest(self):  # noqa
        """"""
        import doctest
        doctest.testmod()

    def _test_base(self):  # noqa
        """"""
        from transformers.models.xlm_roberta.tokenization_xlm_roberta_fast import XLMRobertaTokenizerFast
        tokenizer: XLMRobertaTokenizerFast = XLMRobertaTokenizerFast.from_pretrained('xlm-roberta-large')
        s = 'nasi adalah food yang sangat populer.'
        print(tokenizer.tokenize(s))


if __name__ == '__main__':
    """"""
    __Test()
