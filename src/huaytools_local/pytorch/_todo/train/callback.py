#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Time: 2021-10-16 12:56 下午

Author: huayang

Subject:

"""
import re
import doctest

from abc import ABC
from typing import *
from logging import Logger

import torch
import numpy as np

from huaytools_local.pytorch._todo import train
from huaytools_local._python.utils import get_logger

VAL_LOSS = 'val_loss'


class Callback(ABC):
    """"""
    trainer: "train.Trainer" = None  # 避免循环引用
    logger: Logger

    def __init__(self):
        """"""
        self.logger = get_logger(self.__class__.__name__)

    def __call__(self, trainer):
        """"""
        self.trainer = trainer
        # self.logger = trainer.logger
        return self

    def on_before_train(self):
        """"""

    def on_after_train(self):
        """"""

    def on_before_train_epoch(self):
        """"""

    def on_after_train_epoch(self):
        """"""

    def on_before_train_batch(self):
        """"""

    def on_after_train_batch(self):
        """"""

    def on_before_optimize_step(self):
        """"""

    def on_after_optimize_step(self):
        """"""

    def on_before_eval(self):
        """"""

    def on_after_eval(self):
        """"""

    def on_before_test(self):
        """"""

    def on_after_test(self):
        """"""


class ProgressbarCallback(Callback):
    """"""
    _w_epoch: int
    _w_step: int

    def on_before_train(self):
        """"""
        trainer = self.trainer
        self._w_epoch = len(str(trainer.num_train_epochs))  # epoch 显示宽度
        self._w_step = len(str(trainer.num_train_steps))  # step 显示宽度

    def on_after_train_batch(self):
        """"""
        self._set_progressbar_postfix()

    def on_before_train_epoch(self):
        """"""
        self._set_progressbar_postfix()
        self._set_progressbar_description()

    def on_after_optimize_step(self):
        """"""
        self._set_progressbar_description()

    def _set_progressbar_postfix(self):  # noqa
        """ 在进度条中添加其他信息 """
        trainer = self.trainer
        trainer.current_batches.set_postfix(loss=self.current_loss)

    def _set_progressbar_description(self):
        """ 更新进度条描述
        默认格式: Global Step[02/39] - Epoch(1/10):  23%|██▎       | 3/13 [00:05<00:16,  1.60s/it, loss=6.24]
        """
        trainer = self.trainer
        trainer.current_batches.set_description(
            f'Global Step[{trainer.global_step:>0{self._w_step}}/{trainer.num_train_steps}] - '
            f'Epoch({trainer.current_epoch_idx + 1:>0{self._w_epoch}}/{trainer.num_train_epochs})'
        )

    @property
    def current_loss(self):
        """"""
        try:
            return self.trainer.batch_loss.item()
        except:
            return float('nan')


class EvaluateCallback(Callback):
    """EvaluateCallback 基类

    References:
        - keras.callbacks.ModelCheckpoint
        - keras.callbacks.EarlyStopping
    """

    # config
    save_best: bool  # 是否保存最佳模型
    early_stopping: bool  # 是否应用 early stopping

    metrics_log: Dict[str, float]  # 保存所有指标
    monitor: str  # 监控指标，默认为 val_loss
    best_monitor: float  # 监控指标的最佳值
    max_maintain: int = 2  # 当连续 max_maintain 个 epoch 指标没有提升，则提前中止训练
    baseline: float = None
    better_than_baseline: bool = False

    def __init__(self,
                 metrics: Union[str, List[str]] = 'val_loss',
                 monitor: str = None,
                 compare_mode: str = None,
                 evaluate_mode: str = 'epoch',
                 num_evaluate_per_steps: int = 0,
                 save_best: bool = True,
                 early_stopping: bool = False,
                 max_maintain: int = 2,
                 baseline: float = None,
                 min_delta: float = 0.0,
                 evaluate_before_train: bool = False):
        """"""
        super().__init__()

        # 指标
        if isinstance(metrics, str):
            metrics = [metrics]
        self.metrics = metrics
        self.metrics_log = dict()

        # 监控指标
        if monitor is None:
            monitor = self.metrics[0]
        self.monitor = monitor

        # 监控指标的比较模式，越大越好还是越小越好
        if compare_mode is None:
            if re.search(r'loss', self.monitor):
                compare_mode = 'min'
            else:
                compare_mode = 'max'
        self.compare_mode = compare_mode

        self.save_best = save_best
        self.evaluate_before_train = evaluate_before_train
        self.early_stopping = early_stopping
        if self.early_stopping:
            self.max_maintain = max_maintain

            if baseline is None:
                self.logger.info(f'Note that `early_stopping=True` but `baseline` is None.')
            else:
                self.baseline = baseline

        self.min_delta = abs(min_delta)
        if self.compare_mode == 'max':
            self.compare_op = np.greater
            self.best_monitor = float('-inf')
            self.min_delta *= 1
        elif self.compare_mode == 'min':
            self.compare_op = np.less
            self.best_monitor = float('inf')
            self.min_delta *= -1
        else:
            raise ValueError('`mode` should be one of {"max", "min"}')

        assert evaluate_mode in ('step', 'epoch'), "The `evaluate_mode` should be one of ('step', 'epoch')."
        self.evaluate_mode = evaluate_mode
        if evaluate_mode == 'step':
            assert num_evaluate_per_steps > 0, "If evaluate_mode='step', " \
                                               "num_evaluate_per_steps should greater than 0"
            self.num_evaluate_per_steps = num_evaluate_per_steps

        self._n_maintain = 0  # 记录没有提升的 epoch 次数

    def compute_metrics(self, model, val_data_loader):
        """"""
        trainer = self.trainer

        total_batch = []
        total_outputs = []
        val_loss = 0.0
        batch_cnt = 0
        for batch in val_data_loader:
            batch_outputs = trainer.training_step(model, batch)
            batch_cnt += 1
            val_loss += batch_outputs[-1].mean().item()

            # TODO: 添加自定义 metric
            total_outputs.append(batch_outputs)
            total_batch.append(batch_outputs)

        self.metrics_log[VAL_LOSS] = val_loss / batch_cnt
        # for metric in self.metrics:
        #     val = getattr(self, f'compute_{metric}')(total_batch, total_outputs)
        #     self.metrics_log[metric] = val

    @torch.no_grad()
    def evaluate(self, before_train=False):
        """"""
        trainer = self.trainer

        trainer.model.eval()
        self.compute_metrics(trainer.model, trainer.val_data_loader)
        trainer.model.train()

        if trainer.current_batches:
            trainer.current_batches.clear()
        log_info = self.get_log_msg(before_train=before_train)
        self.logger.info(log_info)
        # trainer.current_batches.refresh()  # 手动刷新会使进度条保留，这跟设置 leave=False 的期望相反

        if before_train:
            self.best_monitor = self.metrics_log[self.monitor]
            return

        current_monitor = self.metrics_log[self.monitor]
        better_than_best = self._is_improvement(current_monitor, self.best_monitor)
        if better_than_best:
            self.best_monitor = current_monitor

        if not self.better_than_baseline:
            self.better_than_baseline = self._is_improvement(current_monitor, self.baseline)

        if self.better_than_baseline:  # 只有指标高于 baseline 时，才会激活 early stop
            self._n_maintain += 1
            if better_than_best:  # 如果有提升，就清零
                self._n_maintain = 0

        # save best
        if self.save_best and better_than_best:
            trainer.save_model(save_msg=log_info)

        # early stopping
        if self.early_stopping and self._n_maintain >= self.max_maintain and trainer.current_epoch_idx > 0:
            trainer.stop_training = True
            self.logger.info(f'Early stop with best {self.monitor}={self.best_monitor:.3} '
                             f'after global_step[{trainer.global_step}].')

    def get_log_msg(self, before_train=False):
        """"""
        trainer = self.trainer
        metrics_str = ', '.join(f'{name}={value:.3}' for name, value in self.metrics_log.items())

        if before_train:
            log_suffix = 'before training'
        elif self.evaluate_mode == 'step':
            log_suffix = f'after global_step[{trainer.global_step}]'
        else:  # self.evaluate_mode == 'epoch':
            log_suffix = f'after epoch({trainer.current_epoch_idx})'

        log_info = f'Evaluate metric: {metrics_str} {log_suffix}'
        return log_info

    def on_before_train(self):
        """"""
        if self.evaluate_before_train:
            self.evaluate(before_train=True)

    def on_after_optimize_step(self):
        """"""
        # if self.trainer.stop_training:
        #     return

        if self.evaluate_mode == 'step' \
                and self.trainer.global_step % self.num_evaluate_per_steps != 0:
            self.evaluate()

    def on_after_train_epoch(self):
        """"""
        # if self.trainer.stop_training:
        #     return

        if self.evaluate_mode == 'epoch':
            self.evaluate()

    def on_after_train(self):
        """"""
        if not self.save_best:
            self.trainer.save_model(save_msg=self.get_log_msg())

    def _is_improvement(self, cur, ref):
        """"""
        if ref is None:
            return True
        return self.compare_op(cur - self.min_delta, ref)


class LossEvaluateCallback(EvaluateCallback):
    """"""

    def __init__(self, **kwargs):
        """"""
        super().__init__(monitor=VAL_LOSS, compare_mode='min', **kwargs)


def _test():
    """"""
    doctest.testmod()


if __name__ == '__main__':
    """"""
    _test()
