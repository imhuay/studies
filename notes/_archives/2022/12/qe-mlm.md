基于 BERT/MLM 的查询扩展方法
===
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2025-07-08%2016%3A53%3A13&color=yellowgreen&style=flat-square)

<!--END_SECTION:badge-->
<!--info
top: false
hidden: false
-->

<!-- TOC -->
- [CLEF 2021](#clef-2021)
<!-- TOC -->

## CLEF 2021
> Green, Tommaso, Luca Moroldo, and Alberto Valente. "Exploring BERT Synonyms and Quality Prediction for Argument Retrieval." CLEF (Working Notes). 2021.

1. 对 query 进行词性标注, 对名词/形容词/过去分词 MASK;
2. 使用 BERT 预测被 MASK 部分的 top N (N = 10) 候选;
3. 使用 BERT 计算所有生成 token 的 embedding, 并与原始 token 计算 cosine 相似度;
    > embedding 由 BERT 的后 4 层输出拼接而成, 因此 embed_size = 768 * 4 = 3072;
    >> [[1810.04805] BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding](https://arxiv.org/abs/1810.04805)
4. 保留相似度大于 $\alpha$ (=0.85) 的 token;
    > 原文的做法更复杂一点, 考虑了相似度都小于 $\alpha$ 时如何进一步迭代;
5. 对每个位置的 token 计算笛卡尔积来生成候选, 随机取其中 max_n_query 的 query 作为候选;
    > 改进: 可以利用语言模型计算每个扩展 query 的得分, 取 top;