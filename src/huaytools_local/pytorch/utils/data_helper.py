#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Time: 2021-11-19 11:07 上午

Author: huayang

Subject:

"""
import os
import time

from typing import *
from itertools import islice
from collections import defaultdict

import torch
from torch import Tensor
from torch.utils.data import DataLoader, TensorDataset
from torch.utils.data import Dataset, IterableDataset
from torch.utils.data.dataset import T_co  # noqa

from huaytools_local.utils import get_logger, IterUtils


class DictTensorDataset(Dataset[Dict[str, Tensor]]):  # python=3.6中使用，需删掉 [Dict[str, Tensor]]
    """@Pytorch Utils
    字典格式的 Dataset

    Examples:
        >>> x = y = torch.as_tensor([1,2,3,4,5])
        >>> _ds = DictTensorDataset(x=x, y=y)
        >>> len(_ds)
        5
        >>> dl = DataLoader(_ds, batch_size=3)
        >>> for batch in dl: print(batch)
        {'x': tensor([1, 2, 3]), 'y': tensor([1, 2, 3])}
        {'x': tensor([4, 5]), 'y': tensor([4, 5])}
        >>> len(dl)
        2

    References:
        - torch.utils.data.TensorDataset
        - huggingface/datasets.arrow_dataset.Dataset
    """

    tensors_dict: Dict[str, Tensor]

    def __init__(self, **tensors_dict: Tensor) -> None:
        """
        Args:
            **tensors_dict:
        """
        from huaytools_local.utils import remove_duplicates
        assert len(remove_duplicates([tensor.shape[0] for tensor in tensors_dict.values()])) == 1, \
            "Size mismatch between tensors"
        self.tensors_dict = tensors_dict

    def __getitem__(self, index) -> Dict[str, Tensor]:
        """"""
        return {name: tensor[index] for name, tensor in self.tensors_dict.items()}

    def __len__(self):
        return IterUtils.first(self.tensors_dict.values()).shape[0]


class SimpleDataLoader(DataLoader):
    """@Pytorch Utils
    简化创建 DataLoader 的过程

    Examples:
        # single input
        >>> x = [1,2,3,4,5]
        >>> dl = SimpleDataLoader(x, batch_size=3, single_input=True, shuffle=False)
        >>> for batch in dl:
        ...     print(type(batch).__name__, batch)
        list [tensor([1, 2, 3])]
        list [tensor([4, 5])]

        # multi inputs
        >>> x = y = [1,2,3,4,5]
        >>> dl = SimpleDataLoader([x, y], batch_size=3, shuffle=False, device='cpu')
        >>> for batch in dl:
        ...     print(type(batch).__name__, batch)
        list [tensor([1, 2, 3]), tensor([1, 2, 3])]
        list [tensor([4, 5]), tensor([4, 5])]

        # multi inputs (dict)
        >>> x = y = [1,2,3,4,5]
        >>> dl = SimpleDataLoader({'x': x, 'y': y}, batch_size=3, shuffle=False, device='cpu')
        >>> for batch in dl:
        ...     print(type(batch).__name__, batch)
        dict {'x': tensor([1, 2, 3]), 'y': tensor([1, 2, 3])}
        dict {'x': tensor([4, 5]), 'y': tensor([4, 5])}

        # multi inputs (row2col)
        >>> xy = [[1,1],[2,2],[3,3],[4,4],[5,5]]
        >>> dl = SimpleDataLoader(xy, batch_size=3, row2col=True, shuffle=False, device='cpu')
        >>> for batch in dl:
        ...     print(type(batch).__name__, batch)
        list [tensor([1, 2, 3]), tensor([1, 2, 3])]
        list [tensor([4, 5]), tensor([4, 5])]

        # multi inputs (dict, row2col)
        >>> xy = [{'x':1,'y':1},{'x':2,'y':2},{'x':3,'y':3},{'x':4,'y':4},{'x':5,'y':5}]
        >>> dl = SimpleDataLoader(xy, batch_size=3, row2col=True, shuffle=False, device='cpu')
        >>> for batch in dl:
        ...     print(type(batch).__name__, batch)
        dict {'x': tensor([1, 2, 3]), 'y': tensor([1, 2, 3])}
        dict {'x': tensor([4, 5]), 'y': tensor([4, 5])}

    Notes:
        V1: 当数据较大时，直接把所有数据 to('cuda') 会爆内存，所以删除了 default_device
            如果数据量比较小，也可以设置 device='cuda' 提前把数据移动到 GPU
        V2: 重写了 __iter__()，在产生 batch 时才移动 tensor，因此还原了 default_device
    """

    def __init__(self, dataset: Iterable, batch_size,
                 single_input=False, row2col=False,
                 shuffle=True, device=None, **kwargs):
        """

        Args:
            dataset:
            batch_size:
            single_input: if is single input, default False
            row2col: work when `single_input` is False, default False
            shuffle: default True
            device: default None
            **kwargs:
        """
        # self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.device = device

        if single_input:
            dataset = TensorDataset(torch.as_tensor(dataset))
        else:  # multi inputs
            if row2col:
                if isinstance(next(iter(dataset)), Dict):
                    col_dataset = defaultdict(list)
                    for row in dataset:
                        for k, v in row.items():
                            col_dataset[k].append(v)
                    dataset = col_dataset
                else:
                    dataset = zip(*dataset)

            if isinstance(dataset, Dict):
                dataset = {name: torch.as_tensor(tensor) for name, tensor in dataset.items()}
                dataset = DictTensorDataset(**dataset)
            else:
                dataset = [torch.as_tensor(tensor) for tensor in list(dataset)]
                dataset = TensorDataset(*dataset)

        # 这样写会导致无法实用其他类型的 sampler
        # if shuffle:
        #     sampler = RandomSampler(dataset, replacement=repeat_sampling)
        # else:
        #     sampler = SequentialSampler(dataset)
        super().__init__(dataset, batch_size=batch_size, shuffle=shuffle, **kwargs)

    def __iter__(self):
        """
        References:
            from hanlp.common.dataset import DeviceDataLoader
        """
        for batch in super().__iter__():
            if self.device is not None:
                if isinstance(batch, Dict):
                    batch = {name: tensor.to(self.device) for name, tensor in batch.items()}
                else:
                    batch = [tensor.to(self.device) for tensor in batch]

            yield batch


def _identity(x):
    return x


class SequenceDataset(Dataset):
    """"""

    def __init__(self,
                 data: Union[Sequence, Dict[str, Sequence]],
                 map_fn: Callable = _identity):
        """
        Args:
            data:
            map_fn:

        Examples:
            >>> d = ['1', '2', '3']
            >>> ds = SequenceDataset(d)
            >>> ds[1]
            '2'
            >>> ds = SequenceDataset(d, map_fn=lambda x: float(x))
            >>> for it in islice(ds, 2):
            ...     print(it)
            1.0
            2.0

            # dict data
            >>> d = {'a': range(10), 'b': range(10, 20)}
            >>> ds = SequenceDataset(d)
            >>> for it in islice(ds, 2):
            ...     print(it)
            {'a': 0, 'b': 10}
            {'a': 1, 'b': 11}

            # list dict (same as above)
            >>> d = [{'a': a, 'b': b} for a, b in zip(range(10), range(10, 20))]  # noqa
            >>> ds = SequenceDataset(d)
            >>> for it in islice(ds, 2):
            ...     print(it)
            {'a': 0, 'b': 10}
            {'a': 1, 'b': 11}
        """
        self.data = data
        self.map_fn = map_fn

        if isinstance(self.data, dict):
            assert len(set([len(v) for v in self.data.values()])) == 1, \
                f'Data length is not equal with { {k: len(v) for k, v in self.data.items()} }.'
            self._getitem = self._getitem_dict
        else:
            self._getitem = self._getitem_default

    def __getitem__(self, index) -> T_co:
        return self._getitem(index)

    def __len__(self):
        if isinstance(self.data, dict):
            return len(IterUtils.first(self.data.values()))
        else:
            return len(self.data)

    def _getitem_dict(self, index):
        return self.map_fn({n: d[index] for n, d in self.data.items()})

    def _getitem_default(self, index):
        return self.map_fn(self.data[index])


class IterDataset(IterableDataset):
    """"""

    def __init__(self, data: Union[Iterable, Dict[str, Iterable]], map_fn: Callable = _identity):
        """
        Args:
            data:
            map_fn:

        Examples:
            >>> d = iter(range(100))
            >>> ds = IterDataset(d, map_fn=lambda x: x + 1.)
            >>> for it in islice(ds, 2):
            ...     print(it)
            1.0
            2.0

            # dict data
            >>> d = {'a': iter(range(10)), 'b': iter(range(10, 200))}
            >>> ds = IterDataset(d, map_fn=lambda x: {'a': x['a'] + 1., 'b': x['b'] * 2.})
            >>> for it in islice(ds, 2, 4):
            ...     print(it)
            {'a': 3.0, 'b': 24.0}
            {'a': 4.0, 'b': 26.0}

        """
        self.data = data
        self.map_fn = map_fn

        if isinstance(self.data, dict):
            self._iter = self._iter_dict
        else:
            self._iter = self._iter_default

    def __getitem__(self, index) -> T_co:  # not be called when using `IterableDataset`
        return NotImplemented

    def __iter__(self) -> Iterator[T_co]:
        yield from self._iter()

    def _iter_dict(self):
        # keys = self.data.keys()
        # for values in zip(*map(self.data.get, keys)):
        #     yield self.map_fn(dict(zip(keys, values)))
        ks, vs = zip(*self.data.items())
        for v in zip(*vs):
            yield self.map_fn(dict(zip(ks, v)))

    def _iter_default(self):
        for it in self.data:
            yield self.map_fn(it)


DataContainer = Union[Sequence, Iterable, Dict[str, Union[Sequence, Iterable]]]


def get_dataset(data: DataContainer,
                map_fn: Callable = None) -> Dataset:  # noqa
    """"""

    def _is_sequence():
        f1 = isinstance(data, Sequence)
        f2 = isinstance(data, dict) and all(isinstance(v, Sequence) for v in data.values())
        return f1 or f2

    if map_fn is None:
        map_fn = _identity

    if _is_sequence():
        return SequenceDataset(data, map_fn)
    else:
        return IterDataset(data, map_fn)


class ToyDataLoader(DataLoader):
    """"""
    logger = get_logger()

    def __init__(self, dataset: Union[Dataset, DataContainer],
                 batch_size: int = 8,
                 map_fn: Callable = None,  # convert each sample
                 collate_fn: Callable = None,  # convert batch samples
                 shuffle: bool = True,
                 device: str = None,
                 **kwargs):
        """
        Args:
            dataset:
            batch_size:
            map_fn:
            collate_fn:
            shuffle:
            device:
            **kwargs: kwargs of DataLoader

        Examples:
            # sequence
            >>> d = ['1', '2', '3']
            >>> ds = SequenceDataset(d, map_fn=lambda x: int(x))
            >>> dl = ToyDataLoader(ds, batch_size=2, shuffle=False)
            >>> next(iter(dl))
            tensor([1, 2])
            >>> dl = ToyDataLoader(d, batch_size=2, shuffle=False,
            ...                    map_fn=lambda x: torch.as_tensor(int(x)).to(torch.float))
            >>> for it in islice(dl, 2):
            ...     print(it)
            tensor([1., 2.])
            tensor([3.])

            # sequence of dict
            >>> d = [{'a': a, 'b': b} for a, b in zip(range(10), range(10, 20))]  # noqa
            >>> dl = ToyDataLoader(d, batch_size=3, shuffle=False,
            ...                    map_fn=lambda x: {k: v + 1 for k, v in x.items()})  # noqa
            >>> for it in islice(dl, 2):
            ...     print(it)
            {'a': tensor([1, 2, 3]), 'b': tensor([11, 12, 13])}
            {'a': tensor([4, 5, 6]), 'b': tensor([14, 15, 16])}

            # dict (same as above)
            >>> d = {'a': range(10), 'b': range(10, 20)}
            >>> dl = ToyDataLoader(d, batch_size=3, shuffle=False,
            ...                    map_fn=lambda x: {k: v + 1 for k, v in x.items()})  # noqa
            >>> for it in islice(dl, 2):
            ...     print(it)
            {'a': tensor([1, 2, 3]), 'b': tensor([11, 12, 13])}
            {'a': tensor([4, 5, 6]), 'b': tensor([14, 15, 16])}

            # iter
            >>> d = iter(range(100))
            >>> dl = ToyDataLoader(d, batch_size=4, shuffle=False)
            >>> for it in islice(dl, 2):
            ...     print(it)
            tensor([0, 1, 2, 3])
            tensor([4, 5, 6, 7])

            # iter of dict
            >>> d = {'a': (i for i in range(10)), 'b': (i for i in range(10, 200))}  # noqa
            >>> dl = ToyDataLoader(d, batch_size=3, shuffle=False)
            >>> for dl in islice(dl, 2):
            ...     print(dl)
            {'a': tensor([0, 1, 2]), 'b': tensor([10, 11, 12])}
            {'a': tensor([3, 4, 5]), 'b': tensor([13, 14, 15])}
        """
        self.device = device
        if not isinstance(dataset, Dataset):
            dataset = get_dataset(dataset, map_fn=map_fn)

        super().__init__(dataset, batch_size=batch_size, collate_fn=collate_fn, shuffle=shuffle,
                         **kwargs)

    def __iter__(self):
        """
        References:
            hanlp.common.dataset.DeviceDataLoader
        """
        for batch in super().__iter__():
            if self.device is not None:
                if isinstance(batch, Dict):
                    batch = {name: tensor.to(self.device) for name, tensor in batch.items()}
                else:
                    batch = [tensor.to(self.device) for tensor in batch]

            yield batch


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

    # def _test_SequenceDataset(self):  # noqa
    #     """"""
    #     data = ['1', '2', '3']
    #     ds = SequenceDataset(data)
    #     for i in ds:
    #         print(i)
    #
    #     ds = SequenceDataset(data, map_fn=lambda x: float(x))
    #     for i in ds:
    #         print(i)

    # def _test_IterDataset(self):  # noqa
    #     """"""
    #     data = {'a': (i for i in range(10)), 'b': (i for i in range(10, 20))}
    #     ds = IterDataset(data, map_fn=lambda x: {k: v + 1 for k, v in x.items()})
    #     for i in ds:
    #         print(i)

    # def _test_ToyDataLoader(self):  # noqa
    #     """"""
    #     data = ['1', '2', '3']
    #
    #     # data -> dataset -> dataloader
    #     ds = SequenceDataset(data, map_fn=lambda x: float(x))
    #     dl = ToyDataLoader(ds, batch_size=2, shuffle=False)
    #     for it in dl:
    #         print(it)
    #
    #     print()
    #     # data -> dataloader
    #     dl = ToyDataLoader(data, batch_size=2, shuffle=False,
    #                        map_fn=lambda x: int(x),
    #                        collate_fn=lambda b: torch.as_tensor(b).to(torch.float))
    #     for it in dl:
    #         print(it)
    #
    #     print()
    #     # dict -> dataloader
    #     # 注意：dict 的 value 最好已经处理成 tensor 或 float，
    #     # 如果要自己写 collate_fn 的话，需要注意传入的 batch 是 list[dict[str, sample]], 而不是 dict[str, samples]，
    #     # 示例：[{'f1': 1, 'f2': 2}, ...]，而不是 {'f1': [1,...], 'f2': [2,...]}
    #     data = {'feature1': ['1', '2', '3', '4', '5'], 'feature2': [4, 5, 6, 7, 8]}
    #     dl = ToyDataLoader(data, batch_size=3, shuffle=False,
    #                        map_fn=lambda x: {'f1': int(x['feature1']) + 1., 'f2': x['feature2'] * 2.})
    #     for it in dl:
    #         print(it)
    #
    #     print()
    #     # dict iter -> dataloader
    #     data = {'a': (i for i in range(10)), 'b': (i for i in range(10, 200))}
    #     dl = ToyDataLoader(data, batch_size=3, shuffle=False, map_fn=lambda x: {k: v + 1. for k, v in x.items()})
    #     for it in dl:
    #         print(it)


if __name__ == '__main__':
    """"""
    __Test()
