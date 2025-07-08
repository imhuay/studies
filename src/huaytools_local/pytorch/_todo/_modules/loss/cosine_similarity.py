#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Time: 2021-10-13 8:30 下午

Author: huayang

Subject:

"""
import doctest

from torch.nn import functional as F  # noqa

from huaytools_local.pytorch._todo._modules import mean_squared_error_loss


def cosine_similarity_loss(x1, x2, labels):
    """ cosine 相似度损失

    Examples:
        # >>> logits = torch.randn(5, 5).clamp(min=_EPSILON)  # 负对数似然的输入需要值大于 0
        # >>> labels = torch.arange(5)
        # >>> onehot_labels = F.one_hot(labels)
        #
        # # 与官方结果比较
        # >>> my_ret = negative_log_likelihood_loss(logits, onehot_labels)
        # >>> official_ret = F.nll_loss(torch.log(logits + _EPSILON), labels, reduction='none')
        # >>> assert torch.allclose(my_ret, official_ret, atol=1e-5)

    Args:
        x1: [B, N]
        x2: same shape as x1
        labels: [B] or scalar

    Returns:
        [B] vector or scalar
    """
    cosine_scores = F.cosine_similarity(x1, x2, dim=-1)  # [B]
    return mean_squared_error_loss(cosine_scores, labels)  # [B]


def _test():
    """"""
    doctest.testmod()


if __name__ == '__main__':
    """"""
    _test()
