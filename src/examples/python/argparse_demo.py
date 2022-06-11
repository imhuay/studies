#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Time:
    2021-01-18 19:20
    
Author:
    huayang
    
Subject:
    argparse usage demo

References:
    https://docs.python.org/zh-cn/3/library/argparse.html#the-add-argument-method
"""
import argparse


def get_args(test_arg_ls: list = None):
    """
    主要是 `.add_argument()` 方法的使用：
        .add_argument(
            name or flags...    # 参数名，带 '-' 前缀的为关键字参数，不带为位置参数
            [, action]          # 当参数在命令行中出现时使用的动作基本类型，默认 `store`，满足绝大多数情况，其他 action 详见文档
            [, nargs]           # 命令行参数应当消耗的数目
            [, const]           # 被一些 action 和 nargs 选择所需求的常数
            [, default]         # 参数的默认值
            [, type]            # 参数会被转换成的类型
            [, choices]         # 该选项的值应当从一组受限值中选择
            [, required]        # 该命令行选项是否可省略
            [, help]            # 该选项作用的描述
            [, metavar]         # 在使用方法消息中使用的参数值示例
            [, dest]            # 被添加到 parse_args() 所返回对象上的属性名
        )
    """
    p = argparse.ArgumentParser(description='argparse demo')

    # 位置参数
    p.add_argument(
        'foo',
        # required=True,  # 位置参数默认且只能是必需的
        type=str,
        help='示例参数1：foo，这是一个位置参数',
    )

    # 关键词参数
    p.add_argument(
        '--bar', '-b',  # 一个全称，一个简称
        required=True,  # 该关键词参数是必须的
        type=int,       # 传入值会转换成 int 类型
        choices={1, 2, 3},  # 该选项的值必须是 {1,2,3} 之一
        help='示例参数2：bar，这是一个关键词参数，且是必须的',
    )

    # store_const 行为的参数
    p.add_argument(
        '--ccc',
        action='store_const',   # 如果在命令行中出现这个选项，则 ccc=CCC，否则为 ccc=None
        const='CCC',            # 该选项的默认值为 'CCC'，可以通过 args.ccc = 'XXX' 来修改
        help='示例参数3：这是一个 store_const 行为的参数',
    )

    # bool 类型的参数
    p.add_argument(
        '--ddd',
        action='store_false',    # 如果在命令行中出现这个选项则 ddd=False，否则默认为 ddd=True
        help='这是一个 bool 类型的参数，',
    )

    args = p.parse_args(test_arg_ls)

    return args


if __name__ == '__main__':
    """
    python argparse_demo.py FOO --bar 2 --ccc --ddd
    """
    # 模拟命令行参数
    test_arg_ls = 'FOO --bar 2 --ccc --ddd'.split(' ')
    args = get_args(test_arg_ls)
    args.some_new = 1  # 可以直接加新的参数
    for k, v in args.__dict__.items():
        print(k, v)
    """
    foo FOO
    bar 2
    ccc CCC
    ddd False
    """

    print()
    test_arg_ls = 'FOO --bar 2 --ccc'.split(' ')
    args = get_args(test_arg_ls)
    args.ccc = 'XXX'
    for k, v in args.__dict__.items():
        print(k, v)
    """
    foo FOO
    bar 2
    ccc XXX
    ddd True
    """

    print()
    test_arg_ls = 'FOO --bar 2'.split(' ')
    args = get_args(test_arg_ls)
    for k, v in args.__dict__.items():
        print(k, v)
    """
    foo FOO
    bar 2
    ccc None
    ddd True
    """
