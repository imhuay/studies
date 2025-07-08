Wiki
===
<!--info
toc_id: wiki
-->

<!-- TOC -->
- [C](#c)
    - [C++](#c-1)
- [D](#d)
    - [Docker](#docker)
- [G](#g)
    - [git](#git)
    - [gitbook](#gitbook)
        - [(1)](#1)
        - [(2)](#2)
    - [GitHub Action](#github-action)
    - [glob](#glob)
- [H](#h)
    - [Hive](#hive)
    - [HuggingFace](#huggingface)
- [J](#j)
    - [Jupyter](#jupyter)
        - [Jupyter Lab](#jupyter-lab)
        - [IPython](#ipython)
- [K](#k)
    - [开发环境](#开发环境)
        - [Mac](#mac)
        - [深度学习](#深度学习)
- [L](#l)
    - [LaTeX](#latex)
    - [LLM](#llm)
    - [领域短语挖掘](#领域短语挖掘)
- [M](#m)
    - [Markdown](#markdown)
- [N](#n)
    - [NLP](#nlp)
    - [Node.js](#nodejs)
- [O](#o)
    - [Obsidian](#obsidian)
- [P](#p)
    - [PyCharm](#pycharm)
    - [PySpark](#pyspark)
    - [Python](#python)
- [Q](#q)
    - [Query 理解](#query-理解)
- [S](#s)
    - [SQL](#sql)
    - [STAR 法则](#star-法则)
- [T](#t)
    - [Transformer 模型](#transformer-模型)
- [W](#w)
    - [Windows](#windows)
    - [WSL](#wsl)
- [Y](#y)
    - [yaml](#yaml)
    - [语言模型](#语言模型)
<!-- TOC -->


## C

### C++
> C++ 是一种计算机高级程序设计语言

- [C++]()

## D

### Docker
> 一个开源的应用容器引擎，让开发者可以打包他们的应用及依赖到一个可移植的镜像中；
- [Docker 学习笔记](./_archives/2022/08/Docker学习笔记.md)


## G

### git
> 一个开源的分布式版本控制系统，可以有效地进行项目版本管理。
- [`git` 常用命令](./_archives/2022/06/git.md)
    - [`git-subtree` 的基本用法](./_archives/2022/06/git-subtree的基本用法.md)

### gitbook

#### (1)
> 一款现代化的文档平台，常用于编辑产品文档、知识分享、个人笔记等，支持与 GitHub 自动同步；  
- 官网网址：[GitBook - Where software teams break knowledge silos.](https://www.gitbook.com)
- 本项目的 GitBook 地址：[studies-gitbook](https://imhuay.gitbook.io/studies)


#### (2)
> 一个基于 Node.js 的命令行工具，使用 Markdown 快速构建文档或书籍；  
> 目前团队已不再维护，转向 GitBook 在线平台
- 官方 GitHub 地址（已不再维护）：[GitbookIO/gitbook](https://github.com/GitbookIO/gitbook)
- [GitBook 使用记录](./_archives/2022/04/Gitbook.md)
    > 对 markdown 和 html 混写支持不佳，已不再使用


### GitHub Action
> GitHub Action 是一个由 Github 提供的自动化工具。具体的执行的操作由仓库中的 YAML 文件定义（位于 `.github/workflows` 目录下），并在相应事件触发时运行，也可以手动触发，或按定义的时间表触发。
- [Github Action 使用备忘](./_archives/2022/08/GithubAction备忘.md)

### glob
> 一种在 shell 中使用的简化版正则表达式
- [glob 语法备忘](./_archives/2022/08/glob语法备忘.md)


## H

### Hive
> 一款基于 Hadoop 的数据仓库工具，Hive 能够将结构化的数据文件映射为一张数据库表，并提供 SQL 查询功能；
- [Hive SQL 常用操作](./_archives/2022/04/HiveSQL常用操作.md)
- [Hive 常用 SQL 备忘](./_archives/2023/03/Hive常用SQL备忘.md)

### HuggingFace
> 一家 AI 创业公司, 创建了目前最流行的预训练模型库 [transformers](https://github.com/huggingface/transformers);

- [huggingface 套件使用备忘](./_archives/2023/06/huggingface套件使用备忘.md)


## J

### Jupyter
> 一款支持交互式编程的笔记软件, 此前被称为 IPython notebook; 目前除了支持 Python 外, 也开始支持其他语言;

#### Jupyter Lab
> Jupyter 开发的新一代 notebook 界面, 支持目录, 插件等更多高级功能; 

#### IPython
> Jupyter 的前身; 自 IPython 4.x 开始, 与语言无关的部分迁移至 Jupyter 项目, IPython 本身则专注于交互式 Python;

- [Jupyter & IPython 使用备忘](./_archives/2022/12/jupyter与ipython备忘.md)

## K

### 开发环境

#### Mac
> [Mac 环境配置](./_archives/2022/07/Mac环境配置.md)

#### 深度学习
> [深度学习环境配置](./_archives/2022/07/深度学习环境配置.md)


## L

### LaTeX
> 一种可以处理排版和渲染的标记语言，常用于论文编辑；
- [LaTeX 常用编辑格式](./_archives/2022/04/LaTeX备忘.md)；

### LLM
> 大型语言模型 (Large Language Model, LLM)
- [LLM 训练方案整理](./_archives/2023/06/llm训练方案整理.md)
- [LLM 应用收集](./_archives/2023/06/llm应用收集.md)

### 领域短语挖掘
> 同义：短语挖掘（Phrase Mining）<br/>
> 另见：“关键词挖掘”，“新词发现”，“LDA 主题模型”
- **领域短语挖掘**，指从给定领域语料（将大量的文档融合在一起组成一个语料）中自动挖掘该领域内高质量短语的过程。
- 一般挖掘过程：候选短语生成 -> 统计特征计算 -> 质量评分/排序
- 与**关键词抽取**的区别：关键词抽取是从语料中抽取最重要、最有代表性的短语，其抽取的短语数量一般比较小。
- 与**新词发现**的区别：新词发现的主要目标是发现词汇库中不存在的新词，而领域短语挖掘不区分新旧短语。新词发现可以通过在领域短语挖掘的基础上进一步过滤已有词汇来实现。
- 参考
    - [第3章：词汇挖掘与实体识别——《知识图谱概念与技术》肖仰华_fufu_good的博客-CSDN博客](https://blog.csdn.net/fufu_good/article/details/104216156)
    - [NLP必备：领域短语挖掘中的质量评估、常用算法解读与开源实现 - 墨天轮](https://www.modb.pro/db/379555)


## M

### Markdown
> Markdown 是一种轻量级标记语言，可以使用纯文本格式来编写文档，然后通过转化为 HTML 来丰富可读性，并在一定程度上兼容 HTML 代码；  
> 另见：[Obsidian](#obsidian)
- [Markdown 常用编辑格式](./_archives/2022/04/Markdown.md)
- [使用 Markdown 编辑简历](./_archives/2022/06/Markdown简历工具.md)


## N

### NLP
> 自然语言处理 (Natural Language Processing, NLP)

- [NLP 领域术语](./_archives/2022/12/nlp_wiki.md)

### Node.js
> Node.js® is an open-source, cross-platform JavaScript runtime environment.
>> [Node.js](https://nodejs.org/en/)

- [Node.js 环境搭建](./_archives/2022/12/nodejs环境.md)

## O

### Obsidian
> 一款流行的 Markdown 笔记软件;
- [Obsidian 使用记录](./_archives/2022/05/Obsidian.md)


## P

### PyCharm
> JetBrains 公司开发的一款 Python IDE;

- [PyCharm 常用配置](./_archives/2022/07/PyCharm常用配置.md)

### PySpark
> Spark 为 Python 开发者提供的 API;

- [PySpark 笔记 & 备忘](./_archives/2023/01/PySpark笔记.md)

### Python
> 流行的编程语言

- [python 国内镜像源](./_archives/2022/06/python国内镜像源.md)


## Q

### Query 理解
> Query 理解 (QU，Query Understanding), 简单来说就是从词法、句法、语义三个层面对 query 进行结构化解析;
>> [搜索中的 Query 理解及应用_夕小瑶的博客-CSDN博客_query理解](https://blog.csdn.net/xixiaoyaoww/article/details/106205415)

- [Query 理解相关阅读](./_archives/2022/12/query理解相关阅读.md)

## S

<!-- ### Scheduler (Spark)
- 调度器，用于控制例行化调度、依赖检测等功能； -->

### SQL
> SQL (Structured Query Language) 是具有数据操纵和数据定义等多种功能的数据库语言;

- [Hive/Spark/Presto SQL 备忘](./_archives/2023/01/大数据SQL备忘.md)
- SQL 优化
    - [暴力扫描](./_archives/2023/02/SQL优化之暴力扫描.md)

### STAR 法则
> STAR 法则是一种用于描述事件的方式, STAR 分别表示情境 (Situation)、任务 (Task)、行动 (Action)、结果 (Result) 四项的缩写;
>> [STAR法则_百度百科](https://baike.baidu.com/item/STAR%E6%B3%95%E5%88%99/9056070)

- [使用 STAR 法则描述简历](./_archives/2022/10/简历技巧.md#star-法则)


## T

### Transformer 模型
> 一种流行的深度学习模型;

> ***Keywords**: transformer, bert*

- [Transformers Wiki](./_archives/2022/05/TransformerWiki.md)
    - [Transformer 常见问题](./_archives/2022/05/Transformer常见问题.md)
    - [Transformer 的优势与劣势](./_archives/2023/02/Transformer的优势与劣势.md)
    - ...

## W

### Windows
> 微软以图形用户界面为基础研发的操作系统

- [Windows 使用备忘](./_archives/2023/01/Windows备忘.md)

### WSL
> Windows Subsystem for Linux, WSL

- [WSL 使用记录](./_archives/2022/09/WSL使用记录.md)

## Y

### yaml
> 一个可读性高，用来表达序列化数据的标记语言
- [YAML 入门教程 - 菜鸟教程](https://www.runoob.com/w3cnote/yaml-intro.html)


### 语言模型
> 语言模型指用来计算一个句子 (序列) 出现概率的模型;

- [语言模型基础](./_archives/2022/10/语言模型.md)