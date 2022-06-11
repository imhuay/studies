#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Time: 2021-11-04 2:20 下午

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
    'PGM'
]


class PGM:
    """@Pytorch Train Plugin
    Projected Gradient Method (对抗训练)

    Examples:
        >>> def training_step(model, batch, optimizer, steps=3, pgm=PGM(param_pattern='word_embedding')):
        ...     inputs, labels = batch
        ...
        ...     # 正常训练
        ...     loss = model(inputs, labels)
        ...     loss.backward()  # 反向传播，得到正常的梯度
        ...
        ...     # 对抗训练（需要添加的代码）
        ...     pgm.collect(model)
        ...     for t in range(steps):
        ...         pgm.attack()  # 小步添加扰动
        ...
        ...         if t < steps - 1:
        ...             optimizer.zero_grad()  # 在最后一步前，还没有得到最终对抗训练的梯度，所以要先清零
        ...         else:
        ...             pgm.restore_grad(model)  # 最后一步时恢复正常的梯度，与累积的扰动梯度合并
        ...
        ...         loss_adv = model(inputs, labels)
        ...         loss_adv.backward()  # 累加对抗梯度（在最后一步之前，实际只有对抗梯度）
        ...     pgm.restore(model)  # 恢复被添加扰动的参数
        ...
        ...     # 更新参数
        ...     optimizer.step()
        ...     optimizer.zero_grad()

    References:
        - [Towards Deep Learning Models Resistant to Adversarial Attacks](https://arxiv.org/abs/1706.06083)
        - [NLP中的对抗训练 + PyTorch实现](https://zhuanlan.zhihu.com/p/91269728)
    """

    def __init__(self, param_pattern: Union[str, re.Pattern],
                 alpha: float = 0.3,
                 epsilon: float = 1.0):
        """
        Args:
            param_pattern: 需要添加对抗扰动的参数名/pattern，如果是 NLP 模型，一般为 embedding 层的参数
            epsilon: 扰动系数
            alpha:
        """
        self.param_backup = dict()
        self.grad_backup = dict()
        if isinstance(param_pattern, str):
            param_pattern = re.compile(param_pattern)
        self.param_pattern = param_pattern
        self.epsilon = torch.as_tensor(epsilon)
        self.alpha = torch.as_tensor(alpha)

    def collect(self, model: nn.Module):
        """收集需要添加扰动的参数"""
        for name, param in model.named_parameters():
            # 备份需要添加扰动的参数
            if self.param_pattern.search(name) and param.requires_grad:
                self.param_backup[name] = param.data.clone()
            # 备份所有梯度
            if param.requires_grad:
                self.grad_backup[name] = param.grad.clone()

    def attack(self):
        """添加对抗"""
        for name, param in self.param_backup.items():
            # 计算并添加扰动
            g = param.grad
            g_norm = torch.norm(param.grad)
            if g_norm != 0 and not torch.isnan(g_norm):
                r_t = self.alpha * g / g_norm  # 小步扰动
                r_adv = (param.data + r_t) - self.param_backup[name]  # 累计扰动
                r_norm = torch.norm(r_adv)
                if r_norm > self.epsilon:  # 如果超过扰动空间
                    r_adv = self.epsilon * r_adv / r_norm

                param.data = self.param_backup[name] + r_adv  # 添加扰动

    def restore_grad(self, model):
        for name, param in model.named_parameters():
            if param.requires_grad:
                param.grad = self.grad_backup[name]

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
