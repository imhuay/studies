#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Time:
    2022-08-18 20:27
Author:
    huayang (imhuay@163.com)
Subject:
    _common
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

import random
import numpy as np
import torch
import torch.nn as nn

from torch import Tensor

from huaytools_local.utils import get_logger

logger = get_logger()


class TorchUtils:
    """"""

    @staticmethod
    def set_seed(seed: int = None):
        """
        Args:
            seed:

        Notes:
            如果在 DataLoader 设置了 num_workers>0，还需要设置 worker_init_fn，以确保数据加载的顺序；
            ```
            # 示例
            def _worker_init_fn(worker_id):
                np.random.seed(int(seed) + worker_id)
            ```

        References:
            [PyTorch固定随机数种子](https://blog.csdn.net/john_bh/article/details/107731443)
        """
        if seed is None:
            return

        os.environ['PYTHONHASHSEED'] = str(
            seed)  # ref: https://docs.python.org/3/using/cmdline.html#envvar-PYTHONHASHSEED
        random.seed(seed)
        np.random.seed(seed)

        torch.manual_seed(seed)
        torch.cuda.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)  # if using multi-GPU.

    @staticmethod
    def get_torch_version():
        """"""
        return torch.__version__

    @staticmethod
    def recur_to(obj: Union[Tensor, Sequence[Tensor], Mapping[Any, Tensor]],
                 sth: Union[str, torch.dtype, torch.device, Tensor]):
        """
        Examples:
            >>> t = torch.as_tensor([1,2,3])
            >>> t = TorchUtils.recur_to(t, torch.float16)
            >>> t.dtype
            torch.float16
            >>> ts = [torch.as_tensor([1,2,3]), torch.as_tensor([4,5,6])]
            >>> ts = TorchUtils.recur_to(ts, t)
            >>> ts[0].dtype
            torch.float16
            >>> ts = {'a': torch.as_tensor([1]), 'b': [torch.as_tensor([2]), {'c': torch.as_tensor([3])}]}
            >>> ts = TorchUtils.recur_to(ts, torch.device('cpu'))
            >>> ts['b'][0].device
            device(type='cpu')
        """
        return _recur_to(obj, sth)

    @staticmethod
    def load_state_dict_from_tensorflow(weights_path):
        """"""
        import tensorflow as tf

        def _loader(name):
            """"""
            return tf.train.load_variable(weights_path, name)

        if os.path.isdir(weights_path):  # 如果是目录
            # 找出目录下的 xxx.ckpt.index 文件
            file_ls = os.listdir(weights_path)
            file_name = [f for f in file_ls if f.endswith('.index')][0]
            weights_path = os.path.join(weights_path, file_name)

        weights_path = weights_path[:-6] if weights_path.endswith('.index') else weights_path
        weights_pretrained = OrderedDict()
        for n, _ in tf.train.list_variables(weights_path):
            array = _loader(n)
            if n.endswith('kernel'):
                array = np.transpose(array)  # transpose(tf[in, out]) -> pt[out, in]
            weights_pretrained[n] = torch.as_tensor(array)

        return weights_pretrained

    @staticmethod
    def load_state_dict(weights_path, map_location='cpu', **kwargs):
        """"""
        return torch.load(weights_path, map_location=map_location, **kwargs)

    @staticmethod
    def load_state_dict_explicit(model: nn.Module, state_dict, name_mapping=None):
        """
        与 m.load_state_dict 功能类似，对未加载的权重给出更明确的提示

        Args:
            model:
            state_dict: {name: tensor} 字典
            name_mapping: {name: name_old} 字典，默认为 None；
                当 weights_dict 与模型中的权重名称不匹配时，可以通过 name_mapping 再映射一次

        Examples:
            >>> m = nn.Linear(3, 4)  # {'weight': ..., 'bias': ...}
            >>> wd = {'w': torch.randn(4, 3), 'b': torch.randn(4)}
            >>> nm = {'weight': 'w', 'bias': 'b'}
            >>> _ = TorchUtils.load_state_dict_explicit(m, wd, nm)
        """

        if name_mapping:
            for name, name_old in name_mapping.items():
                if name_old in state_dict:
                    state_dict[name] = state_dict.pop(name_old)  # 替换新名称

        load_keys = set()  # 记录顺利加载的 key
        state_dict_tmp = OrderedDict()  # 新 state_dict，不直接修改原 state_dict
        state_dict_old = model.state_dict()
        for name, tensor in state_dict_old.items():
            if name not in state_dict:
                state_dict_tmp[name] = tensor
            else:
                assert state_dict[name].shape == tensor.shape

                state_dict_tmp[name] = state_dict[name]
                load_keys.add(name)

        missed_keys = sorted(set(state_dict_old.keys()) - load_keys)  # 未更新的权重
        unused_keys = sorted(set(state_dict.keys()) - load_keys)  # 未使用的权重
        logger.info(f'Missed weights({len(missed_keys)}): {missed_keys}')
        logger.info(f'Unused weights({len(unused_keys)}): {unused_keys}')

        model.load_state_dict(state_dict_tmp)  # reload
        model.eval()  # deactivate dropout
        return model


