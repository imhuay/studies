#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Time: 2021-11-16 11:28 上午

Author: huayang

Subject:

"""
import os  # noqa
import doctest  # noqa

# from typing import *
# from itertools import islice
# from collections import defaultdict

import torch
import torch.nn as nn


class MaskPooling(nn.Module):
    """
    MaskPooling

    Examples:
        >>> class SentenceBert(nn.Module):
        ...     def __init__(self):
        ...         super().__init__()
        ...         self.bert = Bert()  # noqa
        ...         self.pooling = MaskPooling(mode='mean')
        ...
        ...     def forward(self, token_ids, masks):
        ...         token_embeddings = self.bert(token_ids)[1]  # [B, L, H]
        ...         return self.pooling(token_embeddings, masks)  # [B, H]
    """

    def __init__(self, mode='mean'):
        """"""
        super().__init__()
        self.mode = mode
        if mode == 'mean':
            self.pooling = self.mean_mask_pooling
        elif mode == 'sum':
            self.pooling = self.sum_mask_pooling
        elif mode == 'max':
            self.pooling = self.max_mask_pooling
        else:
            raise ValueError(f"`mode` should one of ('mean', 'sum', 'max'), but {mode}")

    def forward(self, token_embeddings, masks):
        """
        Args:
            token_embeddings: [B, L, H]
            masks: 0/1 tensor with [B, L]

        Returns: [B, H]
        """
        expanded_masks = masks.unsqueeze(-1).expand(token_embeddings.shape).float()  # [B, L] -> [B, L, H]
        return self.pooling(token_embeddings, expanded_masks)

    @staticmethod
    def mean_mask_pooling(token_embeddings, expanded_masks):
        """"""
        return (token_embeddings * expanded_masks).sum(1) / expanded_masks.sum(1)  # [B, L, H] -> [B, H]

    @staticmethod
    def sum_mask_pooling(token_embeddings, expanded_masks):
        """"""
        return (token_embeddings * expanded_masks).sum(1)  # [B, L, H] -> [B, H]

    @staticmethod
    def max_mask_pooling(token_embeddings, expanded_masks):
        """"""
        return torch.max(token_embeddings.masked_fill(expanded_masks == 0, -1e12), dim=1).values  # [B, H]
