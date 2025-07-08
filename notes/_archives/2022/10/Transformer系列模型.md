Transformer/BERT 常见变体
===
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2025-07-08%2016%3A53%3A13&color=yellowgreen&style=flat-square)

<!--END_SECTION:badge-->
<!--info
top: false
hidden: false
-->

<!-- TOC -->
- [概览](#概览)
    - [ALBERT](#albert)
    - [BART](#bart)
    - [ERNIE (Baidu)](#ernie-baidu)
    - [ERNIE (THU)](#ernie-thu)
    - [MT-DNN](#mt-dnn)
    - [RoBERTa](#roberta)
    - [SpanBERT](#spanbert)
    - [T5](#t5)
    - [UniLM*](#unilm)
    - [XLM](#xlm)
    - [XLNet*](#xlnet)
- [WIKI](#wiki)
    - [BPE](#bpe)
    - [抽取式问答](#抽取式问答)
    - [Masking Trick](#masking-trick)
    - [PLM](#plm)
    - [SBO](#sbo)
    - [Span mask](#span-mask)
    - [双流注意力机制](#双流注意力机制)
    - [TLM](#tlm)
    - [Transformer-XL](#transformer-xl)
<!-- TOC -->

<!-- 快速编辑

> algorithms/[xxx](../../../../algorithms/README.md#xxx)

<div align="center"><img src="../../../_assets/Sentence-BERT模型图.png" height="300" /></div>

<table>
<tr valign="top">
<th> ... </td>
<th> ... </td>
</tr>
<tr>
<td> ... </td>
<td> ... </td>
</tr>
</table>
-->

## 概览

<table >
<tr>
<th> Name </td>
<th> Features </td>
</tr>
<tr valign="top">
<td>

### ALBERT

</td>
<td>

- **简介**:
- **优化方向**:
- **改进方法**:

</td>
</tr>
<tr valign="top">
<td>

### BART

</td>
<td>

- **简介**:
- **优化方向**:
- **改进方法**:

</td>
</tr>
<tr valign="top">
<td>

### ERNIE (Baidu)

</td>
<td>

- **简介**:
- **优化方向**:
- **改进方法**:

</td>
</tr>
<tr valign="top">
<td>

### ERNIE (THU)

</td>
<td>

- **简介**:
- **优化方向**:
- **改进方法**:

</td>
</tr>
<tr valign="top">
<td>

### MT-DNN

</td>
<td>

- **简介**: MT-DNN (Multi-Task Deep Neural Network)
- **优化方向**: 进一步提升 BERT 在下游任务中的表现, 使具有更强的泛化能力;
- **改进方法**: 
    - 模型主体与 BERT 一致, 输出层为不同任务设计了各自的输出形式和目标函数;
    - 四个子任务: 单句分类, 文本相似度, 句对分类, 相关性排序;

</td>
</tr>
<tr valign="top">
<td>

### RoBERTa

</td>
<td>

- **简介**:
- **优化方向**:
- **改进方法**:

</td>
</tr>
<tr valign="top">
<td>

### SpanBERT

</td>
<td>

- **优化方向**: 通过扩大掩码范围提升模型性能; 服务于[抽取式问答](#抽取式问答)任务;
- **改进方法**:
    - 模型结构与 BERT 一致;
    - 使用 [Span mask](#span-mask) 方案, 对局部连续的 token 做 mask 来扩大掩码的粒度;
    - 使用 [SBO](#sbo) (Span Boundary Objective) 作为训练方法;

</td>
</tr>
<tr valign="top">
<td>

### T5

</td>
<td>

- **简介**:
- **优化方向**:
- **改进方法**:

</td>
</tr>
<tr valign="top">
<td>

### UniLM*

</td>
<td>

- **简介**: UniLM (Unified Pre-trained Language Model, 统一预训练语言模型)
- **优化方向**: 在 BERT 的基础上获得**文本生成**的能力;
- **改进方法**:
    - 模型结构与 BERT 基本一致, 仅通过调整 Attention Mask, 使模型具有多种语言模型的能力;
        > [Masking 技巧](#masking-trick);

</td>
</tr>
<tr valign="top">
<td>

### XLM

</td>
<td>

- **简介**: XLM (Cross-lingual Language Model, 跨语言的语言模型);
- **优化方向**: 使 BERT 具有跨语言表征的能力;
- **改进方法**:
    - 模型结构与 BERT 一致;
    - 使用 [BPE](#bpe) 分词, 缓解未登录词过多的问题;
    - 使用 [TLM](#tlm) 和双语语料训练;
        > 实际为 MLM 和 TML 交叉训练;

</td>
</tr>
<tr valign="top">
<td>

### XLNet*

</td>
<td>

- **简介**: 使用 [Transformer-XL](#transformer-xl) 作为特征提取器
- **优化方向**:
- **改进方法**:
    - 提出 [PLM](#plm) 训练方法, 解决 MLM 中 `[MASK]` 的问题;
    - 提出[双流注意力机制](#双流注意力机制)配合 PLM 训练;
    - 使用 Transformer-XL 作为特征提取器, 加强长文本理解能力;
- 参考资料
    - [乱序语言模型 - 科学空间](https://kexue.fm/archives/6933#乱序语言模型)

</td>
</tr>
</table>


## WIKI

### BPE
> Byte Pair Encoding
- 由于不同语料的数量不一致, 因此构建 BPE 融合词表时需要

### 抽取式问答

### Masking Trick
> [从语言模型到Seq2Seq：Transformer如戏，全靠Mask - 苏剑林](https://kexue.fm/archives/6933)

### PLM
> Permutation Language Model

- 实现方法:
    - 将一句话中的随机打乱, 得到一个排列 (Permutation), 然后用单向编码的方式预测该排列末尾 15% 的词;
    - 具体实现时, 不会真的打乱顺序, 而是通过调整 Mask 矩阵实现;

### SBO
> Span Boundary Objective


### Span mask

### 双流注意力机制
> Two-Stream Self-Attention

### TLM
> Translated Language Model

### Transformer-XL