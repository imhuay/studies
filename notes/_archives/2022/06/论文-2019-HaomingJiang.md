SMART Loss
===
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2022-10-13%2001%3A56%3A19&color=yellowgreen&style=flat-square)

<!--END_SECTION:badge-->
> [[1911.03437] SMART: Robust and Efficient Fine-Tuning for Pre-trained Natural Language Models through Principled Regularized Optimization](https://arxiv.org/abs/1911.03437)


## 摘要
- 迁移学习从根本上改变了自然语言处理（NLP）的格局。许多最先进的模型会先在大规模语料库上进行**预训练**，然后在下游任务上进行**微调**。
- 然而，由于下游任务的**数据资源有限**，且预训练模型的复杂度极高，主动微调往往会导致模型**过拟合**，无法推广到看不见的数据。
- 本文提出了一种微调方案，能够使模型具有更好的泛化能力；其主要包含两个部分
    - Smoothness-inducing regularization：限制模型的复杂度；
    - Bregman proximal point optimization：防止过度优化；

## 相关工作
- 一些常见的**防止过度学习**的方法：
    - 启发式学习率
    - 逐步解冻（gradually unfreeze）
    - 只微调部分层
    - 在模型中添加额外的参数或层，只训练这部分
- 缺点：需要进行大量的调优工作
- 
