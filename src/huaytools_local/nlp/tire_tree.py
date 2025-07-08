#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Time:
    2022-08-03 10:59
Author:
    HuaYang (imhuay@163.com)
Subject:
    A simple implementation of TireTree (字典树、前缀树)
References:
    [字典树的Python实现 - 知乎](https://zhuanlan.zhihu.com/p/335793141)
"""
import os
import sys
import json
import time

from typing import *
from pathlib import Path
from collections import defaultdict

_KT = TypeVar('KT')
_VT = TypeVar('VT')


class TireNode:
    """"""
    key: _KT
    value: _VT
    nodes: Dict[_KT, 'TireNode']
    is_end: bool
    count: int

    def __init__(self, key: _KT, value: _VT = None):
        """"""
        self.key = key
        self.value = value
        self.nodes = dict()
        self.is_end = False
        self.count = 0

    @property
    def nodes_count(self) -> int:
        return len(self.nodes)


class TireTree(TireNode):
    """"""
    # info field name
    F_SEQ = 'seq'  # 至当前节点的序列，下简称序列
    F_IS_END = 'is_end'  # 序列是否是一个完整的序列
    F_COUNT = 'count'  # 序列在语料中出现的计数
    F_SUB_NODE_COUNT = 'sub_node_count'  # 直接子节点的计数
    F_ALL_SUB_NODE_COUNT = 'all_sub_node_count'  # 全部子节点的计数

    _default_info = {
        F_SEQ: tuple(),
        F_IS_END: False,
        F_COUNT: 0,
        F_SUB_NODE_COUNT: 0,
        F_ALL_SUB_NODE_COUNT: 0,
    }

    # 遍历结果
    _traversal: List = None

    # 更新状态
    _updated: bool = False

    def __init__(self):
        super().__init__(key=None)

    def insert(self, seq: Sequence[_KT], value: _VT = None):
        """"""
        if not seq:
            return

        self._updated = True

        cur = self
        for it in seq:
            if not cur.nodes.get(it, None):
                node = TireNode(it)
                cur.nodes[it] = node
            cur = cur.nodes[it]

        cur.is_end = True
        cur.value = value
        cur.count += 1

    def search(self, seq: Sequence):
        """"""
        cur = self
        for p in seq:
            cur = cur.nodes.get(p, None)
            if cur is None:
                return False
        return cur.is_end

    def find_all_subseq(self, seq: Sequence, flatten=True) -> List[List]:
        """找出所有完整的子串"""
        ret = []
        for start_idx in range(len(seq)):
            sub_ret = []
            cur = self
            seq_suf = seq[start_idx:]
            for i, p in enumerate(seq_suf):
                cur: TireNode = cur.nodes.get(p, None)
                if cur is None:
                    break
                if cur.is_end:
                    sub_ret.append(tuple(seq_suf[:i + 1]))

            if sub_ret:
                ret.append(sub_ret)

        if flatten:
            new_ret = []
            for sub_ret in ret:
                new_ret += sub_ret
            ret = sorted(set(new_ret), key=new_ret.index)

        return ret

    @property
    def traversal(self) -> List[Dict]:
        """遍历所有节点，记录相关信息"""
        if self._traversal is None or self._updated:
            self._traversal = self._traverse()
        self._updated = False
        return self._traversal

    def _traverse(self):
        _traversal = []

        def dfs(node: TireNode, seq: List):
            if not node:
                return self._default_info

            info = self._default_info.copy()
            _traversal.append(info)

            info[TireTree.F_COUNT] = node.count
            info[TireTree.F_IS_END] = node.is_end
            info[TireTree.F_SUB_NODE_COUNT] = len(node.nodes)
            info[TireTree.F_ALL_SUB_NODE_COUNT] = len(node.nodes)

            for k, v in node.nodes.items():
                seq.append(v.key)
                sub_info = dfs(v, seq)
                sub_info[TireTree.F_SEQ] = tuple(seq)
                info[TireTree.F_ALL_SUB_NODE_COUNT] += sub_info[TireTree.F_ALL_SUB_NODE_COUNT]
                seq.pop()

            return info

        dfs(self, [])
        return _traversal


class __Test:
    """"""

    def __init__(self):
        """"""
        phrases = ['a b', 'a b c', 'a b d', 'a b c',
                   'apple', 'apple inc',
                   'nlp',
                   'machine', 'machine learning', 'machine learning', 'machine learning system',
                   'machine system']
        tire = TireTree()
        for p in phrases:
            tokens = p.split()
            tire.insert(tokens)

        self.tire = tire

        # try:
        #     from huaytools.utils import cprint
        # except ImportError:
        #     cprint = print

        for k, v in self.__class__.__dict__.items():
            if k.startswith('_test') and isinstance(v, Callable):
                print(f'\x1b[32m=== Start "{k}" {{\x1b[0m')
                start = time.time()
                v(self)
                print(f'\x1b[32m}} End "{k}" - Spend {time.time() - start:f}s===\x1b[0m\n')

    def _test_doctest(self):  # noqa
        """"""
        import doctest
        doctest.testmod()

    def _test_find_all_subseq(self):  # noqa
        """"""
        tire = self.tire
        assert tire.search('apple inc'.split())

        txt = "I'm studying machine learning ."
        ret = tire.find_all_subseq(txt.split())
        print(ret)

    def _test_traversal(self):
        """"""
        for it in self.tire.traversal:
            print(it)


if __name__ == '__main__':
    """"""
    __Test()
