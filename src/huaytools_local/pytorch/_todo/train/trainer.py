#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Time: 2021-07-16 1:21 下午

Author: huayang

Subject:

"""
import os
import math

from typing import *
from abc import ABC, abstractmethod
from logging import Logger

import torch
import torch.nn as nn

from tqdm import tqdm
from torch import Tensor
from torch.optim import Optimizer
from torch.optim.lr_scheduler import LambdaLR
from torch.utils.data import DataLoader
from accelerate import Accelerator

from huaytools_local._python.custom import BunchDict
from huaytools_local._python.utils import get_logger, set_attr, get_attr, get_print_json, get_caller_name

from huaytools_local.pytorch.utils import set_seed
from huaytools_local.pytorch._todo.train.callback import Callback, EvaluateCallback, ProgressbarCallback
from huaytools_local.pytorch._todo.train.scheduler import get_linear_schedule_with_warmup
from huaytools_local.pytorch._todo.train import (
    get_parameters_for_weight_decay,
    get_model_save_dir,
    get_optimizer_by_name,
    STR2OPT
)

# TODO
# from my.pytorch.train.accelerator import SimpleAccelerator

__all__ = [
    'Trainer'
]


class Trainer(ABC):
    """@Pytorch Utils
    Trainer 基类

    Examples:
        # See examples/pytorch_trainer/*

    Note: （约定）TODO
        1.
    """
    logger: Logger

    # config
    args: BunchDict

    # modules
    model: nn.Module
    optimizer: Optimizer
    scheduler: Union[LambdaLR, Any]
    accelerator: Accelerator
    callbacks: List[Callback] = None

    # data loader
    train_data_loader: DataLoader
    val_data_loader: DataLoader = None
    test_data_loader: DataLoader = None

    # inner state
    global_step = 0
    stop_training: bool = False
    continue_training: bool = False  # TODO
    updating_gradient: bool = True
    current_epoch_idx: int = 0
    current_batches: tqdm = None
    current_batch: Union[List, Dict, Any] = None
    current_batch_idx: int = 0
    batch_loss: torch.Tensor = None
    has_set_model: bool = False

    def __init__(self,
                 # training args:
                 batch_size: int = 32,
                 optimizer_type: Union[str, Type[Optimizer]] = 'AdamW',
                 learning_rate: float = 5e-5,
                 weight_decay: float = 0.01,
                 no_decay_params: Tuple[str] = ('bias', 'LayerNorm.weight'),
                 num_train_epochs: int = 3,
                 num_train_steps: int = None,  # infer by train_dataset
                 num_warmup_steps: int = None,  # num_train_steps * 0.1
                 num_gradient_accumulation: int = 1,
                 use_cpu_device: bool = False,
                 save_dir: str = None,
                 save_model_state_dict: bool = True,
                 save_model_old_format: bool = False,
                 random_seed: int = None,
                 # trainer args
                 evaluate_callback: EvaluateCallback = None,
                 auto_optimizing: bool = True,
                 show_progressbar: bool = True):
        """

        Args:
            batch_size:
            optimizer_type:
            learning_rate:
            weight_decay:
            no_decay_params:
            num_train_epochs:
            num_train_steps: infer by train_dataset
            num_warmup_steps: default num_train_steps * 0.1, set 0 to make warmup disabled
            num_gradient_accumulation:
            use_cpu_device:
            save_dir:
            save_model_state_dict:
            save_model_old_format:
            random_seed:
            evaluate_callback:
            auto_optimizing:
            show_progressbar:
        """
        self.logger = get_logger(self.__class__.__name__)

        self.args = BunchDict()
        # properties which will be saved to `self.args`
        self.random_seed = random_seed
        self.batch_size = batch_size
        self.optimizer_type = optimizer_type
        self.learning_rate = learning_rate
        self.weight_decay = weight_decay
        self.no_decay_params = no_decay_params
        self.num_train_epochs = num_train_epochs
        self.num_train_steps = num_train_steps
        self.num_warmup_steps = num_warmup_steps
        self.num_gradient_accumulation = num_gradient_accumulation
        self.use_cpu_device = use_cpu_device
        self.save_dir = save_dir
        self.save_model_state_dict = save_model_state_dict
        self.save_model_old_format = save_model_old_format

        self.auto_optimizing = auto_optimizing

        if show_progressbar:
            progressbar_callback = ProgressbarCallback()
            self.add_callback(progressbar_callback, 0)

        if evaluate_callback is None:
            evaluate_callback = EvaluateCallback(evaluate_before_train=True)
        self.add_callback(evaluate_callback)

    def train(self):
        """"""
        self.on_before_train()

        for self.current_epoch_idx in range(self.num_train_epochs):
            if self.stop_training:
                break

            self.on_before_train_epoch()

            for self.current_batch_idx, self.current_batch in enumerate(self.current_batches):
                if self.stop_training:
                    break

                self.on_before_train_batch()

                if self.auto_optimizing:
                    loss = self.training_step(self.model, self.current_batch)[-1]
                    self.batch_loss = loss.mean() / self.num_gradient_accumulation
                    self.loss_backward(self.batch_loss)

                    # gradient_accumulation
                    self.updating_gradient = ((self.current_batch_idx + 1) % self.num_gradient_accumulation == 0) \
                                             or (self.current_batch_idx + 1) == len(self.train_data_loader)  # noqa
                    if self.updating_gradient:
                        self.on_before_optimize_step()

                        # 注意顺序: loss.backward() -> optimizer.step() -> scheduler.step() -> optimizer.zero_grad()
                        # 因为可能存在累积梯度，因此 optimizer.zero_grad() 须在 optimizer.step() 之后
                        self.optimizer.step()
                        self.scheduler.step()
                        self.optimizer.zero_grad()
                        self.global_step += 1
                        if self.global_step >= self.num_train_steps:
                            self.stop_training = True

                        self.on_after_optimize_step()
                else:
                    # 如果 auto_optimizing 为 False，则需要在 training_step 中手动完成更新
                    # 比如在强化学习中，有两个学习器需要交替更新，auto_optimizing 就无法完成
                    self.batch_loss = self.training_step(self.model, self.current_batch)[-1]

                self.on_after_train_batch()

            self.on_after_train_epoch()

        self.on_after_train()

    def training_step(self, model, batch) -> Tuple[Any, Tensor]:
        """
        Returns: 1.单独返回 loss；2.如果有多个返回值，loss 放在最后一个
        """
        try:
            if isinstance(batch, Dict):
                outputs = model(**batch)
            elif isinstance(batch, Sequence):
                outputs = model(*batch)
            else:
                outputs = model(batch)
        except:
            raise RuntimeError(f'Default {self.training_step.__name__} cannot parse the model and batch, '
                               f'overwrite the {self.training_step.__name__} to define how the model read batch. '
                               f'Note that if there are more than one outputs, put the loss at last.')

        if isinstance(outputs, Tensor):
            outputs = (outputs,)
        elif isinstance(outputs, Sequence) and isinstance(outputs[-1], Tensor):
            outputs = tuple(outputs)
        else:
            raise TypeError(f'The {self.training_step.__name__} should return `loss` or `(..., loss)`')

        return outputs

    @abstractmethod
    def set_model(self):
        """"""
        raise NotImplementedError

    @abstractmethod
    def set_data_loader(self, batch_size):
        """"""
        raise NotImplementedError

    def loss_backward(self, loss):
        """"""
        if self.accelerator is not None:
            self.accelerator.backward(loss)
        else:
            loss.backward()

    def add_callback(self, callback: Callback, idx=-1):
        """"""
        if self.callbacks is None:
            self.callbacks = []
        self.callbacks.insert(idx, callback(self))

    # def set_callbacks(self):
    #     """"""
    #     if self.use_default_progressbar:
    #         self.add_callback(ProgressbarCallback()(self), 0)
    #
    #     if all(not isinstance(c, EvaluateCallback) for c in self.callbacks):
    #         self.add_callback(LossEvaluateCallback()(self))

    def set_optimizer(self, model: nn.Module):
        """"""
        parameters = get_parameters_for_weight_decay(model, self.learning_rate,
                                                     self.weight_decay, self.no_decay_params)
        self.optimizer = get_optimizer_by_name(self.optimizer_type)(parameters)

    def set_scheduler(self, optimizer: Optimizer, num_train_steps):
        """"""
        self.scheduler = get_linear_schedule_with_warmup(optimizer, self.num_warmup_steps, num_train_steps)

    def set_accelerator(self):
        """"""
        self.accelerator = Accelerator(cpu=self.use_cpu_device)

    def accelerate_prepare(self):
        """"""
        self.model, self.train_data_loader, self.optimizer = self.accelerator.prepare(
            self.model, self.train_data_loader, self.optimizer)

        if self.val_data_loader is not None:
            self.val_data_loader = self.accelerator.prepare(self.val_data_loader)

        if self.test_data_loader is not None:
            self.test_data_loader = self.accelerator.prepare(self.test_data_loader)

    def on_before_train(self):
        """"""
        # init
        set_seed(self.random_seed)

        if not self.has_set_model:
            self.set_model()
        self.set_accelerator()  # 设置 device，需要用到 device 放在这之后
        self.set_data_loader(self.batch_size)
        self.set_optimizer(self.model)
        self.set_scheduler(self.optimizer, self.num_train_steps)
        self.accelerate_prepare()
        self.log_train_state()
        self.model.train()

        for callback in self.callbacks:
            callback.on_before_train()

    def on_after_train(self):
        """"""
        if not os.path.exists(self.save_dir):
            self.save_model()

        for callback in self.callbacks:
            callback.on_after_train()

    def on_before_train_epoch(self):
        """"""
        # if self.stop_training:
        #     return

        self.current_batches = tqdm(self.train_data_loader,
                                    leave=(self.current_epoch_idx == (self.num_train_epochs - 1)))

        for callback in self.callbacks:
            callback.on_before_train_epoch()

    def on_after_train_epoch(self):
        """"""
        # if self.stop_training:
        #     return

        self.current_batches.clear()
        self.current_batches.close()

        for callback in self.callbacks:
            callback.on_after_train_epoch()

    def on_before_train_batch(self):
        """"""
        # if self.stop_training:
        #     return

        for callback in self.callbacks:
            callback.on_before_train_batch()

    def on_after_train_batch(self):
        """"""
        # if self.stop_training:
        #     return

        for callback in self.callbacks:
            callback.on_after_train_batch()

    def on_before_optimize_step(self):
        """"""
        # if self.stop_training:
        #     return

        for callback in self.callbacks:
            callback.on_before_optimize_step()

    def on_after_optimize_step(self):
        """"""
        # if self.stop_training:
        #     return

        for callback in self.callbacks:
            callback.on_after_optimize_step()

    def save_model(self, save_msg: str = '', model_name=None, save_config=True):
        """"""
        os.makedirs(self.save_dir, exist_ok=True)
        save_obj = self.model.state_dict() if self.save_model_state_dict else self.model
        if model_name is not None:
            self.model_name = model_name
        model_save_path = os.path.join(self.save_dir, self.model_name)

        # 保存模型
        torch.save(save_obj, model_save_path, _use_new_zipfile_serialization=not self.save_model_old_format)

        if save_msg != '':
            with open(os.path.join(self.save_dir, 'save_log.txt'), 'a', encoding='utf8') as fw:
                fw.write(save_msg + '\n')

        if save_config:
            # 保存配置
            config_path = os.path.join(self.save_dir, self.config_name)
            self.args.save(config_path)

        self.logger.info(f'model saved at {model_save_path}')

    @classmethod
    def from_trained(cls, save_dir, config_name='train_config.json'):
        """"""
        # TODO: 未完成
        trainer = cls()
        config_path = os.path.join(save_dir, config_name)
        trainer.args = BunchDict.load(config_path)

        model_path = os.path.join(save_dir, trainer.model_name)
        model = torch.load(model_path)
        if trainer.save_model_state_dict:
            trainer.set_model()
            trainer.model.load_state_dict(model)
        else:
            trainer.model = model
        trainer.has_set_model = True

        return trainer

    def log_train_state(self):
        self.logger.info(f'Config({len(self.args)}): {get_print_json(self.args)}')
        self._log_data_loader(self.train_data_loader, 'Train')
        self._log_data_loader(self.val_data_loader, 'Val')
        self._log_data_loader(self.test_data_loader, 'Test')

    def _log_data_loader(self, data_loader, dl_name):
        if data_loader and hasattr(data_loader.dataset, '__len__'):
            self.logger.info(f'{dl_name} data size: {len(data_loader.dataset)}')  # noqa

    # === train args ===
    def _get_attr(self, name: str = None):
        name = name or get_caller_name()  # 获取调用函数名（这里就是属性名）
        return get_attr(self.args, name)

    def _set_attr(self, value, name: str = None):
        name = name or get_caller_name()  # 获取调用函数名（这里就是属性名）
        set_attr(self.args, name, value)

    @property
    def device(self):
        try:
            value = self._get_attr()
        except:
            value = self.accelerator.device.type
            self._set_attr(value)
        return value

    @property
    def batch_size(self):
        return self._get_attr()

    @batch_size.setter
    def batch_size(self, value):
        self._set_attr(value)

    @property
    def val_batch_size(self):
        try:
            value = self._get_attr()
        except:
            value = self._get_attr('batch_size')
            self._set_attr(value)

        return value

    @val_batch_size.setter
    def val_batch_size(self, value):
        self._set_attr(value)

    @property
    def test_batch_size(self):
        try:
            value = self._get_attr()
        except:
            value = self._get_attr('batch_size')
            self._set_attr(value)

        return value

    @test_batch_size.setter
    def test_batch_size(self, value):
        self._set_attr(value)

    @property
    def num_train_epochs(self):
        return self._get_attr()

    @num_train_epochs.setter
    def num_train_epochs(self, value):
        self._set_attr(value)

    @property
    def num_train_steps(self):
        value = self._get_attr()  # default = -1
        if value is None:
            value = self.num_train_epochs * math.ceil(
                len(self.train_data_loader) / self.num_gradient_accumulation)
            self._set_attr(value)

        return value

    @num_train_steps.setter
    def num_train_steps(self, value):
        self._set_attr(value)

    @property
    def num_warmup_steps(self):
        value = self._get_attr()
        if value is None:
            value = self.num_train_steps * 0.1  # TODO: default value
            self._set_attr(value)
        return value

    @num_warmup_steps.setter
    def num_warmup_steps(self, value):
        self._set_attr(value)

    @property
    def num_gradient_accumulation(self):
        return self._get_attr()

    @num_gradient_accumulation.setter
    def num_gradient_accumulation(self, value):
        self._set_attr(value)

    @property
    def use_cpu_device(self):
        return self._get_attr()

    @use_cpu_device.setter
    def use_cpu_device(self, value):
        self._set_attr(value)

    @property
    def learning_rate(self):
        return self._get_attr()

    @learning_rate.setter
    def learning_rate(self, value):
        self._set_attr(value)

    @property
    def weight_decay(self):
        return self._get_attr()

    @weight_decay.setter
    def weight_decay(self, value):
        self._set_attr(value)

    @property
    def no_decay_params(self):
        return self._get_attr()

    @no_decay_params.setter
    def no_decay_params(self, value):
        self._set_attr(value)

    @property
    def optimizer_type(self):
        return self._get_attr()

    @optimizer_type.setter
    def optimizer_type(self, value):
        if isinstance(value, type):
            # from huaytools.python.utils import get_typename
            # type_name = get_typename(value)
            # TODO: 支持自定义 opt（另外保存下来）
            STR2OPT[value.__name__] = value
            value = value.__name__
        self._set_attr(value)

    @property
    def save_dir(self):
        return self._get_attr()

    @save_dir.setter
    def save_dir(self, value):
        if value is None:
            value = get_model_save_dir()
        self._set_attr(value)

    @property
    def save_model_state_dict(self):
        return self._get_attr()

    @save_model_state_dict.setter
    def save_model_state_dict(self, value):
        self._set_attr(value)

    @property
    def save_model_old_format(self):
        return self._get_attr()

    @save_model_old_format.setter
    def save_model_old_format(self, value):
        self._set_attr(value)

    @property
    def random_seed(self):
        return self._get_attr()

    @random_seed.setter
    def random_seed(self, value):
        if value is None:
            value = torch.seed()
        self._set_attr(value)

    @property
    def model_name(self):
        try:
            value = self._get_attr()
        except:
            value = self.model.__class__.__name__ + '.pt'
            self._set_attr(value)
        return value

    @model_name.setter
    def model_name(self, value):
        self._set_attr(value)

    @property
    def config_name(self):
        try:
            value = self._get_attr()
        except:
            value = 'train_config.json'
            self._set_attr(value)
        return value

    @config_name.setter
    def config_name(self, value):
        self._set_attr(value)
