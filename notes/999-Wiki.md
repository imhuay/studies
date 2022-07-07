Wiki
===
- [D](#d)
    - [DCL](#dcl)
    - [DDL](#ddl)
    - [DML](#dml)
- [G](#g)
    - [git](#git)
    - [GitBook (1)](#gitbook-1)
    - [GitBook (2)](#gitbook-2)
- [H](#h)
    - [Hive](#hive)
- [L](#l)
    - [LaTeX](#latex)
    - [领域短语挖掘](#领域短语挖掘)
- [M](#m)
    - [Markdown](#markdown)
- [O](#o)
    - [Obsidian](#obsidian)
- [S](#s)
    - [Scheduler (Spark)](#scheduler-spark)
- [T](#t)
    - [TCL](#tcl)


## D

### DCL
> 另见：DDL，DML，TCL
- Data Control Language，数据库控制语言；
- 基本命令：`GRANT, REVOKE` 等；

### DDL
> 另见：DCL，DML，TCL
- Data Definition Language，数据库定义语言，SQL 语言的四大功能之一；
- 基本命令：`CREATE, ALTER, DROP` 等；

### DML
> 另见：DCL，DDL，TCL
- Data Manipulation Language，数据操纵语言
- 基本命令：`SELECT, INSERT, UPDATE, DELETE` 等；


## G

### git
> 一个开源的分布式版本控制系统，可以有效地进行项目版本管理。
- [`git` 的常用命令](./_archives/2022/06/git.md)
    - [`git-subtree` 的基本用法](./_archives/2022/06/git-subtree的基本用法.md)

### GitBook (1)
> 一款现代化的文档平台，常用于编辑产品文档、知识分享、个人笔记等，支持与 GitHub 自动同步；  
- 官网网址：[GitBook - Where software teams break knowledge silos.](https://www.gitbook.com/)
- 本项目的 GitBook 地址：[studies-gitbook](https://imhuay.gitbook.io/studies)


### GitBook (2)
> 一个基于 Node.js 的命令行工具，使用 Markdown 快速构建文档或书籍；  
> 目前团队已不再维护，转向 [GitBook 在线平台](#gitbook-1)
- 官方 GitHub 地址（已不再维护）：[GitbookIO/gitbook](https://github.com/GitbookIO/gitbook)
- [GitBook 使用记录](./_archives/2022/04/Gitbook.md)
    > 对 markdown 和 html 混写支持不佳，已不再使用


## H

### Hive
> 一款基于 Hadoop 的数据仓库工具，Hive 能够将结构化的数据文件映射为一张数据库表，并提供 SQL 查询功能；
- [Hive SQL 常用操作](./_archives/2022/04/HiveSQL常用操作.md)


## L

### LaTeX
> 一种可以处理排版和渲染的标记语言，常用于论文编辑；
- [LaTeX 常用编辑格式](./_archives/2022/04/LaTeX备忘.md)；

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


## O

### Obsidian
> 一款流行的 Markdown 笔记软件；
- [Obsidian 使用记录](./_archives/2022/05/Obsidian.md)


## S

### Scheduler (Spark)
- 调度器，用于控制例行化调度、依赖检测等功能；


## T

### TCL
> 另见：DCL，DDL，DML
- Transaction Control Language，事务控制语言；
- 基本命令：`SAVEPOINT, ROLLBACK` 等；
