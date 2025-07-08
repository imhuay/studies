#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Time: 2021-11-03 3:58 下午

Author: huayang

Subject:

"""
import re
import os
import doctest

from typing import Union, List, Dict

import torch

from huaytools_local._python.utils import get_env, set_env, get_logger
from huaytools_local._python.config_loader import load_config_file
from huaytools_local.nlp.bert.tokenization import BertTokenizer as _BertTokenizer
from huaytools_local.pytorch.utils import load_state_dict_tf, load_state_dict_pt

logger = get_logger()

WEIGHTS_MAP_GOOGLE = {
    # embeddings
    'embeddings.word_embeddings.weight': 'bert/embeddings/word_embeddings',
    'embeddings.position_embeddings.weight': 'bert/embeddings/position_embeddings',
    'embeddings.token_type_embeddings.weight': 'bert/embeddings/token_type_embeddings',
    'embeddings.LayerNorm.weight': 'bert/embeddings/LayerNorm/gamma',
    'embeddings.LayerNorm.bias': 'bert/embeddings/LayerNorm/beta',

    # transformers
    'transformers.{idx}.attention.q_dense.weight': 'bert/encoder/layer_{idx}/attention/self/query/kernel',
    'transformers.{idx}.attention.q_dense.bias': 'bert/encoder/layer_{idx}/attention/self/query/bias',
    'transformers.{idx}.attention.k_dense.weight': 'bert/encoder/layer_{idx}/attention/self/key/kernel',
    'transformers.{idx}.attention.k_dense.bias': 'bert/encoder/layer_{idx}/attention/self/key/bias',
    'transformers.{idx}.attention.v_dense.weight': 'bert/encoder/layer_{idx}/attention/self/value/kernel',
    'transformers.{idx}.attention.v_dense.bias': 'bert/encoder/layer_{idx}/attention/self/value/bias',
    'transformers.{idx}.attention.o_dense.weight': 'bert/encoder/layer_{idx}/attention/output/dense/kernel',
    'transformers.{idx}.attention.o_dense.bias': 'bert/encoder/layer_{idx}/attention/output/dense/bias',
    'transformers.{idx}.attention_LayerNorm.weight': 'bert/encoder/layer_{idx}/attention/output/LayerNorm/gamma',
    'transformers.{idx}.attention_LayerNorm.bias': 'bert/encoder/layer_{idx}/attention/output/LayerNorm/beta',
    'transformers.{idx}.ffn.W1.weight': 'bert/encoder/layer_{idx}/intermediate/dense/kernel',
    'transformers.{idx}.ffn.W1.bias': 'bert/encoder/layer_{idx}/intermediate/dense/bias',
    'transformers.{idx}.ffn.W2.weight': 'bert/encoder/layer_{idx}/output/dense/kernel',
    'transformers.{idx}.ffn.W2.bias': 'bert/encoder/layer_{idx}/output/dense/bias',
    'transformers.{idx}.ffn_LayerNorm.weight': 'bert/encoder/layer_{idx}/output/LayerNorm/gamma',
    'transformers.{idx}.ffn_LayerNorm.bias': 'bert/encoder/layer_{idx}/output/LayerNorm/beta',

    # pooler
    'pooler.dense.weight': 'bert/pooler/dense/kernel',
    'pooler.dense.bias': 'bert/pooler/dense/bias',

    # tasks
    'mlm.dense.weight': 'cls/predictions/transform/dense/kernel',
    'mlm.dense.bias': 'cls/predictions/transform/dense/bias',
    'mlm.LayerNorm.weight': 'cls/predictions/transform/LayerNorm/gamma',
    'mlm.LayerNorm.bias': 'cls/predictions/transform/LayerNorm/beta',
    'mlm.decoder.bias': 'cls/predictions/output_bias',
    'nsp.dense.weight': 'cls/seq_relationship/output_weights',
    'nsp.dense.bias': 'cls/seq_relationship/output_bias',
}

WEIGHTS_MAP_TRANSFORMERS = {
    # embeddings
    'embeddings.word_embeddings.weight': 'bert.embeddings.word_embeddings.weight',
    'embeddings.position_embeddings.weight': 'bert.embeddings.position_embeddings.weight',
    'embeddings.token_type_embeddings.weight': 'bert.embeddings.token_type_embeddings.weight',
    'embeddings.LayerNorm.weight': 'bert.embeddings.LayerNorm.weight',
    'embeddings.LayerNorm.bias': 'bert.embeddings.LayerNorm.bias',

    # transformers
    'transformers.{idx}.attention.q_dense.weight': 'bert.encoder.layer.{idx}.attention.self.query.weight',
    'transformers.{idx}.attention.q_dense.bias': 'bert.encoder.layer.{idx}.attention.self.query.bias',
    'transformers.{idx}.attention.k_dense.weight': 'bert.encoder.layer.{idx}.attention.self.key.weight',
    'transformers.{idx}.attention.k_dense.bias': 'bert.encoder.layer.{idx}.attention.self.key.bias',
    'transformers.{idx}.attention.v_dense.weight': 'bert.encoder.layer.{idx}.attention.self.value.weight',
    'transformers.{idx}.attention.v_dense.bias': 'bert.encoder.layer.{idx}.attention.self.value.bias',
    'transformers.{idx}.attention.o_dense.weight': 'bert.encoder.layer.{idx}.attention.output.dense.weight',
    'transformers.{idx}.attention.o_dense.bias': 'bert.encoder.layer.{idx}.attention.output.dense.bias',
    'transformers.{idx}.attention_LayerNorm.weight': 'bert.encoder.layer.{idx}.attention.output.LayerNorm.weight',
    'transformers.{idx}.attention_LayerNorm.bias': 'bert.encoder.layer.{idx}.attention.output.LayerNorm.bias',
    'transformers.{idx}.ffn.W1.weight': 'bert.encoder.layer.{idx}.intermediate.dense.weight',
    'transformers.{idx}.ffn.W1.bias': 'bert.encoder.layer.{idx}.intermediate.dense.bias',
    'transformers.{idx}.ffn.W2.weight': 'bert.encoder.layer.{idx}.output.dense.weight',
    'transformers.{idx}.ffn.W2.bias': 'bert.encoder.layer.{idx}.output.dense.bias',
    'transformers.{idx}.ffn_LayerNorm.weight': 'bert.encoder.layer.{idx}.output.LayerNorm.weight',
    'transformers.{idx}.ffn_LayerNorm.bias': 'bert.encoder.layer.{idx}.output.LayerNorm.bias',

    # pooler
    'pooler.dense.weight': 'bert.pooler.dense.weight',
    'pooler.dense.bias': 'bert.pooler.dense.bias',

    # tasks
    'mlm.dense.weight': 'cls.predictions.transform.dense.weight',
    'mlm.dense.bias': 'cls.predictions.transform.dense.bias',
    'mlm.LayerNorm.weight': 'cls.predictions.transform.LayerNorm.weight',
    'mlm.LayerNorm.bias': 'cls.predictions.transform.LayerNorm.bias',
    'mlm.decoder.weight': 'cls.predictions.decoder.weight',
    'mlm.decoder.bias': 'cls.predictions.bias',
    'nsp.dense.weight': 'cls.seq_relationship.weight',
    'nsp.dense.bias': 'cls.seq_relationship.bias',
}


class BertTokenizer(_BertTokenizer):
    """
    Examples:
        >>> text = '我爱python，我爱编程；I love python, I like programming. Some unkword'

        # 模型输入
        >>> _, token_ids, token_type_ids = tokenizer.encode(text, return_token_type_ids=True)
        >>> assert token_ids[:6].tolist() == [101, 2769, 4263, 9030, 8024, 2769]
        >>> assert token_type_ids.tolist() == [0] * len(token_ids)

        # 句对模式
        >>> txt1 = '我爱python'
        >>> txt2 = '我爱编程'
        >>> _, token_ids, token_masks = tokenizer.encode(txt1, txt2, return_token_masks=True)
        >>> assert token_ids.tolist() == [101, 2769, 4263, 9030, 102, 2769, 4263, 5356, 4923, 102]
        >>> assert token_masks.tolist() == [1] * 10

        >>> # batch 模式
        >>> ss = ['我爱python', '深度学习', '机器学习']
    """

    def encode(self, txt1, txt2=None,
               max_len=None,
               return_token_type_ids=False,
               return_token_masks=False,
               convert_fn=torch.as_tensor):
        """"""
        return super().encode(txt1, txt2=txt2,
                              max_len=max_len,
                              return_token_type_ids=return_token_type_ids,
                              return_token_masks=return_token_masks,
                              convert_fn=convert_fn)

    def batch_encode(self,
                     texts,
                     max_len=None,
                     convert_fn=torch.as_tensor,
                     return_token_type_ids=False,
                     return_token_masks=False):
        """"""
        return super().batch_encode(texts,
                                    max_len=max_len,
                                    return_token_type_ids=return_token_type_ids,
                                    return_token_masks=return_token_masks,
                                    convert_fn=convert_fn)


_default_vocab_path = os.path.join(os.path.dirname(__file__), 'vocab/cn.txt')
tokenizer = BertTokenizer(_default_vocab_path)


def set_CKPT_DIR(ckpt_dir):  # noqa
    """"""
    set_env('CKPT', ckpt_dir)


def get_CKPT_DIR():  # noqa
    return get_env('CKPT', os.path.join(os.environ['HOME'], 'workspace/ckpt'))


def build_bert_pretrained(ckpt_path, **kwargs):
    from ._bert import Bert
    return Bert.from_pretrained(ckpt_path, **kwargs)


def build_rbt3(ckpt_path=None, config_file_name=None, from_tf=None):
    """"""
    if ckpt_path is None:
        ckpt_path = os.path.join(get_CKPT_DIR(), 'chinese_rbt3_L-3_H-768_A-12')

    if from_tf is None:
        from_tf = _check_from_tensorflow(ckpt_path)

    if config_file_name is None:
        config_file_name = 'bert_config_rbt3.json' if from_tf else 'config.json'

    from ._bert import Bert
    model = Bert.from_pretrained(ckpt_path,
                                 config_file_name=config_file_name)

    return model


def _check_from_tensorflow(ckpt_path):
    """"""
    if os.path.isdir(ckpt_path):
        fns = os.listdir(ckpt_path)
        return any(fn.find('index') != -1 for fn in fns)
    else:
        return False


def get_pretrained_assets(ckpt_path,
                          num_hidden_layers: Union[int, List[int]] = None,
                          config_file_name: str = None,
                          weight_file_name: str = None,
                          vocab_file_name: str = None,
                          return_tokenizer: bool = False,
                          from_tensorflow: bool = None,
                          name_mapping: Dict = None,
                          name_prefix: str = None,
                          remove_mapping_prefix: bool = False):
    """

    Args:
        ckpt_path:
        num_hidden_layers:
        config_file_name: 
        weight_file_name:
        vocab_file_name:
        return_tokenizer:
        from_tensorflow: 是否 tf 权重
        name_mapping: 权重名称映 {key: value}
            如：'embeddings.word_embeddings.weight': 'bert.embeddings.word_embeddings.weight'
        name_prefix: 给 name_mapping 中 key 添加前缀
            如 'embeddings.word_embeddings.weight' -> 'bert.embeddings.word_embeddings.weight'
        remove_mapping_prefix: 移除 name_mapping 中 value 的前缀（special for SentenceTransformer weights）
            如 'bert.embeddings.word_embeddings.weight' -> 'embeddings.word_embeddings.weight'
    """
    from ._bert import BertConfig

    if from_tensorflow is None:
        from_tensorflow = _check_from_tensorflow(ckpt_path)

    if config_file_name is None:
        config_file_name = 'bert_config.json' if from_tensorflow else 'config.json'

    if weight_file_name is None:
        weight_file_name = 'bert_model.ckpt' if from_tensorflow else 'pytorch_model.bin'

    config_path = os.path.join(ckpt_path, config_file_name)
    if os.path.exists(config_path):
        args: BertConfig = load_config_file(config_path, cls=BertConfig)
    else:
        args = BertConfig()

    if num_hidden_layers is None:
        num_hidden_layers = args.num_hidden_layers
    else:
        if isinstance(num_hidden_layers, List):
            args.num_hidden_layers = len(num_hidden_layers)
        else:
            args.num_hidden_layers = num_hidden_layers

    if os.path.isdir(ckpt_path):
        state_dict_path = os.path.join(ckpt_path, weight_file_name)
    else:
        state_dict_path = ckpt_path
    state_dict = get_state_dict(state_dict_path, from_tf=from_tensorflow)

    if name_mapping is None:
        mapping_temp = WEIGHTS_MAP_GOOGLE if from_tensorflow else WEIGHTS_MAP_TRANSFORMERS
        name_mapping = get_name_mapping(num_hidden_layers, mapping_temp, prefix=name_prefix,
                                        remove_mapping_prefix=remove_mapping_prefix)

    # 权重映射
    for name, name_old in name_mapping.items():
        if name_old in state_dict:
            state_dict[name] = state_dict.pop(name_old)  # 替换新名称

    if return_tokenizer:
        vocab_file_name = vocab_file_name or 'vocab.txt'
        vocab_path = os.path.join(ckpt_path, vocab_file_name)
        if not os.path.exists(vocab_path):
            logger.warning(f'return_tokenizer is True, but there is no {vocab_file_name} in ckpt path. '
                           f'It will use default tokenizer with chinese vocab.')
            _tokenizer = tokenizer
        else:
            _tokenizer = BertTokenizer(vocab_path)
        return args, state_dict, _tokenizer

    return args, state_dict


def get_name_mapping(num_transformers: Union[int, List[int]], mapping_temp: dict,
                     prefix: str = None,
                     remove_mapping_prefix=False):
    """
    只保证 transformers.BertModel 的权重能顺利加载，像其他重新构建的模型，比如 Bart，则不行

    Args:
        num_transformers:
        mapping_temp:
        prefix: 给 mapping_temp 的 key 部分加前缀；
            如果是直接给 Bert 加载权重，则 prefix_k == ''；
            如果是给模型的子 Module 加载权重，则需要添加前缀，
            比如下面的情况，prefix == 'bert'，
            即 'embeddings.LayerNorm.weight' -> 'bert.embeddings.LayerNorm.weight'
            ```
            class MyModel(torch.nn.Module):
                def __init__(self):
                    super().__init__()
                    self.bert = Bert()
            ```
        remove_mapping_prefix: 移除 mapping_temp 中 value 部分的前缀（兼容 SentenceTransformer），
            如 'bert.embeddings.LayerNorm.weight' -> 'embeddings.LayerNorm.weight'
    """
    if prefix is None:
        prefix = ''
    elif not prefix.endswith('.'):
        prefix += '.'

    if isinstance(num_transformers, List):
        idx_vs = num_transformers
    else:
        idx_vs = list(range(num_transformers))

    mapping_dict = dict()
    for name_k, name_v in mapping_temp.items():
        if not (name_k.startswith('mlm') or name_k.startswith('nsp')):
            name_k = prefix + name_k
        if remove_mapping_prefix:
            name_v = name_v[5:]  # remove 'bert.'

        if re.search(r'idx', name_k):
            for idx_k, idx_v in enumerate(idx_vs):
                name_k_idx = name_k.format(idx=idx_k)
                name_v_idx = name_v.format(idx=idx_v)
                mapping_dict[name_k_idx] = name_v_idx
        else:
            mapping_dict[name_k] = name_v

    return mapping_dict


def get_state_dict(weights_path, from_tf=False):
    """ 加载预训练权重字典 {weight_name: tensor} """

    def _update_state_dict_keys(_state_dict):
        """"""
        # 特殊处理：一些 pt 权重参数中 LN 层的参数名依然为 gamma 和 beta（官方实现应该为 weight 和 bias）
        #   推测应该是使用了自定义 LN 层，所以参数名称不同，这里需要特殊处理一下
        tmp_keys = []
        for key in _state_dict.keys():
            new_key = None
            if "gamma" in key:
                new_key = key.replace("gamma", "weight")
            if "beta" in key:
                new_key = key.replace("beta", "bias")
            if new_key:
                tmp_keys.append((key, new_key))

        for old_key, new_key in tmp_keys:
            _state_dict[new_key] = _state_dict.pop(old_key)

        return _state_dict

    if from_tf:
        state_dict = load_state_dict_tf(weights_path)
    else:
        state_dict = load_state_dict_pt(weights_path)
        _update_state_dict_keys(state_dict)
    return state_dict


def _test():
    """"""
    doctest.testmod()


if __name__ == '__main__':
    """"""
    _test()
