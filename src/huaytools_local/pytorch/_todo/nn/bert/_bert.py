#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Time:
    2021-06-30 8:14 下午

Author:
    huayang

Subject:

"""
import os  # noqa
import doctest  # noqa

from typing import *
from logging import Logger
from argparse import Namespace
from typing import Dict

import torch
import torch.nn as nn
import torch.nn.functional as F  # noqa

from torch import Tensor

from huaytools_local._python import BunchDict
from huaytools_local._python.utils import get_logger, set_attr, get_attr, get_caller_name
from huaytools_local.pytorch.utils import load_state_dict_explicit, init_weights
from huaytools_local.pytorch._todo._backend import ACT_STR2FN

from .utils import get_pretrained_assets
from .bert_nsp import NextSentencePrediction
from .bert_mlm import MaskedLanguageModel
from ..transformer import Transformer

__all__ = [
    'Bert',
    'BertConfig',
    'BertPretrain',
]


class BertConfig(BunchDict):
    """
    Examples:
        >>> args = BertConfig()
        >>> args.hidden_size
        768
        >>> args = BertConfig(hidden_size=128)
        >>> args.hidden_size
        128
        >>> save_fp = r'./bert_config.json'
        >>> args.save(save_fp)
        >>> del args
        >>> args = BertConfig.load(save_fp)
        >>> args.hidden_size
        128
        >>> os.system(f'rm {save_fp}')
        0
    """

    def __init__(self, **kwargs):
        """ Default Base Config """

        self.hidden_size = 768  # hidden_size
        self.vocab_size = 21128  # chinese vocab
        self.intermediate_size = 3072  # 768 * 4
        self.num_hidden_layers = 12  # num_transformers
        self.num_attention_heads = 12  # num_attention_heads
        self.max_position_embeddings = 512  # max_seq_len
        self.type_vocab_size = 2  # num_token_type
        self.hidden_act = 'gelu'  # activation_fn
        self.hidden_dropout_prob = 0.1  # dropout_prob
        self.attention_probs_dropout_prob = 0.1  # attention_dropout_prob
        self.initializer_range = 0.02  # normal_std

        # no use
        self.directionality = "bidi"
        self.pooler_fc_size = 768
        self.pooler_num_attention_heads = 12
        self.pooler_num_fc_layers = 3
        self.pooler_size_per_head = 128
        self.pooler_type = "first_token_transform"

        super().__init__(**kwargs)


class Bert(nn.Module):
    """@Pytorch Models
    Bert by Pytorch

    Examples:
        >>> bert = Bert()

        >>> ex_token_ids = torch.randint(100, [2, 3])
        >>> o = bert(ex_token_ids)
        >>> o[0].shape
        torch.Size([2, 768])
        >>> o[1].shape
        torch.Size([2, 3, 768])

        # Tracing
        >>> _ = bert.eval()  # avoid TracerWarning
        >>> traced_bert = torch.jit.trace(bert, (ex_token_ids,))
        >>> inputs = torch.randint(100, [5, 6])
        >>> torch.equal(traced_bert(inputs)[1], bert(inputs)[1])
        True

        # >>> print(traced_bert.code)

    """
    logger: Logger

    def __init__(self,
                 args: Union[Dict, Namespace] = None,
                 _init_weights: bool = False):
        """"""
        super().__init__()
        self.logger = get_logger(self.__class__.__name__)
        self.args = args or BertConfig()

        # build model
        self.embeddings = BertEmbedding(vocab_size=self.vocab_size,
                                        embedding_size=self.hidden_size,
                                        max_position_embeddings=self.max_position_embeddings,
                                        type_vocab_size=self.type_vocab_size,
                                        dropout_prob=self.hidden_dropout_prob)
        self.transformers = nn.ModuleList([Transformer(hidden_size=self.hidden_size,
                                                       intermediate_size=self.intermediate_size,
                                                       num_attention_heads=self.num_attention_heads,
                                                       activation_fn=self.hidden_act,
                                                       dropout_prob=self.hidden_dropout_prob,
                                                       attention_dropout_prob=self.attention_probs_dropout_prob)
                                           for _ in range(self.num_hidden_layers)])
        self.pooler = BertPooling(hidden_size=self.hidden_size)

        # init weights
        if _init_weights:
            self.apply(lambda m: init_weights(m, self.initializer_range))  # recursive init all modules

    def forward(self,
                token_ids: Tensor,
                token_type_ids: Tensor = None,
                token_masks: Tensor = None,
                return_value: str = None):
        """
        Args:
            token_ids: [B, L]
            token_type_ids: [B, L]
            token_masks: [B, L]
            return_value:

        Notes:
            踩坑记录 (torch==1.8)：
                对于在 forward 中生成的 tensor，当模型 trace 化时 device 会被固定下来，影响模型的迁移；
                因此，除非这些中间 tensor 可以通过 inputs 生成，否则不建议自动生成
        """

        if token_type_ids is None:  # 默认输入是单句，即全0
            token_type_ids = token_ids - token_ids  # 这样 device 将始终与 token_ids 保持一致
            # token_type_ids = torch.zeros(token_ids.shape, dtype=token_ids.dtype, device=token_ids.device)
            # 注意：使用上述方法在 tracing 时，device 会被固定为当时的环境，导致迁移时可能出现问题

        if token_masks is None:  # masks 为 None 时，根据 token_ids 推断
            token_masks = (token_ids > 0).to(torch.uint8)  # [B, L]
            # token_masks = (token_ids > 0).to(torch.uint8).to(token_ids.device)
            # 因为是通过 token_ids 生成，所以 device 与 token_ids 一致，不用重新设置

        # embedding
        x = self.embeddings(token_ids, token_type_ids)

        # transformers
        all_hidden_states = (x,)  # avoid tracing warning
        for transformer in self.transformers:
            x = transformer(x, token_masks)  # [B, L, N]
            all_hidden_states += (x,)

        # pooler
        token_embeddings = all_hidden_states[-1]  # [B, L, N]
        cls_before_pooler = token_embeddings[:, 0]  # [B, N]
        cls_embedding = self.pooler(cls_before_pooler)  # [B, N]

        # all_hidden_states = tuple(all_hidden_states)  # avoid tracing warning
        outputs = (cls_embedding, token_embeddings, all_hidden_states)
        if return_value == 'cls_embedding':
            return outputs[0]
        elif return_value == 'token_embeddings':
            return outputs[1]
        elif return_value == 'all_hidden_states':
            return outputs[2]
        else:
            return outputs

    @classmethod
    def from_pretrained(cls, ckpt_path,
                        num_hidden_layers: Union[int, List[int]] = None,
                        name_mapping: Dict = None,
                        remove_mapping_prefix: bool = False,
                        config_file_name: str = None,
                        weight_file_name: str = None,
                        vocab_file_name: str = None,
                        from_tf: bool = None):
        """"""
        assets = get_pretrained_assets(ckpt_path,
                                       num_hidden_layers=num_hidden_layers,
                                       name_mapping=name_mapping,
                                       remove_mapping_prefix=remove_mapping_prefix,
                                       config_file_name=config_file_name,
                                       weight_file_name=weight_file_name,
                                       vocab_file_name=vocab_file_name,
                                       from_tensorflow=from_tf)

        args, weights_dict = assets[:3]
        bert = load_state_dict_explicit(cls(args), weights_dict)
        return bert

    @property
    def word_embeddings(self) -> Tensor:
        """"""
        return self.embeddings.word_embeddings.weight.data

    # === args ===
    def _get_attr(self, name: str = None):
        name = name or get_caller_name()  # 获取调用函数名（这里就是属性名）
        return get_attr(self.args, name)

    def _set_attr(self, value, name: str):
        name = name or get_caller_name()  # 获取调用函数名（这里就是属性名）
        set_attr(self.args, name, value)

    @property
    def hidden_size(self) -> int:
        """"""
        return self._get_attr()

    @property
    def vocab_size(self) -> int:
        return self._get_attr()

    @property
    def intermediate_size(self) -> int:
        return self._get_attr()

    @property
    def num_hidden_layers(self) -> int:
        return self._get_attr()

    @property
    def num_attention_heads(self) -> int:
        return self._get_attr()

    @property
    def max_position_embeddings(self) -> int:
        return self._get_attr()

    @property
    def type_vocab_size(self) -> int:
        return self._get_attr()

    @property
    def hidden_act(self) -> Callable:
        act_fn = self._get_attr()
        return ACT_STR2FN[act_fn] if isinstance(act_fn, str) else act_fn

    @property
    def hidden_dropout_prob(self) -> float:
        return self._get_attr()

    @property
    def attention_probs_dropout_prob(self) -> float:
        return self._get_attr()

    @property
    def initializer_range(self) -> float:
        return self._get_attr()


class BertEmbedding(nn.Module):
    """ Bert Embedding """

    def __init__(self,
                 vocab_size=21128,
                 embedding_size=768,
                 max_position_embeddings=512,
                 type_vocab_size=2,
                 pad_token_id=0,
                 dropout_prob=0.1,
                 layer_norm_eps=1e-12):
        """"""
        super().__init__()
        self.max_seq_len = max_position_embeddings

        self.word_embeddings = nn.Embedding(vocab_size, embedding_size, padding_idx=pad_token_id)
        self.position_embeddings = nn.Embedding(max_position_embeddings, embedding_size)
        self.token_type_embeddings = nn.Embedding(type_vocab_size, embedding_size)

        self.LayerNorm = nn.LayerNorm(embedding_size, eps=layer_norm_eps)
        self.dropout = nn.Dropout(dropout_prob)

        # not model parameters
        self.register_buffer("position_ids", torch.arange(max_position_embeddings).expand((1, -1)))

    def forward(self, token_ids, token_type_ids):
        """"""
        word_embeddings = self.word_embeddings(token_ids)
        token_type_embeddings = self.token_type_embeddings(token_type_ids)

        seq_length = token_ids.shape[1]
        position_ids = self.position_ids[:, :seq_length]
        position_embeddings = self.position_embeddings(position_ids)

        # embeddings Add
        embeddings = word_embeddings + token_type_embeddings + position_embeddings
        embeddings = self.LayerNorm(embeddings)  # layer_norm
        embeddings = self.dropout(embeddings)  # dropout
        return embeddings


class BertPooling(nn.Module):
    """ Bert Pooling """

    def __init__(self, hidden_size=768, activation_fn=torch.tanh):
        """"""
        super().__init__()

        self.dense = nn.Linear(hidden_size, hidden_size)
        self.act = activation_fn

    def forward(self, inputs):
        """"""
        return self.act(self.dense(inputs))


class BertPretrain(nn.Module):
    """@Pytorch Models
    Bert 预训练（MLM + NSP）

    References:
        https://github.com/microsoft/unilm/blob/master/unilm-v1/src/pytorch_pretrained_bert/modeling.py
        - BertForPreTraining
            - BertPreTrainingHeads
                - BertLMPredictionHead
    """

    def __init__(self,
                 args: BertConfig = None,
                 share_word_embeddings=False,
                 _init_weights: bool = False):
        """"""
        super().__init__()

        self.bert = Bert(args, _init_weights=_init_weights)
        self.mlm = MaskedLanguageModel(args.hidden_size,
                                       word_embeddings=self.bert.word_embeddings,
                                       share_word_embeddings=share_word_embeddings)
        self.nsp = NextSentencePrediction(args.hidden_size, num_classes=2)

    def forward(self,
                token_ids: Tensor,
                token_type_ids: Tensor = None,
                token_masks: Tensor = None,
                mlm_labels: Tensor = None,
                nsp_labels: Tensor = None):
        """"""
        cls_embedding, token_embeddings, all_hidden_states = self.bert(token_ids,
                                                                       token_type_ids=token_type_ids,
                                                                       token_masks=token_masks)
        mlm_outputs = self.mlm(token_embeddings, labels=mlm_labels)
        nsp_outputs = self.nsp(cls_embedding, labels=nsp_labels)

        total_loss = (token_ids - token_ids).float().mean()  # 0
        if mlm_labels is not None:
            mlm_logits, mlm_loss = mlm_outputs
            total_loss += mlm_loss
        else:
            mlm_logits = mlm_outputs

        if nsp_labels is not None:
            nsp_logits, nsp_loss = nsp_outputs
            total_loss += nsp_loss
        else:
            nsp_logits = nsp_outputs

        if mlm_labels or nsp_labels:
            return mlm_logits, nsp_logits, total_loss
        else:
            return mlm_logits, nsp_logits

    @classmethod
    def from_pretrained(cls, ckpt_path,
                        name_mapping: Dict = None,
                        config_file_name: str = None,
                        weight_file_name: str = None,
                        vocab_file_name: str = None,
                        from_tf: bool = None):
        """"""
        assets = get_pretrained_assets(ckpt_path,
                                       name_mapping=name_mapping,
                                       name_prefix='bert',
                                       config_file_name=config_file_name,
                                       weight_file_name=weight_file_name,
                                       vocab_file_name=vocab_file_name,
                                       from_tensorflow=from_tf)

        args, weights_dict = assets[:2]
        model = load_state_dict_explicit(cls(args), weights_dict)

        # 初始化 mlm 的 decoder 权重
        word_embeddings = model.bert.word_embeddings
        if not model.mlm.share_word_embeddings:
            word_embeddings = word_embeddings.clone()
        model.mlm.decoder.weight.data = word_embeddings
        return model
