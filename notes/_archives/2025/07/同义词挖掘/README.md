同义词挖掘
===
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2025-08-02%2000%3A21%3A38&color=yellowgreen&style=flat-square)

<!--END_SECTION:badge-->
<!--info
top: false
hidden: true
-->

> ***Keywords**: 同义词挖掘*

<!--START_SECTION:toc-->
- [同义词挖掘基本流程](#同义词挖掘基本流程)
- [背景](#背景)
<!--END_SECTION:toc-->


<!--

<div align='center'><img src='path/to/xxx.png' height='300'/></div>

<details><summary><b>点击展开</b></summary>
</details>

HTML 空格: &nbsp;
-->

## 同义词挖掘基本流程

<details><summary><b>1. 挖掘候选 pair (同义词对)</b></summary>

**基于用户行为**
- Session 共现 (用户在一段时间内先后输入的不同搜索词)
    - 这些词在语义或意图上可能存在关联, 可作为潜在同义词候选对;
- 点击同源 (统计不同搜索词点击相同实体的比例)
    - Query A -> 实体 X
    - Query A -> 实体 X
    - **(可选)** 当 $P(X|Q_A) ≈ P(X|Q_B)$ 时视为候选对

    $$P(X|Q) = \frac{搜索词Q点击商户X的次数}{搜索词Q的点击总次数}$$

**基于文本相似度**
1. 中文拼音相似度 (如"麦当劳" vs "麦当当");
2. 编辑距离 (如"烧烤" vs "烧拷");
3. 包含关系 (如"火锅" vs "重庆火锅");
4. 向量相似度

</details>

<details><summary><b>2. 候选过滤</b></summary>



</details>


## 背景