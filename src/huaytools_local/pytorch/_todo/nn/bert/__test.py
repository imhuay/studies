#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Time: 2021-11-03 2:31 下午

Author: huayang

Subject:

"""

import numpy as np

from huaytools_local.pytorch._todo.nn import *

os.environ['TRANSFORMERS_OFFLINE'] = '1'  # 离线模式


@torch.no_grad()
def _test_mlm():
    """"""
    from transformers.models.bert import BertForPreTraining
    # 模型构建
    pt_ckpt_path = os.path.join(get_CKPT_DIR(), 'bert-base-chinese')
    bert_my = BertPretrain.from_pretrained(pt_ckpt_path)
    bert_tr = BertForPreTraining.from_pretrained(pt_ckpt_path)

    # 模型输入
    _, token_ids = tokenizer.encode(r'科学技术是第一生产力', convert_fn=None)
    # mask '技术'
    token_ids[3] = token_ids[4] = tokenizer.token2id_map['[MASK]']
    inputs = torch.as_tensor([token_ids])

    # mine
    mlm_logits, _ = bert_my(inputs)
    # transformers
    prediction_logits = bert_tr(inputs).prediction_logits
    assert torch.allclose(mlm_logits, prediction_logits, atol=1e-5)
    assert list(mlm_logits.shape) == [1, 12, 21128]
    ret = mlm_logits[0][3:5].argmax(axis=1)
    assert [tokenizer.id2token_map[id_] for id_ in ret.tolist()] == ['技', '术']


@torch.no_grad()
def _test_load_weights():
    """"""

    def count_no_decay(m):
        """"""
        no_decay_params = ('LayerNorm.weight',)  # 'bias'
        cnt = 0
        for n, t in m.state_dict().items():
            for N in no_decay_params:
                if N in n:
                    cnt += 1

        return cnt

    # 构建模型
    from transformers import BertModel

    # google 原始 bert 权重
    tf_ckpt_path = os.path.join(get_CKPT_DIR(), 'chinese_L-12_H-768_A-12')
    # transformers.BertModel 的权重
    pt_ckpt_path = os.path.join(get_CKPT_DIR(), 'bert-base-chinese')
    bert_my_tf = Bert.from_pretrained(tf_ckpt_path)
    bert_my_tr = Bert.from_pretrained(pt_ckpt_path)
    bert_tr = BertModel.from_pretrained(pt_ckpt_path)
    bert_tr.config.output_hidden_states = True

    assert len(bert_my_tf.state_dict()) == len(bert_tr.state_dict())

    ss = ['我爱NLP', '我爱Python']
    token_ids, token_type_ids, token_masks = tokenizer.batch_encode(ss, convert_fn=torch.as_tensor,
                                                                    return_token_type_ids=True,
                                                                    return_token_masks=True)

    cls_embedding, token_embeddings, all_hidden_states = bert_my_tf(token_ids, token_type_ids, token_masks)
    # print(cls_embedding.shape)
    assert torch.allclose(cls_embedding[0, :5],
                          torch.Tensor([0.9974924, 0.99995434, 0.9740488, 0.8418756, 0.97812724]), atol=1e-5)

    # 对比 transformers.Bert 的结果
    o_pt = bert_tr(token_ids, token_masks, token_type_ids)

    assert count_no_decay(bert_my_tf) == count_no_decay(bert_tr)
    assert np.allclose(o_pt.pooler_output, cls_embedding, atol=1e-5)
    assert np.allclose(o_pt.last_hidden_state, token_embeddings, atol=1e-5)
    assert np.allclose(torch.cat(o_pt.hidden_states), torch.cat(all_hidden_states), atol=1e-5)

    # 使用 transformers.BertModel 的权重创建模型
    cls_embedding, token_embeddings, all_hidden_states = bert_my_tr(token_ids, token_type_ids, token_masks)
    assert np.allclose(o_pt.pooler_output, cls_embedding, atol=1e-5)
    assert np.allclose(o_pt.last_hidden_state, token_embeddings, atol=1e-5)
    assert np.allclose(torch.cat(o_pt.hidden_states), torch.cat(all_hidden_states), atol=1e-5)

    # 测试 tracing 化
    traced_bert = torch.jit.trace(bert_my_tr, (token_ids, token_type_ids, token_masks))

    new_ss = ['测试1', '测试2', '测试3']
    new_inputs = tokenizer.batch_encode(new_ss, convert_fn=torch.as_tensor,
                                        return_token_type_ids=True,
                                        return_token_masks=True)
    o1 = bert_my_tr(*new_inputs)
    o2 = traced_bert(*new_inputs)
    assert torch.equal(torch.cat(o1[-1]), torch.cat(o2[-1]))


@torch.no_grad()
def _test_load_appointed_layers():
    """"""
    # transformers.BertModel 的权重
    pt_ckpt_path = os.path.join(get_CKPT_DIR(), 'bert-base-chinese')
    # 默认加载前 n 层
    bert_my_1 = Bert.from_pretrained(pt_ckpt_path, num_hidden_layers=3)
    bert_my_2 = Bert.from_pretrained(os.path.join(pt_ckpt_path, 'pytorch_model.bin'), num_hidden_layers=[0, 1, 2])

    ss = ['我爱NLP', '我爱Python']
    token_ids, token_type_ids, token_masks = tokenizer.batch_encode(ss, convert_fn=torch.as_tensor,
                                                                    return_token_type_ids=True,
                                                                    return_token_masks=True)

    o1 = bert_my_1(token_ids, token_type_ids, token_masks, return_value='all_hidden_states')
    o2 = bert_my_2(token_ids, token_type_ids, token_masks, return_value='all_hidden_states')
    assert torch.equal(torch.cat(o1), torch.cat(o2))

    # 最后三层 transformer
    bert_my_3 = Bert.from_pretrained(pt_ckpt_path, num_hidden_layers=[9, 10, 11])
    assert len(list(bert_my_3.named_parameters())) == 55
    # 指定三层 transformer
    bert_my_4 = Bert.from_pretrained(pt_ckpt_path, num_hidden_layers=[0, 10, 11])
    assert len(list(bert_my_4.named_parameters())) == 55


def _test_rbt3():
    """"""
    rbt3_ckpt = os.path.join(get_CKPT_DIR(), 'rbt3')
    rbt3_my_tf = build_rbt3()
    rbt3_my_pt = build_rbt3(rbt3_ckpt)
    from transformers import BertModel
    rbt3_tr = BertModel.from_pretrained(rbt3_ckpt)

    ss = ['我爱NLP', '我爱Python']
    token_ids, token_type_ids, token_masks = tokenizer.batch_encode(ss, convert_fn=torch.as_tensor,
                                                                    return_token_type_ids=True,
                                                                    return_token_masks=True)
    o_my_tf = rbt3_my_tf(token_ids, token_type_ids, token_masks, return_value='token_embeddings')
    o_my_pt = rbt3_my_pt(token_ids, token_type_ids, token_masks, return_value='token_embeddings')
    o_tr = rbt3_tr(token_ids, token_masks, token_type_ids)[0]
    assert torch.allclose(o_my_tf, o_my_pt, atol=1e-5) and torch.allclose(o_my_pt, o_tr, atol=1e-5)


def _test_sentence_bert():
    """"""
    from sentence_transformers import SentenceTransformer
    pt_ckpt_path = os.path.join(get_CKPT_DIR(), 'bert-base-chinese')
    bert = Bert.from_pretrained(pt_ckpt_path)
    bert_sent_my = SentenceBert(bert, pool_mode='mean')
    bert_sent_tr = SentenceTransformer(pt_ckpt_path)

    ss = ['我爱NLP', '我爱Python']
    token_ids, token_type_ids, token_masks = tokenizer.batch_encode(ss, convert_fn=torch.as_tensor,
                                                                    return_token_type_ids=True,
                                                                    return_token_masks=True)

    o_my = bert_sent_my(token_ids)
    o_tr = bert_sent_tr({'input_ids': token_ids, 'attention_mask': token_masks})
    assert torch.equal(o_my, o_tr['sentence_embedding'])


def _test():
    """"""
    doctest.testmod()

    _test_sentence_bert()
    _test_rbt3()
    _test_load_appointed_layers()
    _test_mlm()
    _test_load_weights()


if __name__ == '__main__':
    """"""
    _test()