def _recur_to(obj, sth):
    """"""
    if hasattr(obj, 'to'):
        return obj.to(sth)
    elif isinstance(obj, Sequence):
        return type(obj)([_recur_to(o, sth) for o in obj])  # noqa
    elif isinstance(obj, Mapping):
        return type(obj)([(k, _recur_to(v, sth)) for k, v in obj.items()])  # noqa
    else:
        raise TypeError(f"Can not apply {obj} to {sth}.")


def sequence_masking(x: torch.Tensor,
                     mask: torch.Tensor,
                     axis=1, mode='add', inf=1e12):
    """序列 mask

    Args:
        x: 2D 或 2D 以上张量，必须包含 batch_size 和 seq_len 两个维度
        mask: 形如  (batch_size, seq_len) 的 0/1 矩阵
        axis: 需要 mask 的维度，即 seq_len 所在维度，默认为 1
        mode: 有 'mul' 和 'add' 两种：
            mul 会将 pad 部分置零，一般用于全连接层之前；
            add 会把 pad 部分减去一个大的常数，一般用于 softmax 之前。
        inf: 大的常数

    Returns:
        tensor with shape same as x

    Examples:
        mask = [B, L]
        示例 1：x.shape = [B, L, _],     则 axis=1 (默认)
        示例 2：x.shape = [B, _, L, _],  则 axis=2
        示例 3：x.shape = [B, _, _, L],  则 axis=-1
    """
    if mask is None:
        return x

    assert mask.ndim == 2, 'only for mask.ndim == 2'

    if axis < 0:
        axis = x.ndim + axis

    # 将 mask 的维度扩充到与 x 一致，以便进行广播
    # 示例：假设 x.shape = [B, _, L, _]
    # 则经过以下操作后，mask.shape = [B, 1, L, 1]，相当于 mask = mask[:, None, :, None]
    for _ in range(axis - 1):
        mask = mask.unsqueeze(1)
    for _ in range(x.ndim - axis - 1):
        mask = mask.unsqueeze(-1)

    if mode == 'mul':
        return x * mask
    elif mode == 'add':
        return x - (1 - mask) * inf
    else:
        raise ValueError('`mode` must be one of %s' % {'add', 'mul'})


def create_mask_3d(q_tensor: Tensor, v_mask: Tensor, dtype=torch.float):
    """ Create 3D attention mask from a 2D tensor mask.

    Args:
      q_tensor: 2D or 3D Tensor of shape [B, Q, ...].
      v_mask: int32 Tensor of shape [B, V].
      dtype:

    Returns:
        float Tensor of shape [B, Q, V].

    References:
        [google-research/bert](https://github.com/google-research/bert)
    """
    B = q_tensor.shape[0]  # noqa
    Q = q_tensor.shape[1]  # noqa

    v_mask = v_mask.unsqueeze(1)  # [B, V] -> [B, 1, V]
    mask = torch.ones([B, Q, 1]) * v_mask  # [B, Q, V]
    return mask.to(dtype)


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

    def _test_xxx(self):  # noqa
        """"""
        pass


if __name__ == '__main__':
    """"""
    __Test()
