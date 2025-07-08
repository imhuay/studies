#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Time: 2021-10-23 9:31 下午

Author: huayang

Subject:

"""

import torch
from torch import nn as nn

from huaytools_local.pytorch._todo._modules import EncoderWrapper


class ClassificationLayer(nn.Module):
    """"""
    SINGLE_LABEL = 'single'  # 单标签
    MULTI_LABEL = 'multi'  # 多标签
    REGRESSION = 'regress'  # 回归

    def __init__(self,
                 n_classes=2,
                 hidden_size=768,
                 problem_type='single'):
        """

        Args:
            n_classes:
            problem_type: one of {'single', 'multi', 'regress'}
            hidden_size:
        """
        super().__init__()

        self.n_classes = n_classes
        self.dense = nn.Linear(hidden_size, n_classes)
        self.softmax = nn.Softmax(-1)
        self.sigmoid = nn.Sigmoid()

        self.problem_type = problem_type
        if problem_type == ClassificationLayer.REGRESSION:
            # logits.shape == labels.shape
            #   num_labels > 1, shape: [B, N];
            #   num_labels = 1, shape: [B];
            self.loss_fn = nn.MSELoss()
        elif problem_type == ClassificationLayer.MULTI_LABEL:
            # logits.shape == labels.shape == [B, N];
            self.loss_fn = nn.BCEWithLogitsLoss()
        elif problem_type == ClassificationLayer.SINGLE_LABEL:
            # logits.shape: [B, N];
            # labels: [B];
            self.loss_fn = nn.CrossEntropyLoss()  # softmax-log-NLLLoss
        else:
            raise ValueError(f'Unsupported problem_type={problem_type}')

    def forward(self, inputs, labels=None):
        """"""
        logits = self.dense(inputs)  # [B, N] <=> [batch_size, num_labels]

        if self.problem_type == ClassificationLayer.REGRESSION and self.n_classes == 1:
            logits = logits.squeeze()  # [B, 1] -> [B]

        if self.problem_type == ClassificationLayer.SINGLE_LABEL:
            probs = self.softmax(logits)
        elif self.problem_type == ClassificationLayer.MULTI_LABEL:
            probs = self.sigmoid(logits)
        else:
            probs = logits

        if labels is None:  # eval
            return probs
        else:
            loss = self.loss_fn(logits, labels)
            return probs, loss


def _test():
    """"""

    def _test_EncoderWrapper():  # noqa
        """"""

        class TestEncoder(EncoderWrapper):
            """"""

            def __init__(self, encoder, encoder_helper):
                """"""
                super(TestEncoder, self).__init__(encoder, encoder_helper)
                self.loss_fn = nn.CrossEntropyLoss()

            def forward(self, _inputs, labels=None):
                """"""
                outputs = self.encode(_inputs)

                if labels is not None:
                    loss = self.loss_fn(outputs, labels)
                    return outputs, loss

                return outputs

        from huaytools_local.pytorch._todo._modules import get_bert_pretrained

        bert, tokenizer = get_bert_pretrained(return_tokenizer=True)
        encode_wrapper = lambda _e, _i: _e(*_i)[1].mean(1)  #
        test_encoder = EncoderWrapper(bert, encode_wrapper)

        ss = ['测试1', '测试2']
        inputs = tokenizer.batch_encode(ss, max_len=10, convert_fn=torch.as_tensor)
        o = test_encoder(inputs)
        assert list(o.shape) == [2, 768]

    _test_EncoderWrapper()

    def _test_TextClassification_fine_tune():  # noqa
        """"""
        from huaytools_local.pytorch._todo._modules import Bert
        inputs = [torch.tensor([[1, 2, 3]]), torch.tensor([[0, 0, 0]])]

        class Test(nn.Module):
            """"""

            def __init__(self, num_labels=1):
                super(Test, self).__init__()

                self.bert = Bert()
                self.clf = ClassificationLayer(num_labels)
                # self.bert.load_weights()  # 可选

            def forward(self, _inputs):
                outputs = self.bert(*_inputs)
                cls_embedding = outputs[0]
                ret = self.clf(cls_embedding)
                return ret

        clf = Test()  # bert 参与训练
        logits = clf(inputs)
        print(logits)
        print('state_dict size:', len(clf.state_dict()))

    _test_TextClassification_fine_tune()

    def _test_TextClassification():  # noqa
        """"""
        from huaytools_local.pytorch._todo._modules import Bert
        test_inputs = [torch.tensor([[1, 2, 3]]), torch.tensor([[0, 0, 0]])]
        bert = Bert()
        outputs = bert(*test_inputs)
        inputs = outputs[0]  # cls_embedding

        with torch.no_grad():
            classifier = ClassificationLayer(n_classes=3)
            logits = classifier(inputs)
            print(logits)

        # bert 不参与训练
        print('state_dict size:', len(classifier.state_dict()))

    _test_TextClassification()


if __name__ == '__main__':
    """"""
    _test()
