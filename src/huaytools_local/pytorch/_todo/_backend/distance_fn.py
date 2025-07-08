#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Time:
    2021-08-09 5:09 下午

Author:
    huayang

Subject:

"""

import torch
import torch.nn.functional as F  # noqa

from huaytools_local.pytorch._todo._backend import l2_normalize


# def dense_wrapper(distance_fn):
#     """"""
#     return lambda x1, x2: distance_fn(x1.unsqueeze(1), x2.unsqueeze(1), dim=-1)


def euclidean_distance(x1, x2):
    """ 欧氏距离
        same as `F.pairwise_distance(p=2)`

    Args:
        x1: [B, N] or [N]
        x2: same shape as x1

    Returns:
        [B] vector or scalar
    """
    return (x1 - x2).pow(2).sum(-1).pow(0.5)


def euclidean_distance_nosqrt(x1, x2):
    """ 欧氏距离，不对结果开方

    Args:
        x1: [B, N] or [N]
        x2: same shape as x1

    Returns:
        [B] vector or scalar
    """
    return (x1 - x2).pow(2).sum(-1)  # .pow(0.5)


def cosine_distance(x1, x2, dim=-1):
    """ cosine 距离
        等价于 `1 - F.cosine_similarity`

    Args:
        x1: [B, N] or [N]
        x2: same shape as x1
        dim: 默认 -1

    Returns:
        [B] vector or scalar

    Examples:
        x1 = torch.as_tensor([1, 2, 3]).to(torch.float)
        x2 = torch.as_tensor([9, 8, 7]).to(torch.float)
        print(cosine_distance(x1, x2).numpy())
        # 0.11734104
        print(1 - F.cosine_similarity(x1, x2, dim=0).numpy())
        # 0.1173410415649414

        x1 = torch.as_tensor([[1, 2, 3], [4, 5, 6], [7, 8, 9]]).to(torch.float)
        x2 = torch.as_tensor([[9, 8, 7], [6, 5, 4], [3, 2, 1]]).to(torch.float)
        print(cosine_distance(x1, x2).numpy())
        # [0.11734104 0.05194807 0.1173411 ]
        print(1 - F.cosine_similarity(x1, x2, dim=1).numpy())
        # [0.11734104 0.05194807 0.11734104]
    """
    x1_normalized = l2_normalize(x1, dim=dim)
    x2_normalized = l2_normalize(x2, dim=dim)
    return 1 - (x1_normalized * x2_normalized).sum(dim)


def _test():
    """"""

    def _test_o():
        """"""
        x1 = torch.as_tensor([1, 2, 3]).to(torch.float)
        x2 = torch.as_tensor([9, 8, 7]).to(torch.float)
        print(cosine_distance(x1, x2).numpy())
        # 0.11734104
        print(1 - F.cosine_similarity(x1, x2, dim=0).numpy())
        # 0.1173410415649414

        x1 = torch.as_tensor([[1, 2, 3], [4, 5, 6], [7, 8, 9]]).to(torch.float)
        x2 = torch.as_tensor([[9, 8, 7], [6, 5, 4], [3, 2, 1]]).to(torch.float)
        print(cosine_distance(x1, x2).numpy())
        # [0.11734104 0.05194807 0.1173411 ]
        print(1 - F.cosine_similarity(x1, x2, dim=1).numpy())
        # [0.11734104 0.05194807 0.11734104]

    _test_o()

    def _test_cosine_distance():
        """"""
        x1 = torch.randn(3, 4, 5, 6, 7)
        x2 = torch.randn(3, 4, 5, 6, 7)
        assert torch.allclose(cosine_distance(x1, x2, dim=0), 1 - F.cosine_similarity(x1, x2, dim=0), atol=1e-5)
        assert torch.allclose(cosine_distance(x1, x2, dim=1), 1 - F.cosine_similarity(x1, x2, dim=1), atol=1e-5)
        assert torch.allclose(cosine_distance(x1, x2, dim=2), 1 - F.cosine_similarity(x1, x2, dim=2), atol=1e-5)
        assert torch.allclose(cosine_distance(x1, x2, dim=3), 1 - F.cosine_similarity(x1, x2, dim=3), atol=1e-5)
        assert torch.allclose(cosine_distance(x1, x2, dim=4), 1 - F.cosine_similarity(x1, x2, dim=4), atol=1e-5)

        from huaytools_local.pytorch.utils import cosine_similarity_dense
        x1 = torch.randn(5, 6)
        x2 = torch.randn(5, 6)
        assert torch.allclose(
            cosine_similarity_dense(x1, x2),  # [5, 5]
            F.cosine_similarity(x1.unsqueeze(1), x2.unsqueeze(0), dim=-1),  # [5, 5]
            atol=1e-5
        )

    _test_cosine_distance()


if __name__ == '__main__':
    """"""
    _test()
