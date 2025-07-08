#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Time: 2022-06-04 11:50 上午

Author: huayang

Subject:

"""
import os  # noqa
import doctest  # noqa

# from collections import defaultdict
# from itertools import islice
# from pathlib import Path
from typing import *

# from tqdm import tqdm

import torch
import torch.nn as nn
import evaluate
from torch import Tensor

from torch.utils.data import DataLoader
from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForSequenceClassification

from huaytools_local.pytorch.train.trainer import Trainer


def get_sst2_dataloader(model_name='roberta-base', batch_size=32):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    data = load_dataset('glue', 'sst2')
    ds_train, ds_val = data['train'], data['validation']

    def process_fn(txt):
        return tokenizer(txt['sentence'], truncation=True, padding='longest', return_token_type_ids=True)

    def get_dataloader(ds):  # noqa
        ds = ds.map(process_fn, batched=True)
        ds = ds.map(lambda x: {'labels': x['label']}, batched=True)
        ds.set_format(type='torch', columns=['input_ids', 'token_type_ids', 'attention_mask', 'labels'])

        return DataLoader(ds, batch_size=batch_size)

    dl_train, dl_val = get_dataloader(ds_train), get_dataloader(ds_val)
    return dl_train, dl_val


class MyTrainer(Trainer):
    accuracy = evaluate.load("accuracy")
    loss_fn = nn.CrossEntropyLoss()

    def init_model(self):
        """"""
        self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name, num_labels=2)

    def init_dataset(self, batch_size):
        """"""
        self.data_train, self.data_val = get_sst2_dataloader(model_name=self.model_name,
                                                             batch_size=batch_size)

    def training_step(self, batch) -> Union[Tensor, Tuple[Tensor, ...]]:
        labels = batch.pop('labels')
        logits = self.model(**batch).logits
        loss = self.loss_fn(logits, labels)
        return logits, loss

    def on_after_train_epoch(self):
        """"""
        for batch in self.data_val:
            refs = batch['labels']  # 从 batch 中提取 labels
            batch.pop('labels')
            logits, _ = self.training_step(batch)
            preds = torch.argmax(logits, dim=-1)
            self.accuracy.add_batch(references=refs, predictions=preds)

        ret = self.accuracy.compute()
        self.logger.info(f'After train {self.epoch_idx} epoch, val acc={ret}')


def main():
    model_name = r'roberta-base'
    trainer = MyTrainer(batch_size=32, model_name=model_name)
    trainer.train()


if __name__ == '__main__':
    """"""
    main()
