#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Time: 2021-10-23 9:29 下午

Author: huayang

Subject:

"""
import os
import sys
import json
import doctest

from typing import *
from collections import defaultdict
from typing import Callable

from torch import Tensor, nn as nn


def default_encode_wrapper(encoder, inputs):
    """"""
    if isinstance(inputs, Tensor):
        return encoder(inputs)
    elif isinstance(inputs, list):
        return encoder(*inputs)
    else:
        return encoder(**inputs)


class EncoderWrapper(nn.Module):
    """ Encoder 包装模块
        用于一些网络结构，网络本身可以使用不同的 Encoder 来生成输入下游的 embedding，比如孪生网络；

    Examples:

        示例1：单独使用，相当于对给定模型的输出通过`encode_wrapper`做一次包装；
            在本例中，即对 bert 的第二个输出计算的第二维均值（句向量），输出等价于直接使用 `encode_wrapper(encoder, inputs)`；
            使用包装的好处是可以调用`nn.Module`的相关方法，比如模型保存等。
        ```python
        from my.pytorch.modules.transformer.bert import get_bert_pretrained

        bert, tokenizer = get_bert_pretrained(return_tokenizer=True)
        encode_wrapper = lambda _e, _i: _e(*_i)[1].mean(1)
        test_encoder = EncoderWrapper(bert, encode_wrapper)

        ss = ['测试1', '测试2']
        inputs = tokenizer.batch_encode(ss, max_len=10)
        o = test_encoder(inputs)
        print(o.shape)  # [2, 768]
        ```

        示例2：继承使用，常用于一些框架中，框架内的 Encoder 可以任意替换
            本例为一个常见的孪生网络结构，通过继承 `EncoderWrapper` 可以灵活替换所需的模型；
        ```python
        from my.pytorch.modules.loss import ContrastiveLoss
        from my.pytorch.backend.distance_fn import euclidean_distance
        
        class SiameseNet(EncoderWrapper):
            """"""
            def __init__(self, encoder, encoder_helper):
                """"""
                super(SiameseNet, self).__init__(encoder, encoder_helper)

                self.loss_fn = ContrastiveLoss(euclidean_distance)  # 基于欧几里得距离的对比损失
                
            def forward(self, x1, x2, labels):
                """"""
                o1 = self.encode(x1)
                o2 = self.encode(x2)
                return self.loss_fn(o1, o2, labels)
        ```
    """

    def __init__(self, encoder, encode_wrapper: Callable = None):
        """

        Args:
            encoder: 编码器
            encode_wrapper: 辅助函数接口，用于帮助调整 encoder 的输入或输出，
                比如使用 bert 作为 encoder，bert 模型的输出很多，不同任务使用的输出也不同，这是可以通过 encode_wrapper 来调整；
                函数接口如下 `def encode_wrapper(encoder, inputs)`，
                默认为 encoder 直接调用 inputs: `encode_wrapper = lambda _encoder, _inputs: _encoder(_inputs)`
        """
        super(EncoderWrapper, self).__init__()

        self.encoder = encoder
        if encode_wrapper is not None:
            self.encode_wrapper = encode_wrapper

    def forward(self, *args, **kwargs):
        return self.encode(*args, **kwargs)

    def encode_wrapper(self, encoder, inputs) -> Tensor:  # noqa
        return default_encode_wrapper(encoder, inputs)

    def encode(self, inputs):
        return self.encode_wrapper(self.encoder, inputs)
