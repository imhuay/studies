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


class ETFLinear(nn.Module):
    """
    References:
        [[2203.09081] Do We Really Need a Learnable Classifier at the End of Deep Neural Network?](https://arxiv.org/abs/2203.09081)
    """

    def __init__(self, d_in, d_out, bias=False, requires_grad=False):
        """"""
        super().__init__()

        self.weight = torch.nn.Parameter(K.simplex_equiangular_tight_frame(d_out, d_in))
        if bias:
            self.bias = torch.nn.Parameter(torch.zeros(d_out))
        else:
            self.register_parameter('bias', None)
        self.requires_grad_(requires_grad)

    def forward(self, x):
        """"""
        return F.linear(x, self.weight, self.bias)



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


class TripletLoss(nn.Module):
    """

    Examples:
        >>> a, p, n = torch.randn(10, 12), torch.randn(10, 12), torch.randn(10, 12)
        >>> # 对比官方 triplet_loss
        >>> my_tl = TripletLoss(reduce_fn=K.identity)
        >>> tl = nn.TripletMarginLoss(margin=2.0, p=2, reduction='none')
        >>> assert torch.allclose(my_tl(a, p, n), tl(a, p, n), atol=1e-5)
        >>> # 对比官方支持自定义距离的 triplet_loss
        >>> mt_tl = TripletLoss(distance_fn=K.cosine_distance, reduce_fn=K.identity)
        >>> tld = nn.TripletMarginWithDistanceLoss(distance_function=K.cosine_distance, margin=2.0, reduction='none')
        >>> assert torch.allclose(mt_tl(a, p, n), tld(a, p, n), atol=1e-5)

    """

    def __init__(self, distance_fn=K.euclidean_distance, margin=2.0, reduce_fn=torch.mean):
        """"""
        super().__init__()
        self.distance_fn = distance_fn
        self.reduce_fn = reduce_fn
        self.margin = margin

    def forward(self, anchor, positive, negative):
        """"""
        loss = K.compute_triplet_loss(anchor, positive, negative,
                                      distance_fn=self.distance_fn, margin=self.margin)
        return self.reduce_fn(loss)


class RDropLoss(nn.Module):
    """
    References:
        [dropreg/R-Drop](https://github.com/dropreg/R-Drop)
    """

    def __init__(self, alpha=1.0, ce_reduce_fn=torch.mean, kl_reduce_fn=torch.sum, mask_value=0):
        """"""
        super().__init__()

        self.alpha = alpha
        self.cross_entropy = nn.CrossEntropyLoss(reduction='none')
        self.ce_reduce_fn = ce_reduce_fn
        self.kl_reduce_fn = kl_reduce_fn
        self.mask_value = mask_value

    def compute_ce_loss(self, logits1, logits2, labels):
        ce_loss = 0.5 * (self.cross_entropy(logits1, labels) + self.cross_entropy(logits2, labels))
        return self.ce_reduce_fn(ce_loss)

    def compute_kl_loss(self, logits1, logits2, masks):
        kl_loss = K.compute_kl_loss(logits1, logits2, masks, self.mask_value)
        return self.kl_reduce_fn(kl_loss)

    def forward(self, logits1, logits2, labels, masks=None):
        """"""
        ce_loss = self.compute_ce_loss(logits1, logits2, labels)
        kl_loss = self.compute_kl_loss(logits1, logits2, masks)
        return ce_loss + self.alpha * kl_loss
