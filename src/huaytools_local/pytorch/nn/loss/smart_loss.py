#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Time: 2022-05-18 11:31 上午

Author: huayang

Subject:

"""
import os  # noqa
import doctest  # noqa
import itertools

# from collections import defaultdict
# from itertools import islice
# from pathlib import Path
# from typing import *

# from tqdm import tqdm

import torch
import torch.nn as nn
import torch.nn.functional as F  # noqa

import huaytools_local.pytorch.backend as K  # noqa


class SMARTLoss(nn.Module):

    def __init__(
            self,
            eval_fn,
            loss_fn,
            loss_last_fn=None,
            norm_fn=K.inf_norm,
            num_steps: int = 1,
            step_size: float = 1e-3,
            epsilon: float = 1e-6,
            noise_var: float = 1e-5
    ) -> None:
        super().__init__()
        self.eval_fn = eval_fn
        self.loss_fn = loss_fn
        self.loss_last_fn = loss_last_fn if loss_last_fn is not None else loss_fn
        self.norm_fn = norm_fn
        self.num_steps = num_steps
        self.step_size = step_size
        self.epsilon = epsilon
        self.noise_var = noise_var

    def forward(self, embed, state):
        noise = torch.randn_like(embed, requires_grad=True) * self.noise_var

        for i in itertools.count():
            # Compute perturbed embed and states
            embed_perturbed = embed + noise
            state_perturbed = self.eval_fn(embed_perturbed)

            # Return final loss if last step (undetached state)
            if i == self.num_steps:
                return self.loss_last_fn(state_perturbed, state)

            # Compute perturbation loss (detached state)
            loss = self.loss_fn(state_perturbed, state.detach())

            # Compute noise gradient
            noise_gradient = torch.autograd.grad(loss, noise)[0]

            # Move noise towards gradient to change state as much as possible
            step = noise + self.step_size * noise_gradient

            # Normalize new noise step into norm induced ball
            noise = self.norm_fn(step)

            # Reset noise gradients for next step
            noise = noise.detach().requires_grad_()
