电商领域的 NER
===
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2025-07-08%2016%3A53%3A13&color=yellowgreen&style=flat-square)

<!--END_SECTION:badge-->
<!--info
top: false
hidden: false
-->

> 关键词: e-commerce, named entity recognition (ner), query understanding

<!-- TOC -->
- [概述](#概述)
    - [NER 的作用](#ner-的作用)
    - [难点与挑战](#难点与挑战)
    - [传统方法](#传统方法)
- [相关论文](#相关论文)
- [参考资料](#参考资料)
<!-- TOC -->


## 概述
> [^1]

### NER 的作用
- 电商领域有丰富的实体类型和关系, 而这也会反映在用户的搜索 query 上 (品牌, 产品, 属性等);
- 为了理解用户的搜索意图, NER 是一个必要的查询理解 (query understanding) 步骤;

### 难点与挑战
- 不规范的 query;
- 复杂的标签类型, 大量标注数据需求;
- 实时要求;

### 传统方法
- 词表 + 最长匹配;
- 存在的问题: 1) 歧义; 2) OOV;
    ```text
    以下假设 品牌 的优先级高于 产品
    query: weed eater light weight
        pred: weed eater (brand, 一种户外品牌), light (product, 灯)
        true: weed eater (product, 除草剂)
        说明: "weed eater" 既可以是品牌, 也可以是产品;
    query: fridge no ice maker
        pred: ice maker (product, 制冰机)
        true: fridge (product, 冰箱)
        说明: query 中存在两个产品, 根据最长原则标记了错误的产品;
    query: cosco table and chair set
        pred: cosco (brand), table (product)
        true: cosco (brand), table and chair set (product)
        说明: "table and chair set" 不在预定义词表中;
    ``` 


## 相关论文
- Bhange, Bhushan Ramesh, et al. "Named Entity Recognition for E-Commerce Search Queries." (2020).
- Zhang, Hanchu, et al. "Bootstrapping named entity recognition in e-commerce with positive unlabeled learning." arXiv preprint arXiv:2005.11075 (2020).


## 参考资料

[^1]: Bhange, Bhushan Ramesh, et al. "Named Entity Recognition for E-Commerce Search Queries." (2020).