#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Time: 2021-11-04 11:22 上午

Author: huayang

Subject:

"""
import re
import os
import sys
import json
import doctest

from typing import *
from collections import defaultdict

import torch
import torch.nn as nn

__all__ = [
    'FGM'
]


class FGM:
    """@Pytorch Train Plugin
    Fast Gradient Method (对抗训练)

    Examples:
        >>> def training_step(model, batch, optimizer, fgm=FGM(param_pattern='word_embedding')):
        ...     inputs, labels = batch
        ...
        ...     # 正常训练
        ...     loss = model(inputs, labels)
        ...     loss.backward()  # 反向传播，得到正常的梯度
        ...
        ...     # 对抗训练（需要添加的代码）
        ...     fgm.collect(model)
        ...     fgm.attack()
        ...     loss_adv = model(inputs, labels)  # 对抗梯度
        ...     loss_adv.backward()  # 累计对抗梯度
        ...     fgm.restore(model)  # 恢复被添加扰动的参数
        ...
        ...     # 更新参数
        ...     optimizer.step()
        ...     optimizer.zero_grad()

    References:
        - [Adversarial Training Methods for Semi-Supervised Text Classification](https://arxiv.org/abs/1605.07725)
        - [NLP中的对抗训练 + PyTorch实现](https://zhuanlan.zhihu.com/p/91269728)
    """

    def __init__(self, param_pattern: Union[str, re.Pattern], epsilon: float = 1.0):
        """
        Args:
            param_pattern: 需要添加对抗扰动的参数名/pattern，如果是 NLP 模型，一般为 embedding 层的参数
            epsilon: 扰动系数
        """
        self.param_backup = dict()
        if isinstance(param_pattern, str):
            param_pattern = re.compile(param_pattern)
        self.param_pattern = param_pattern
        self.epsilon = epsilon

    def collect(self, model: nn.Module):
        """收集需要添加扰动的参数"""
        for name, param in model.named_parameters():
            if self.param_pattern.search(name) and param.requires_grad:
                self.param_backup[name] = param.data.clone()

    def attack(self):
        """攻击对抗"""
        for name, param in self.param_backup.items():
            # 计算并添加扰动
            g = param.grad
            g_norm = torch.norm(param.grad)
            if g_norm != 0 and not torch.isnan(g_norm):
                r_adv = self.epsilon * g / g_norm  # 扰动
                param.data.add_(r_adv)

    def restore(self, model: nn.Module):
        """恢复参数"""
        for name, param in model.named_parameters():
            if name in self.param_backup:
                param.data = self.param_backup[name]

        # 清空备份
        self.param_backup.clear()


def _test():
    """"""
    doctest.testmod()


if __name__ == '__main__':
    """"""
    _test()
