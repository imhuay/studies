#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Time: 2022-06-03 10:32 下午

Author: huayang

Subject:

"""
import os  # noqa
import doctest  # noqa
import math

# from collections import defaultdict
# from itertools import islice
# from pathlib import Path
from typing import *
from abc import ABC, abstractmethod

from tqdm import tqdm

import torch
import torch.nn as nn

from torch import Tensor
from torch.optim import Optimizer
from torch.optim.lr_scheduler import LambdaLR
from torch.utils.data import DataLoader
from accelerate import Accelerator

from huaytools.utils import BunchDict
from huaytools.utils import get_logger, get_time_string, get_attr, set_attr, get_caller_name
from huaytools.pytorch.utils import set_seed


class BaseTrainer(ABC):
    """"""
    logger = get_logger()
    args = BunchDict()

    # modules
    accelerator = None
    model: nn.Module = None
    optimizer: Optimizer = None
    scheduler: Union[LambdaLR, Any] = None
    data_train: DataLoader = None
    data_val: DataLoader = None

    # states
    global_step: int = 0
    epoch_idx: int = None
    batches: tqdm = None
    batch: Union[List, Dict, Any] = None
    batch_idx: int = None
    batch_loss: torch.Tensor = None
    stop_training: bool = False

    _w_epoch: int = None  # epoch 显示宽度
    _w_step: int = None  # step 显示宽度

    def __init__(self,
                 model: nn.Module = None,
                 data_train: DataLoader = None,
                 data_val: DataLoader = None,
                 optimizer_type: Union[str, type] = 'AdamW',
                 batch_size: int = None,
                 learning_rate: float = 5e-5,
                 weight_decay: float = 0.01,
                 no_decay_params: Tuple[str] = ('bias', 'LayerNorm.weight'),
                 num_train_epochs: int = 3,
                 num_train_steps: int = None,
                 num_warmup_steps: int = None,  # default num_train_steps * 0.1
                 num_gradient_accumulation: int = 1,
                 random_seed: int = None,
                 use_cpu_device: bool = False,
                 save_dir: str = None,
                 model_name: str = None,
                 save_model_state_dict: bool = True,
                 save_model_old_format: bool = False,
                 auto_optimizing: bool = True,
                 **kwargs):
        """"""
        self.model = model
        self.data_train = data_train
        self.data_val = data_val

        args = self.args
        args.optimizer_type = optimizer_type
        args.batch_size = batch_size
        args.learning_rate = learning_rate
        args.weight_decay = weight_decay
        args.no_decay_params = no_decay_params
        args.num_train_epochs = num_train_epochs
        args.num_train_steps = num_train_steps
        args.num_warmup_steps = num_warmup_steps
        args.num_gradient_accumulation = num_gradient_accumulation

        args.random_seed = random_seed
        args.use_cpu_device = use_cpu_device

        args.save_dir = save_dir
        args.model_name = model_name
        args.save_model_state_dict = save_model_state_dict
        args.save_model_old_format = save_model_old_format
        args.auto_optimizing = auto_optimizing
        args.update(kwargs)

    def train(self):
        """"""
        self.on_before_train()

        for self.epoch_idx in range(self.num_train_epochs):
            if self.stop_training:
                break

            self.batches = tqdm(self.data_train, leave=(self.epoch_idx == (self.num_train_epochs - 1)))

            self.on_before_train_epoch()
            for self.batch_idx, self.batch in enumerate(self.batches):
                if self.stop_training:
                    break

                self.on_before_train_batch()

                # training step begin
                output = self.training_step(self.batch)
                batch_loss = output if isinstance(output, Tensor) else output[-1]
                self.batch_loss = batch_loss.mean() / self.num_gradient_accumulation
                self.loss_backward()
                self.optimizing_step()
                self.global_step += 1
                # training step end

                self.on_after_train_batch()

            self.on_after_train_epoch()

        self.on_after_train()

    @abstractmethod
    def training_step(self, batch) -> Union[Tensor, Tuple[Tensor, ...]]:
        """
        Returns:
            1.单独返回 loss；
            2.如果有多个返回值，loss 放在最后一个
        """
        raise NotImplementedError

    def loss_backward(self):
        """"""
        if self.accelerator is not None:
            self.accelerator.backward(self.batch_loss)
        else:
            self.batch_loss.backward()

    def optimizing_step(self):
        """"""
        if not self._update_gradient():
            return

        self.optimizer.step()
        self.scheduler.step()
        self.optimizer.zero_grad()

    def _update_gradient(self):
        return ((self.batch_idx + 1) % self.num_gradient_accumulation == 0) \
               or (self.batch_idx + 1) == len(self.data_train)

    def init_accelerator(self):
        """"""
        self.accelerator = Accelerator(cpu=self.use_cpu_device)

    def init_model(self):
        """"""
        if self.model is None:
            raise NotImplementedError

    def init_dataset(self, batch_size):  # noqa
        """"""
        if self.data_train is None:
            raise NotImplementedError

    def init_optimizer(self, model):
        """"""
        from huaytools.pytorch.train.utils import default_optimizer
        self.optimizer = default_optimizer(model, self.optimizer_type, self.learning_rate,
                                           self.weight_decay, self.no_decay_params)

    def init_scheduler(self, optimizer):
        """"""
        from huaytools.pytorch.train.utils import default_scheduler
        self.scheduler = default_scheduler(optimizer, self.num_warmup_steps, self.num_train_steps)

    def on_before_train(self):
        """"""
        set_seed(self.random_seed)
        self.init_accelerator()
        self.init_model()
        self.init_dataset(self.batch_size)
        self.init_optimizer(self.model)
        self.init_scheduler(self.optimizer)

        # accelerator.prepare
        if self.accelerator is not None:
            self.model, self.data_train, self.data_val, self.optimizer = self.accelerator.prepare(
                self.model, self.data_train, self.data_val, self.optimizer)

        # 设置训练状态
        self.model.train()

        # 其他信息
        self._w_epoch = len(str(self.num_train_epochs))
        self._w_step = len(str(self.num_train_steps))

    def on_after_train(self):
        """"""

    def on_before_train_epoch(self):
        """"""

    def on_after_train_epoch(self):
        """"""
        self.save_model()

    def on_before_train_batch(self):
        """"""
        self._set_progressbar_description()
        self._set_progressbar_postfix()

    def on_after_train_batch(self):
        """"""
        if self.global_step >= self.num_train_steps:
            self.stop_training = True

        self._set_progressbar_description()
        self._set_progressbar_postfix()

    def on_before_optimize_step(self):
        """"""

    def on_after_optimize_step(self):
        """"""

    def save_model(self):
        """"""
        os.makedirs(self.save_dir, exist_ok=True)
        save_obj = self.model.state_dict() if self.save_model_state_dict else self.model
        if self.model_name is None:
            self.model_name = f'{self.model.__class__.__name__}_{get_time_string()}.pt'
        model_save_path = os.path.join(self.save_dir, self.model_name)
        config_save_path = os.path.join(self.save_dir, 'config.json')

        # 保存模型，以及训练参数
        torch.save(save_obj, model_save_path, _use_new_zipfile_serialization=not self.save_model_old_format)
        self.save(config_save_path)
        self.logger.info(f'model saved at {model_save_path}')

    def _set_progressbar_postfix(self):  # noqa
        """ 在进度条中添加其他信息 """

        def default(batch_loss):
            try:
                return batch_loss.item()
            except:
                return float('nan')

        self.batches.set_postfix(loss=default(self.batch_loss))

    def _set_progressbar_description(self):
        """ 更新进度条描述
        默认格式: Global Step[02/39] - Epoch(1/10):  23%|██▎       | 3/13 [00:05<00:16,  1.60s/it, loss=6.24]
        """
        self.batches.set_description(
            f'Global Step[{self.global_step:>0{self._w_step}}/{self.num_train_steps}] - '
            f'Epoch({self.epoch_idx + 1:>0{self._w_epoch}}/{self.num_train_epochs})'
        )

    # === special args property ===
    def _get_args(self, name: str = None):
        name = name or get_caller_name()  # 获取调用函数名（这里就是属性名）
        return get_attr(self.args, name)

    def _set_args(self, value, name: str = None):
        name = name or get_caller_name()  # 获取调用函数名（这里就是属性名）
        set_attr(self.args, name, value)

    @property
    def num_train_steps(self):
        value = self._get_args()
        if value is None:
            value = self.num_train_epochs * math.ceil(
                len(self.data_train) / self.num_gradient_accumulation)
            self._set_args(value)

        return value

    @property
    def num_warmup_steps(self):
        value = self._get_args()
        if value is None:
            value = self.num_train_steps * 0.1
            self._set_args(value)
        return value

    def __getattr__(self, item):
        """"""
        return get_attr(self.args, item)
