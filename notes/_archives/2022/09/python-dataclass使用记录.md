`dataclass` 使用记录
===
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2022-10-13%2001%3A56%3A19&color=yellowgreen&style=flat-square)

<!--END_SECTION:badge-->


## 基础
- `dataclass` 是对数据的模板化封装，类比 C/C++ 中的 `stuct`；
- 基本用法：
    ```python
    from dataclasses import dataclass

    @dataclass
    class Foo:
        a: int
        b: str = 'B'  # 默认值
    
    f1 = Foo(1)
    f2 = Foo(2, 'b')
    ```
- Python 3.7 开始加入标准库，3.7 之前需要安装外部依赖；
    ```
    # requirements.txt
    dataclasses; python_version < '3.7'
    ```


## 进阶
> 参考：[Python 最佳实践（数据类专题） - 肥清哥哥](https://space.bilibili.com/374243420/channel/collectiondetail?sid=422655)

