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
# from abc import ABC, abstractmethod

from tqdm import tqdm

import torch
import torch.nn as nn

from torch import Tensor
from torch.optim import Optimizer
from torch.optim.lr_scheduler import LambdaLR
from torch.utils.data import DataLoader
from accelerate import Accelerator

from huaytools_local.utils import BunchDict
from huaytools_local.utils import get_logger, get_time_string, get_attr, set_attr, get_caller_name

from huaytools_local.pytorch.utils import TorchUtils

_ARGS = 'args'


class Trainer:
    """
    Notes:
        关于的 Trainer 的成员变量说明
            Trainer 内部的成员变量分为三类（均可以通过 self.xxx 进行访问）：
                一是 model、optimizer、scheduler、data 等复杂对象；
                二是 learning_rate、num_train_epochs 等超参数，这部分成员统一保存在 self.args 中，
                    并通过重写 `__getattribute__` 使 `self.xxx` 等价于 `self.args.xxx`；
                三是训练过程中的内部状态，如 batch_idx、global_step 等；

        对继承 Trainer 的子类，如果需要添加新的参数（成员变量），推荐以下写法：
            ```python
            class MyTrainer(Trainer):
                # 复杂类型的对象，或不需要保存到 `self.args` 的其他变量直接初始化
                logger = get_logger()
                # 简单类型，且需要保存到 `self.args` 中的超参数仅声明，并在实例化 Trainer 时赋值
                alpha: float
                ...

            trainer = MyTrainer(alpha=2)  # 需要保存到 `self.args` 中的超参数在这里初始化
            ```
    """
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

    def training_step(self, batch) -> Union[Tensor, Tuple[Tensor, ...]]:
        """
        Returns:
            1.单独返回 loss；
            2.如果有多个返回值，loss 放在最后一个
        """
        try:
            if isinstance(batch, Dict):
                outputs = self.model(**batch)
            elif isinstance(batch, (List, Tuple)):
                outputs = self.model(*batch)
            else:
                outputs = self.model(batch)
        except:
            raise NotImplementedError(f'Default `{self.training_step.__name__}` cannot parse the model and batch, '
                                      f'overwriting it to define how the model read batch. '
                                      f'If there are more than one outputs, put the loss at last.')

        if isinstance(outputs, Tensor):
            outputs = (outputs,)
        elif isinstance(outputs, (List, Tuple)) and isinstance(outputs[-1], Tensor):
            outputs = tuple(outputs)
        else:
            raise TypeError(f'The {self.training_step.__name__} should return `loss` or `(..., loss)`')

        return outputs

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
        from huaytools_local.pytorch.train.utils import default_optimizer
        self.optimizer = default_optimizer(model, self.optimizer_type, self.learning_rate,
                                           self.weight_decay, self.no_decay_params)

    def init_scheduler(self, optimizer):
        """"""
        from huaytools_local.pytorch.train.utils import default_scheduler
        self.scheduler = default_scheduler(optimizer, self.num_warmup_steps, self.num_train_steps)

    def on_before_train(self):
        """"""
        TorchUtils.set_seed(self.random_seed)
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
        model_save_path = os.path.join(self.save_dir, self.model_name)
        config_save_path = os.path.join(self.save_dir, 'config.json')

        # 保存模型和参数
        torch.save(save_obj, model_save_path, _use_new_zipfile_serialization=not self.save_model_old_format)
        self.save(config_save_path)
        self.logger.info(f'model saved at {model_save_path}')

    def _set_progressbar_postfix(self):  # noqa
        """ 在进度条中添加其他信息 """

        def default(batch_loss):
            try:
                return batch_loss.item()
            except:  # noqa
                return float('nan')

        self.batches.set_postfix(loss=default(self.batch_loss))

    def _set_progressbar_description(self):
        """ 进度条描述
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

    @property
    def model_name(self):
        value = self._get_args()
        if value is None:
            value = f'{self.model.__class__.__name__}_{get_time_string()}.pt'
            self._set_args(value)
        return value

    # def __getattr__(self, item):
    #     """"""
    #     return get_attr(self.args, item)

    def __getattribute__(self, item):
        """
        Notes:
            为什么用 __getattribute__ 而不是 `__getattr__`？
                首先明确两者的区别，`__getattribute__` 优先级高于 `__getattr__`，只有当前者找不到时，才会调用后者；
                其次见以下示例：
                ```python
                # 某个自定义 Trainer
                class MyTrainer(Trainer):
                    a = 1  # 某个超参数
                    ...

                # 实例化该 trainer
                trainer = MyTrainer(a=2)
                print(trainer.a)  # 2
                ```
                根据直觉，以上代码的意思应该是 `trainer.a` 的默认值为 1，并初始化为 2；
                如果使用 `__getattr__`，那么 `a=1` 的优先级将高于 `a=2`，导致 `self.a == 1` 而 `self.args.a == 2`，与期望不符，
                因此这里要用 `__getattribute__`，并优先访问 `self.args` 中的值。

            注意：在 `__getattribute__` 中调用 `self.xxx` 且 `xxx` 为成员变量时可能会造成无限递归。
        """
        if item == _ARGS:
            return super().__getattribute__(item)  # return self.args 会导致无限递归
        else:
            return get_attr(self.args, item, super().__getattribute__(item))
