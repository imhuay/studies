#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Time:
   2021-07-19 3:26 下午
   
Author:
   huayang
   
Subject:
   
"""
import torch
import torch.nn as nn
import torch.nn.functional as F


class SpanEncoder(nn.Module):
    """"""

    def __init__(self, num_classes, hidden_size, dropout_prob=0.1, loss_fn=None, soft_label=True):
        """"""
        super(SpanEncoder, self).__init__()

        self.num_classes = num_classes
        self.clf_start = nn.Linear(hidden_size, num_classes)

        self.soft_label = soft_label
        if soft_label:
            self.fc_end = nn.Linear(hidden_size + num_classes, hidden_size)
        else:
            self.fc_end = nn.Linear(hidden_size + 1, hidden_size)

        self.ln = nn.LayerNorm(hidden_size)
        self.clf_end = nn.Linear(hidden_size, num_classes)

        self.act = nn.Tanh()
        self.dropout = nn.Dropout(dropout_prob)
        self.softmax = nn.Softmax(-1)

        self.loss = loss_fn or nn.CrossEntropyLoss()

    def _forward_start(self, hidden_states):
        """"""
        return self.clf_start(hidden_states)

    def _forward_end(self, hidden_states, label_prob=None):
        """"""
        # assert hidden_states.shape[:2] == label_prob.shape[:2]
        inputs = torch.cat([hidden_states, label_prob], dim=-1)
        x = self.fc_end(inputs)
        x = self.ln(self.act(x))
        x = self.clf_end(x)
        return x

    def compute_loss(self, hidden_states, labels=None, mask=None):
        """"""
        start_prob = self._forward_start(hidden_states)

        start_labels, end_labels = labels
        if self.soft_label:
            label_prob = F.one_hot(start_labels, num_classes=self.num_classes)
        else:
            label_prob = start_labels.unsqueeze(2).float()

        end_prob = self._forward_end(hidden_states, label_prob)

        start_prob = start_prob.view(-1, self.num_classes)
        end_prob = end_prob.view(-1, self.num_classes)

        if mask:
            active_idx = mask.view(-1) == 1
            start_prob = start_prob[active_idx]
            start_labels = start_labels[active_idx]
            end_prob = end_prob[active_idx]
            end_labels = end_labels[active_idx]

        start_loss = self.loss_fn(start_prob, start_labels)
        end_loss = self.loss_fn(end_prob, end_labels)
        total_loss = (start_loss + end_loss) / 2.0

        return total_loss, start_prob, end_prob

    def forward(self, hidden_states, mask=None):
        """
        Args:
            hidden_states: [B, L, N]
            mask:

        Returns:

        """
        start_prob = self._forward_start(hidden_states)

        label_prob = self.softmax(start_prob, -1)
        if not self.soft_label:
            label_prob = torch.argmax(label_prob, dim=-1).unsqueeze(2).float()

        end_prob = self._forward_end(hidden_states, label_prob)
        return start_prob, end_prob
