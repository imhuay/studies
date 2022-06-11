#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Time: 2022-06-03 10:33 下午

Author: huayang

Subject:

"""
import os  # noqa
import doctest  # noqa
import random

# from collections import defaultdict
# from itertools import islice
# from pathlib import Path
from typing import *

# from tqdm import tqdm


import numpy as np
import torch
import torch.nn as nn

from torch import Tensor

from huaytools.utils import get_logger

from huaytools.pytorch.utils.data_helper import (
    AnyDataset,
    AnyDataLoader
)


def get_torch_version():
    """"""
    return torch.__version__


def set_seed(seed: int = None, apply_cudnn=True):
    """@Pytorch Utils
    设置全局随机数种子，使实验可复现

    Args:
        seed:
        apply_cudnn: cudnn 对卷积操作进行了优化，牺牲了精度来换取计算效率；如果对精度要求不高，可以设置为 False

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

    random.seed(seed)
    os.environ['PYTHONHASHSEED'] = str(seed)  # noqa, 为了禁止hash随机化，使得实验可复现

    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)  # if using multi-GPU.

    if apply_cudnn:
        torch.backends.cudnn.benchmark = False  # noqa
        torch.backends.cudnn.deterministic = True  # noqa


def apply_to(obj, sth):
    """

    Examples:
        >>> t = torch.as_tensor([1,2,3])
        >>> t.dtype
        torch.int64
        >>> t = apply_to(t, float)
        >>> t.dtype
        torch.float64
        >>> ts = [torch.as_tensor([1,2,3]), torch.as_tensor([4,5,6])]
        >>> ts = apply_to(ts, float)
        >>> [t.dtype for t in ts]
        [torch.float64, torch.float64]
        >>> ts = {'a': torch.as_tensor([1]), 'b': [torch.as_tensor([2]), {'c': torch.as_tensor([3])}]}
        >>> ts = apply_to(ts, float)
        >>> [ts['a'].dtype, ts['b'][0].dtype, ts['b'][1]['c'].dtype]
        [torch.float64, torch.float64, torch.float64]

    """
    if hasattr(obj, "to"):
        return obj.to(sth)
    elif isinstance(obj, (List, Tuple)):
        return type(obj)(apply_to(o, sth) for o in obj)
    elif isinstance(obj, Mapping):
        new_obj = [(k, apply_to(v, sth)) for k, v in obj.items()]
        return type(obj)(new_obj)  # noqa
    else:
        raise TypeError(
            f"Can't apply {apply_to.__name__} on object of type {type(obj)}, "
            f"only of nested list/tuple/dicts of objects "
        )


def init_weights(module: nn.Module, normal_std=0.02):
    """@Pytorch Utils
    默认参数初始化

    Examples:
        >>> model = nn.Transformer()
        >>> _ = model.apply(init_weights)

    Args:
        module:
        normal_std:

    References: Bert
    """
    if isinstance(module, nn.Linear):
        # truncated_normal
        nn.init.trunc_normal_(module.weight.data, std=normal_std)
        if module.bias is not None:
            module.bias.data.zero_()
    elif isinstance(module, nn.Embedding):
        # truncated_normal
        nn.init.trunc_normal_(module.weight.data, std=normal_std)
        if module.padding_idx is not None:
            module.weight.data[module.padding_idx].zero_()
    elif isinstance(module, nn.LayerNorm):
        module.weight.data.fill_(1.0)
        module.bias.data.zero_()
    else:
        pass  # default


def load_state_dict_tf(weights_path):
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


def load_state_dict_pt(weights_path, map_location='cpu'):
    """"""
    state_dict = torch.load(weights_path, map_location=map_location)
    return state_dict


def load_state_dict_explicit(model: nn.Module, state_dict, name_mapping=None):
    """ 与 m.load_state_dict 功能类似，对未加载的权重给出更明确的提示

    Args:
        model:
        state_dict: {name: tensor} 字典
        name_mapping: {name: name_old} 字典，默认为 None；
            当 weights_dict 与模型中的权重名称不匹配时，可以通过 name_mapping 再映射一次

    Examples:
        >>> m = nn.Linear(3, 4)  # {'weight': ..., 'bias': ...}
        >>> wd = {'w': torch.randn(4, 3), 'b': torch.randn(4)}
        >>> nm = {'weight': 'w', 'bias': 'b'}
        >>> _ = load_state_dict_explicit(m, wd, nm)
    """
    logger = get_logger()

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
    B = q_tensor.shape[0]  # B
    Q = q_tensor.shape[1]  # Q

    v_mask = v_mask.unsqueeze(1)  # [B, V] -> [B, 1, V]
    mask = torch.ones([B, Q, 1]) * v_mask  # [B, Q, V]
    return mask.to(dtype)


if __name__ == '__main__':
    """"""
    doctest.testmod()
