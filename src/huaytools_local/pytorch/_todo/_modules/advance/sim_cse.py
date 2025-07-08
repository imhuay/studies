#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Time:
   2021-07-30 4:54 下午
   
Author:
   huayang
   
Subject:

References:
    - https://github.com/princeton-nlp/SimCSE
    - https://github.com/bojone/SimCSE
   
"""

import torch
import torch.nn as nn

from huaytools_local.pytorch._todo._modules import EncoderWrapper
from huaytools_local.pytorch.utils import cosine_similarity_dense

__all__ = [
    'SimCSE'
]


# TODO: 有监督
class SimCSE(EncoderWrapper):
    """@Pytorch Models
    SimCSE

    References: https://github.com/princeton-nlp/SimCSE
    """

    def __init__(self, encoder, distance_fn=cosine_similarity_dense, encode_wrapper=None):
        """"""
        super(SimCSE, self).__init__(encoder, encode_wrapper)

        self.distance_fn = distance_fn
        self.loss_fn = nn.CrossEntropyLoss()

    def forward(self, inputs):
        """"""
        # 编码一个 batch 的句向量
        o1 = self.encode(inputs)  # [B, N]

        # 无监督
        if self.training:
            B, N = o1.shape

            # 再 encode 一次，因为是 training 状态，dropout 生效，会导致两次结果不同
            o2 = self.encode(inputs)  # [B, N]
            # 计算两次结果的 cosine 相似度
            logits = self.distance_fn(o1, o2)  # [B, B]
            # 除了自己全是负例，即每个句子都是不同的标签
            labels = torch.arange(B, dtype=torch.long)  # [B]
            # 计算交叉熵损失
            loss = self.loss_fn(logits, labels)

            return o1, o2, loss

        return o1


def _test():
    """"""

    def _test_SimCSE():  # noqa
        """"""
        from huaytools_local.nlp.bert.tokenization import tokenizer
        from huaytools_local.pytorch._todo._modules import Bert

        bert = Bert()

        def encode_wrapper(encoder, _inputs):
            """"""
            cls, hidden_states, all_hidden_states = encoder(*_inputs)
            return hidden_states[:, 0]  # cls before pooler

        sc = SimCSE(bert, encode_wrapper=encode_wrapper)

        print(len(sc.state_dict()))
        # for k, v in sc.state_dict().items():
        #     print(k, v.shape)

        s1 = '我爱机器学习'
        s2 = '我爱计算机'
        tid1, sid1, mask1 = tokenizer.encode(s1, max_len=10)
        tid2, sid2, mask2 = tokenizer.encode(s2, max_len=10)
        tids = torch.tensor([tid1, tid2])
        print(tids)
        sids = torch.tensor([sid1, sid2])
        print(sids)

        # sc.eval()
        inputs = [tids, sids]
        o1, o2, loss = sc(inputs)
        print(o1[0, :5])
        print(o2[0, :5])
        print(loss)

    _test_SimCSE()


if __name__ == '__main__':
    """"""
    _test()
