#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Time: 2022-06-05 12:48 上午

Author: huayang

Subject:

"""
import os  # noqa
import doctest  # noqa

# from collections import defaultdict
# from itertools import islice
# from pathlib import Path
# from typing import *

from dataclasses import dataclass

# from tqdm import tqdm


@dataclass()
class BestThreshold:
    best_accuracy: float
    best_accuracy_threshold: float
    best_f1: float
    best_f1_threshold: float
    best_precision: float
    best_recall: float


def find_best_threshold_binary(scores, labels, greater_better: bool = True, epsilon=1e-12, n_digits=5) -> BestThreshold:
    """@NLP Utils
    搜索最佳阈值（二分类）

    Examples:
        >>> _scores = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
        >>> _labels = [0, 0, 1, 0, 1, 1, 1, 1]
        >>> o = find_best_threshold_binary(_scores, _labels)
        >>> o.best_accuracy, o.best_accuracy_threshold
        (0.875, 0.45)
        >>> o.best_f1, o.best_f1_threshold, o.best_precision, o.best_recall
        (0.90909, 0.25, 0.83333, 1.0)

        >>> _scores = [0.1, 0.2, 0.3]
        >>> _labels = [0, 0, 0]
        >>> # Labels are all negative, the threshold should be meaningless.
        >>> o = find_best_threshold_binary(_scores, _labels)
        >>> o.best_accuracy_threshold
        inf

        >>> _scores = [0.1, 0.2, 0.3]
        >>> _labels = [1, 1, 1]
        >>> # Labels are all positive, the threshold should be meaningless.
        >>> o = find_best_threshold_binary(_scores, _labels)
        >>> o.best_accuracy_threshold
        -inf

        >>> _scores = [0.1, 0.2, 0.3]
        >>> _labels = [1, 1, 1]
        >>> o = find_best_threshold_binary(_scores, _labels, greater_better=False)
        >>> o.best_accuracy_threshold
        inf

    Args:
        scores: float array-like
        labels: 0/1 array-like
        greater_better: Default True, it means that 1 if greater than threshold, 0 otherwise;
            When False, it means that 0 if greater than threshold, 1 otherwise.
        epsilon:
        n_digits: round(f, n_digits)

    """
    from huaytools_local.utils import get_logger
    logger = get_logger()

    assert len(scores) == len(labels)
    rows = sorted(zip(scores, labels), key=lambda x: x[0], reverse=greater_better)

    n_count = 0
    n_correct = 0
    n_pos_total = sum(labels)
    n_neg_remain = len(labels) - n_pos_total

    if n_pos_total == 0:  # 标签全是 0
        logger.warning(f'Labels are all negative, the threshold should be meaningless.')
        threshold = float('inf') if greater_better else float('-inf')
        return BestThreshold(1., threshold, 1., threshold, 1., 1.)

    if n_neg_remain == 0:  # 标签全是 1
        logger.warning(f'Labels are all positive, the threshold should be meaningless.')
        threshold = float('-inf') if greater_better else float('inf')
        return BestThreshold(1., threshold, 1., threshold, 1., 1.)

    best_accuracy = 0
    best_accuracy_threshold = -1
    best_f1 = 0
    best_precision = 0
    best_recall = 0
    best_f1_threshold = -1

    for i in range(len(rows) - 1):
        score, label = rows[i]
        n_count += 1

        if label == 1:
            n_correct += 1
        else:
            n_neg_remain -= 1

        acc = (n_correct + n_neg_remain) / len(labels)
        if acc > best_accuracy:
            best_accuracy = acc
            best_accuracy_threshold = (rows[i][0] + rows[i + 1][0]) / 2

        precision = n_correct / (n_count + epsilon)
        recall = n_correct / (n_pos_total + epsilon)
        f1 = 2 * precision * recall / (precision + recall + epsilon)
        if f1 > best_f1:
            best_precision = precision
            best_recall = recall
            best_f1 = f1
            best_f1_threshold = (rows[i][0] + rows[i + 1][0]) / 2

    tmp = [best_accuracy, best_accuracy_threshold, best_f1, best_f1_threshold, best_precision, best_recall]
    tmp = [round(it, n_digits) for it in tmp]
    return BestThreshold(*tmp)


def find_best_threshold_multiple():
    """"""
    # TODO
    raise NotImplementedError


if __name__ == '__main__':
    """"""
    doctest.testmod()
