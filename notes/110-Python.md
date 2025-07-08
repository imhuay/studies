Python
===
<!--info
toc_id: python
-->

<!-- TOC -->
- [标准库](#标准库)
    - [容器的抽象基类](#容器的抽象基类)
    - [数据类](#数据类)
    - [装饰器](#装饰器)
    - [杂项](#杂项)
- [设计模式](#设计模式)
- [备忘](#备忘)
    - [第三方库](#第三方库)
<!-- TOC -->

## 标准库
> [Python 标准库 — Python 文档](https://docs.python.org/zh-cn/3/library/index.html)

### 容器的抽象基类
> [容器的抽象基类 (`collections.abc`) — Python 文档](https://docs.python.org/zh-cn/3/library/collections.abc.html#collections-abstract-base-classes)  

- 快速查询容器之间的继承关系，以及包含的抽象方法；
- **使用场景**：type hints、`isinstance()`、`issubclass()` 等；
    > 详见：[容器基类的使用](./_archives/2022/08/Python容器基类的使用.md)

### 数据类
- [数据类 `dataclass` 使用记录](./_archives/2022/09/python-dataclass使用记录.md)

### 装饰器
- [装饰器的本质](./_archives/2022/05/python装饰器的本质.md)

### 杂项
- [class method 中 `self` 的含义](./_archives/2022/06/python类方法中self的含义.md)
- [Python 函数声明中单独的正斜杠（/）和星号（*）是什么作用](./_archives/2022/07/python函数声明中单独的正斜杠和星号是什么意思.md)
- [类变量、成员变量，与注解](./_archives/2022/07/python类变量和成员变量的最佳实践)


## 设计模式
> [Python 设计模式](_archives/2022/09/设计模式.md)

## 备忘
- [requirements.txt 语法备忘](./_archives/2022/09/python-requirements语法.md)
- [Pycharm 常用配置](./_archives/2022/07/PyCharm常用配置.md)
    - [常用插件列表](./_archives/2022/07/PyCharm常用配置.md#常用插件)
- [pip & conda 国内镜像](./_archives/2022/06/python国内镜像源.md)
- [Python 标准项目结构]()
    - TODO

### 第三方库

- [PyGitHub](./_archives/2022/10/PyGithubExample.ipynb)

<!-- omit in toc -->
## FAQ

- `conda install` 报 `Solving environment: failed`
    ```shell
    $ conda config --set channel_priority flexible
    ```

<!-- omit in toc -->
## 学习资料
- [Python 的好习惯与最佳实践 - 肥清哥哥的个人空间_bilibili](https://space.bilibili.com/374243420/channel/collectiondetail?sid=422655)
- [不基础的python基础 - 码农高天的个人空间_bilibili](https://space.bilibili.com/245645656/channel/collectiondetail?sid=346060)