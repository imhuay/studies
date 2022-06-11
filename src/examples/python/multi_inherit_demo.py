#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Time:
    2021-02-26 17:17
    
Author:
    huayang
    
Subject:


Notes:
    现象：
        class C(A, B)
        C类 继承了 A 和 B，
        在此之前，A 和 B 没有任何关系
        但在 C 同时继承了 A 和 B 后，A 就能调用 B 中的代码

    说明：
        1. 先继承 B，此时可以访问 B 的所有成员；
        2. 然后继承 A，如果 A 中存在与 B 同名的方法，则会覆盖；
        3. 实际上不是 A 能访问 B，而是 A 中被 C 继承后的方法能访问 B；

    属于 python（解释型语言）独有的特性

    可以看作是某种形式的装饰器，优点是灵活，缺点是可读性（pycharm 中不支持相关跳转，应该不是 python 推荐的写法）
"""


class A:

    def __init__(self, a='A', *args, **kwargs):
        """"""
        print(a)

        self.func()  # B 中的方法


class B:

    def __init__(self, b='B', *args, **kwargs):
        print(b)

    def func(self):
        print('B_func')


class C(A, B):
    """
    C类 继承了 A 和 B
    A类 和 B类 没有继承关系，但是 A 却能调用 B 中的代码
    """

    def __init__(self):
        super().__init__()


class D(B, A):  # 与 C 相比，交换了 继承 A、B 的顺序
    """"""

    def __init__(self):
        super().__init__()


if __name__ == '__main__':
    # print(C.__mro__)
    # a = A()  # err，不能单独实例化 A

    c = C()  # class C(A, B)
    """输出
    A
    B_func
    """

    d = D()  # class D(B, A)
    """输出
    B
    """
