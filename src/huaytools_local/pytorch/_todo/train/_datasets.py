#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Time: 2021-10-14 3:54 下午

Author: huayang

Subject:

"""
import abc
import os
from collections import defaultdict

from typing import *

import numpy as np
from sortedcollections import OrderedSet
from torch.utils.data import DataLoader

from huaytools_local.nlp.bert.tokenization import tokenizer as _tokenizer
from huaytools_local._python.utils import get_logger, get_attr, set_default, set_attr
from huaytools_local._python.custom import BunchDict
from huaytools_local.pytorch._todo.data import ToyDataLoader

__all__ = [
    'Datasets',
    'BertDatasets',
    'NerBertDatasets'
]


class TrainConfig(BunchDict):
    """"""

    def __init__(self, **config_items):
        """"""
        from torch.cuda import is_available
        self.device = 'cuda' if is_available() else 'cpu'

        # data
        self.batch_size: int = 32
        self.val_batch_size: int = 32
        self.test_batch_size: int = 32

        # train
        self.num_train_epochs: int = 3
        self.num_train_steps: int = -1
        self.num_warmup_steps: int = -1
        self.num_gradient_accumulation = 1
        self.learning_rate: float = 5e-5
        self.weight_decay: float = 0.01
        self.no_decay_params = ('bias', 'LayerNorm.weight')
        self.optimizer_name = 'AdamW'
        self.global_step: int = 0

        super(TrainConfig, self).__init__(**config_items)


DEFAULT_ARGS = TrainConfig()

# class DataLoaderDeviceWrapper(DataLoader):
#     """"""
#     device: str
#     data_loader: DataLoader
#
#     def __call__(self, data_loader, device):
#         """"""
#         self.data_loader = data_loader
#         self.device = device
#
#     def __iter__(self):
#         for batch in self.data_loader:
#             yield apply_to(batch, self.device)


logger = get_logger(__name__)


class Datasets(metaclass=abc.ABCMeta):
    """
    Attributes:
        batch_size:
        val_percent:

        features_train: dataset，按行组织数据，遍历时每项为一个样本的 feature (+label)
            通过实现 `_process_row()` 来控制如何从 row 生成 feature
        features_val:
        features_test:

        train_set: data_loader, 按 batch 组织数据，遍历时每项为一个 batch
            可以通过重写 `_build_data_loader()` 调整
        val_set:
        test_set:

        rows_train: rows，原始数据行，仅对行按 ln.split(sep) 切分，其他不做处理（包含不合法数据）
            可以通过重写 `_load_rows()` 调整，比如 NER 的 BIO 标注数据；
            在遍历训练集的过程中，会收集 label_set，默认 row[-1] 为 label，可以通过重写 `_extract_label_from_row()` 来调整；
        rows_val:
        rows_test:

        label_set: {labels}，OrderSet，按出现顺序录入
        label2id_map: {label: id}，可以通过 sort_label 参数控制是否对 label_set 排序后再生成 id
            可以通过重写 `_build_label_map()` 调整
        id2label_map: {id: label}

    """
    batch_size: int
    val_percent: float

    train_set: DataLoader
    val_set: DataLoader
    test_set: DataLoader

    label2id_map: dict
    id2label_map: dict

    def __init__(self,
                 args: Union[Dict, Type],
                 dict_batch=True,
                 sort_label=True,
                 num_examples=3):
        """

        Args:
            args:
            num_examples:
        """
        self.files_train = self._get_file_list(get_attr(args, 'src_train'))
        self.files_val = self._get_file_list(get_attr(args, 'src_val', []))
        self.files_test = self._get_file_list(get_attr(args, 'src_test', []))

        self.device = set_default(args, 'device', DEFAULT_ARGS.device)
        self.batch_size = set_default(args, 'batch_size', DEFAULT_ARGS.batch_size)
        if self.files_val:
            set_attr(args, 'val_percent', -1)
        else:
            set_default(args, 'val_percent', DEFAULT_ARGS.val_percent)
        self.val_percent = get_attr(args, 'val_percent')
        self.shuffle = set_default(args, 'shuffle', DEFAULT_ARGS.shuffle)
        self.random_seed = set_default(args, 'random_seed', DEFAULT_ARGS.random_seed)
        self._sort_label = get_attr(args, 'sort_label', sort_label)
        self._num_examples = get_attr(args, 'num_examples', num_examples)
        self._dict_batch = dict_batch

        self.label_set = OrderedSet()

        # 核心处理逻辑
        # load_rows -> process_row -> post_process
        self._data_process()

    def _build_data_loader(self, dataset):
        return ToyDataLoader(dataset, batch_size=self.batch_size, shuffle=False, device=self.device)

    def _extract_label_from_row(self, row):  # noqa
        """"""
        return row[-1]  # 默认

    def _load_rows(self, files, src_type=None):
        rows = []
        for fp in files:
            with open(fp, encoding='utf8') as f:
                for line in f:
                    row = self._process_line(line, src_type)
                    rows.append(row)

                    if src_type == 'train':
                        label = self._extract_label_from_row(row)
                        self.label_set.add(label)

        return rows

    @abc.abstractmethod
    def _process_line(self, line: str, src_type=None) -> Union[List, Dict]:
        """ 处理原始行数据

        - 如果有 label，默认放在最后一个
        - 没有跟 `_process_row` 放在一起处理，一是为了更灵活的处理 label，而是为了能够兼容 BIO 格式的 NER 数据

        Args:
            line:
            src_type: in {'train', 'val', 'test'}

        Examples:
            # txt 格式
            return line.strip().split('\t')

            # json 格式
            return json.loads(line)
        """

    @abc.abstractmethod
    def _process_row(self, row: Union[List, Dict], src_type=None) -> Union[List, Dict]:
        """ 处理每行数据 src_type in {'train', 'val', 'test'}

        Examples:
            txt1, txt2 = row[0], row[1]
            label = self.label2id_map[row[-1]]
            token_id, token_type_id, mask = tokenizer.encode(txt1, txt2, max_len=self.max_len)

            # list_batch
            return [token_id, token_type_id, mask, label]

            # dict_batch
            return {
                'token_ids': token_id,
                'token_type_ids': token_type_id,
                'masks': mask,
                'labels': label
            }

        Args:
            row:
            src_type: in {'train', 'val', 'test'}
        """

    def _process_rows(self, rows, src_type=None):
        features = []
        for idx, row in enumerate(rows):
            feature = self._process_row(row, src_type)
            features.append(feature)

            if idx < self._num_examples:
                self._show_example(idx, row, feature, src_type)

        return features

    def _show_example(self, idx, row, feature, src_type):  # noqa
        """"""
        logger.info(f"*** Example({src_type}) {idx} ***")
        logger.info(f"\trow: {row}")
        logger.info(f"\tfeature: {feature}")

    def _shuffle_train_dataset(self):
        """"""
        from huaytools_local.nlp.utils import safe_indexing
        rs = np.random.RandomState(self.random_seed)
        idx = rs.permutation(len(self.features_train))
        self.features_train = safe_indexing(self.features_train, idx)

    def _judge_multi_inputs(self, ds):  # noqa
        """"""
        return len(ds) > 0 and len(ds[0]) > 0

    def _data_process(self):
        """"""
        # 一次性加载所有行数据（但先不处理）
        self._load_all_rows()

        # 构建 label_map
        self._build_label_map()

        # 构建数据集
        self._build_all_datasets()

        # 构建 DataLoader
        self._build_all_data_loaders()

    def _build_label_map(self):
        """"""
        if self._sort_label:
            self.label_set = sorted(self.label_set)

        self.label2id_map = {label: i for i, label in enumerate(self.label_set)}
        self.id2label_map = {i: label for label, i in self.label2id_map.items()}

    @staticmethod
    def _flatten_dict_data(dataset: List[Dict]):
        """ [{'a':[..], 'b':[..]}] -> {'a': [..], 'b': [..]} """
        ds_dict = defaultdict(list)
        for row in dataset:
            for k, v in row.items():
                ds_dict[k].append(v)

        return ds_dict

    def _build_all_data_loaders(self):
        if self._dict_batch:
            _ds_train = self._flatten_dict_data(self.features_train)
            _ds_val = self._flatten_dict_data(self.features_val)
            _ds_test = self._flatten_dict_data(self.features_test)
        else:
            _ds_train = zip(*self.features_train) if self._judge_multi_inputs(
                self.features_train) else self.features_train
            _ds_val = zip(*self.features_val) if self._judge_multi_inputs(self.features_val) else self.features_val
            _ds_test = zip(*self.features_test) if self._judge_multi_inputs(self.features_test) else self.features_test
        self.train_set = self._build_data_loader(_ds_train) if _ds_train else None
        self.val_set = self._build_data_loader(_ds_val) if _ds_val else None
        self.test_set = self._build_data_loader(_ds_test) if _ds_test else None

    def _build_all_datasets(self):
        # 构建训练集
        self.features_train = self._process_rows(self.rows_train, src_type='train')
        if self.shuffle:
            self._shuffle_train_dataset()
        # 构建验证集
        if self.val_percent > 0:
            from huaytools_local.nlp.utils import split
            self.features_train, self.features_val = split(self.features_train,
                                                           split_size=self.val_percent,
                                                           shuffled=False)
        else:
            self.features_val = self._process_rows(self.rows_val, src_type='val')
        # 构建测试集
        self.features_test = self._process_rows(self.rows_test, src_type='test')

    def _load_all_rows(self):
        self.rows_train = self._load_rows(self.files_train, src_type='train')
        self.rows_val = self._load_rows(self.files_val, src_type='val')
        self.rows_test = self._load_rows(self.files_test, src_type='test')

    def _get_file_list(self, src) -> Optional[List[str]]:  # noqa
        """ 获取文件列表 """
        if src is None:
            return []
        elif isinstance(src, str):
            if os.path.isdir(src):
                files = [os.path.join(src, fp) for fp in os.listdir(src)]
            else:
                files = [src]
        elif isinstance(src, Iterable):
            files = list(src)
        else:
            raise ValueError(f'Error src={src}.')

        return files


class BertDatasets(Datasets):
    """"""

    def __init__(self, args: dict, tokenizer=_tokenizer, **kwargs):
        """
        Examples:
            # 示例1：单文件，根据比例划分训练集和测试集（默认返回 dict_batch 格式）
            >>> fp = os.path.join(os.path.dirname(__file__), '_data/one_train.txt')
            >>> _args = TrainConfig(src_train=fp, batch_size=2, val_percent=0.2, max_len=16, shuffle=False)
            >>> dl = BertDatasets(_args, num_examples=0)
            >>> len(dl.features_train)
            8
            >>> len(dl.features_val)
            2
            >>> b = next(iter(dl.train_set))  # 训练集第一个 batch
            >>> list(b.keys())  # [token_ids, token_type_ids, masks, labels]
            ['token_ids', 'token_type_ids', 'masks', 'labels']
            >>> list(b['token_ids'].shape)  # token_ids.shape
            [2, 16]
            >>> b['token_ids'][0].numpy().tolist()[:5]  # [CLS, 总，之，就，是]
            [101, 2600, 722, 2218, 3221]

            # 多文件
            >>> fp_train = os.path.join(os.path.dirname(__file__), '_data/one_train.txt')
            >>> fp_val = os.path.join(os.path.dirname(__file__), '_data/one_val.txt')
            >>> fp_test = os.path.join(os.path.dirname(__file__), '_data/one_test.txt')
            >>> _args = TrainConfig(src_train=fp_train, src_val=fp_val, src_test=fp_test,
            ...                     batch_size=3, max_len=16, shuffle=False)
            >>> dl = BertDatasets(_args, dict_batch=False, num_examples=0)
            >>> len(dl.features_train), len(dl.features_val), len(dl.features_test)
            (10, 3, 3)
            >>> b = next(iter(dl.val_set))  # 验证集第一个 batch: [token_ids, token_type_ids, masks, labels]
            >>> list(b[0].shape)  # token_ids.shape: [batch_size, max_len]
            [3, 16]
            >>> b[0][0].numpy().tolist()[:5]  # [CLS，效，果，好，一]
            [101, 3126, 3362, 1962, 671]
            >>> b = next(iter(dl.test_set))  # 测试集第一个 batch: [token_ids, token_type_ids, masks]
            >>> b[0][0].numpy().tolist()[:5]  # [CLS，妆，容，好，漂]
            [101, 1966, 2159, 1962, 4023]

        """
        self.max_len = set_default(args, 'max_len', 128)
        self._task_type = set_default(args, 'task_type', 'single')
        self._tokenizer = tokenizer
        super(BertDatasets, self).__init__(args, **kwargs)

    def _process_line(self, line, src_type=None):
        """"""
        return line.strip().split('\t')

    def _process_row(self, row, src_type=None):
        txt1 = row[0]
        txt2 = row[1] if self._task_type != 'single' else None
        _, token_id, token_type_id, mask = self._tokenizer.encode(txt1, txt2,
                                                                  max_len=self.max_len,
                                                                  return_token_type_ids=True,
                                                                  return_token_masks=True)
        if src_type != 'test':
            label = self.label2id_map[row[-1]]
            if self._dict_batch:
                return {
                    'token_ids': token_id,
                    'token_type_ids': token_type_id,
                    'masks': mask,
                    'labels': label
                }  # key 的命名参考模型的 forward 参数
            else:
                return [token_id, token_type_id, mask, label]

        else:
            if self._dict_batch:
                return {
                    'token_ids': token_id,
                    'token_type_ids': token_type_id,
                    'masks': mask
                }
            else:
                return [token_id, token_type_id, mask]


class NerBertDatasets(BertDatasets):
    """"""

    def __init__(self, args: dict, outer_label='O', **kwargs):
        """
        Examples:
            >>> fp = os.path.join(os.path.dirname(__file__), '_data/ner_train.txt')
            >>> _args = TrainConfig(src_train=fp, batch_size=2, val_percent=0.1, max_len=16, shuffle=False)
            >>> dl = NerBertDatasets(_args, num_examples=0)
            >>> len(dl.features_val) # 共 3 句，划分 0.1 的比例作为验证集（向上取整）
            1
            >>> b = next(iter(dl.train_set))  # 训练集第一个 batch
            >>> len(b)  # [token_ids, token_type_ids, masks, labels]
            4
            >>> b[0][0].numpy().tolist()[:5]  # [CLS，美，国，的，华]
            [101, 5401, 1744, 4638, 1290]
            >>> b[0][1].numpy().tolist()[-5:]  # [北，京，SEP，0，0]
            [1266, 776, 102, 0, 0]

        """
        self._outer_label = outer_label
        set_default(args, 'max_len', 32)
        set_default(args, 'sort_label', False)
        super(NerBertDatasets, self).__init__(args, dict_batch=False, **kwargs)

    def _load_rows(self, files, src_type=False):
        """"""
        if src_type != 'test':
            from huaytools_local.nlp.data_helper.sequence_labeling import data_process
            rows, label_map = data_process(files, sep='\t', outer_label=self._outer_label)
            if src_type == 'train':
                self.label_set = set(label_map.keys())
            return rows
        else:
            return super(NerBertDatasets, self)._load_rows(files)

    def _process_row(self, row, src_type=None, n_special_tokens=2):
        """
        row = [[tokens], [labels]]
        """
        max_len = self.max_len
        outer_label_id = self.label2id_map[self._outer_label]

        if src_type != 'test':
            tokens, label = row
            txt = ' '.join(tokens)

            # padding labels to max_len, PS: [CLS] & [SEP]
            if len(tokens) > max_len - n_special_tokens:
                label_id = [outer_label_id] + label[: max_len - n_special_tokens] + [outer_label_id]
            else:
                label_id = [outer_label_id] + label + [outer_label_id] \
                           + [outer_label_id] * (max_len - n_special_tokens - len(label))
            # label_id = [self.label2id_map[x] for x in label]
            _, token_id, token_type_id, mask = self._tokenizer.encode(txt, max_len=max_len,
                                                                      return_token_type_ids=True,
                                                                      return_token_masks=True)

            return [token_id, token_type_id, mask, label_id]
        else:
            txt = ' '.join(list(row[0]))
            _, token_id, token_type_id, mask = self._tokenizer.encode(txt, max_len=max_len,
                                                                      return_token_masks=True)
            return [token_id, token_type_id, mask]


def _test():
    """"""

    # doctest.testmod()

    def _test_bert_data_loader_helper():
        """"""
        log_n = '测试 1：单句-单文件（默认返回 dict_batch）'
        logger.info(f'-- {log_n} Start --')
        fp = os.path.join(os.path.dirname(__file__), '_data/one_train.txt')
        args = TrainConfig(src_train=fp, batch_size=2, val_percent=0.2, max_len=16, shuffle=False)
        dl = BertDatasets(args, num_examples=2)
        assert len(dl.features_train) + len(dl.features_val) == 10
        assert len(dl.features_val) == 2  # 共 10 句，划分 0.2 的比例作为验证集
        # 训练集第一个 batch
        b = next(iter(dl.train_set))
        assert len(b) == 4  # token_ids, token_type_ids, masks, labels
        assert list(b['token_ids'].shape) == [2, 16]  # token_ids.shape = [batch_size, max_len]
        assert b['token_ids'][0].numpy().tolist()[:5] == [101, 2600, 722, 2218, 3221]  # [CLS, 总，之，就，是]
        logger.info(f'-- {log_n} End --\n')

        log_n = '测试 2：单句-多文件（返回 list_batch）'
        logger.info(f'-- {log_n} Start --')
        fp_train = os.path.join(os.path.dirname(__file__), '_data/one_train.txt')
        fp_val = os.path.join(os.path.dirname(__file__), '_data/one_val.txt')
        fp_test = os.path.join(os.path.dirname(__file__), '_data/one_test.txt')
        args = TrainConfig(src_train=fp_train, src_val=fp_val, src_test=fp_test,
                           batch_size=3, max_len=16, shuffle=False)
        dl = BertDatasets(args, dict_batch=False, num_examples=1)
        assert len(dl.features_train) == 10
        assert len(dl.features_val) == 3
        assert len(dl.features_test) == 3
        # 验证集第一个 batch
        b = next(iter(dl.val_set))
        assert len(b) == 4  # token_ids, token_type_ids, masks, labels
        assert list(b[0].shape) == [3, 16]  # token_ids.shape = [batch_size, max_len]
        assert b[0][0].numpy().tolist()[:5] == [101, 3126, 3362, 1962, 671]  # [CLS，效，果，好，一]
        # 测试集第一个 batch
        b = next(iter(dl.test_set))
        assert len(b) == 3  # token_ids, token_type_ids, masks
        assert list(b[0].shape) == [3, 16]  # token_ids.shape = [batch_size, max_len]
        assert b[0][0].numpy().tolist()[:5] == [101, 1966, 2159, 1962, 4023]  # [CLS，妆，容，好，漂]
        logger.info(f'-- {log_n} End --\n')

        log_n = '测试 3：双句-单文件'
        logger.info(f'-- {log_n} Start --')
        fp = os.path.join(os.path.dirname(__file__), '_data/two_train.txt')
        args = TrainConfig(src_train=fp, task_type='pair', batch_size=2, val_percent=0.3, max_len=16,
                           shuffle=False)
        dl = BertDatasets(args, num_examples=1)
        assert len(dl.features_train) + len(dl.features_val) == 6
        assert len(dl.features_val) == 2  # 共 6 句，划分 0.3 的比例作为验证集（向上取整）
        # 训练集第一个 batch
        b = next(iter(dl.train_set))
        assert len(b) == 4  # token_ids, token_type_ids, masks, labels
        assert list(b['token_ids'].shape) == [2, 16]  # token_ids.shape = [batch_size, max_len]
        assert b['token_ids'][0].numpy().tolist()[:5] == [101, 2600, 722, 2218, 3221]  # [CLS，总，之，就，是]
        assert b['token_ids'][0].numpy().tolist()[11:16] == [1922, 2345, 749, 1416, 102]  # [太，差，了，吧，SEP]
        logger.info(f'-- {log_n} End --\n')

        log_n = '测试 4：NER-单文件'
        logger.info(f'-- {log_n} Start --')
        fp = os.path.join(os.path.dirname(__file__), '_data/ner_train.txt')
        args = TrainConfig(src_train=fp, batch_size=2, val_percent=0.1, max_len=16, shuffle=False)
        dl = NerBertDatasets(args, num_examples=2)
        assert len(dl.features_train) + len(dl.features_val) == 3
        assert len(dl.features_val) == 1  # 共 3 句，划分 0.1 的比例作为验证集（向上取整）
        # 训练集第一个 batch
        b = next(iter(dl.train_set))
        assert len(b) == 4  # token_ids, token_type_ids, masks, labels
        assert list(b[0].shape) == [2, 16]  # token_ids.shape = [batch_size, max_len]
        assert b[0][0].numpy().tolist()[:5] == [101, 5401, 1744, 4638, 1290]  # [CLS，美，国，的，华]
        assert b[0][1].numpy().tolist()[-5:] == [1266, 776, 102, 0, 0]  # [北，京，SEP，0，0]
        logger.info(f'-- {log_n} End --\n')

    # _test_bert_data_loader_helper()


if __name__ == '__main__':
    """"""
    _test()
