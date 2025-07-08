#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Time:
    2022-08-19 17:27
Author:
    huayang (imhuay@163.com)
Subject:
    trainer_wrap
References:
    https://huggingface.co/docs/transformers/training#train
"""
import os
import sys
import json
import time
import doctest
import abc

from typing import *
from pathlib import Path
from itertools import islice
from collections import defaultdict

import torch
import torch.nn as nn
from torch.utils.data import Dataset, IterableDataset

from transformers.trainer import Trainer
from transformers.modeling_utils import PreTrainedModel
from transformers.tokenization_utils_base import PreTrainedTokenizerBase
from transformers.training_args import TrainingArguments
from transformers.trainer_utils import EvalPrediction

TrainDataset = TypeVar('TrainDataset', bound=Dataset)
EvalDataset = TypeVar('EvalDataset', bound=Dataset)


class TrainPipe(abc.ABC):
    """
    References:
        https://colab.research.google.com/github/huggingface/notebooks/blob/main/examples/text_classification.ipynb
    """
    trainer: Trainer
    model: Union[PreTrainedModel, nn.Module]
    args: TrainingArguments
    ds_train: Dataset
    ds_eval: Dataset
    tokenizer: PreTrainedTokenizerBase = None

    def __init__(self):
        """"""
        self.args = self._create_args()
        self.model = self._create_model()
        self.tokenizer = self._create_tokenizer()
        self.ds_train, self.ds_eval = self._create_dataset()

        self._init_trainer()

    def train(self, **kwargs):
        """"""
        self.trainer.train(**kwargs)

    def eval(self, **kwargs):
        """"""
        self.trainer.evaluate(**kwargs)

    def _init_trainer(self):
        """"""
        self.trainer = Trainer(
            model=self.model,
            args=self.args,
            train_dataset=self.ds_train,
            eval_dataset=self.ds_eval,
            compute_metrics=self._compute_metrics
        )

    def _create_args(self) -> TrainingArguments:
        raise NotImplementedError

    def _create_model(self) -> Union[PreTrainedModel, nn.Module]:
        """"""
        raise NotImplementedError

    def _create_tokenizer(self) -> PreTrainedTokenizerBase:
        """"""
        raise NotImplementedError

    def _create_dataset(self) -> Tuple[TrainDataset, EvalDataset]:
        raise NotImplementedError

    def _compute_metrics(self, pred: EvalPrediction) -> Dict:
        raise NotImplementedError


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

    def _test_trainer(self):  # noqa
        """"""

        class DemoTrainPipe(TrainPipe):
            """"""

            def _create_args(self) -> TrainingArguments:
                pass

            def _create_model(self) -> Union[PreTrainedModel, nn.Module]:
                pass

            def _create_tokenizer(self) -> PreTrainedTokenizerBase:
                pass

            def _create_dataset(self) -> Tuple[TrainDataset, EvalDataset]:
                pass

            def _compute_metrics(self, pred: EvalPrediction) -> Dict:
                pass

        pipe = DemoTrainPipe()
        pipe.train()
        pipe.eval()


if __name__ == '__main__':
    """"""
    __Test()
