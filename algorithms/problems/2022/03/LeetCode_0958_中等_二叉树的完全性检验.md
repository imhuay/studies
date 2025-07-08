## 二叉树的完全性检验
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2025-07-08%2016%3A53%3A13&color=yellowgreen&style=flat-square)
[![](https://img.shields.io/static/v1?label=&message=%E4%B8%AD%E7%AD%89&color=yellow&style=flat-square)](../../../README.md#中等)
[![](https://img.shields.io/static/v1?label=&message=LeetCode&color=green&style=flat-square)](../../../README.md#leetcode)
[![](https://img.shields.io/static/v1?label=&message=%E4%BA%8C%E5%8F%89%E6%A0%91/%E6%A0%91&color=blue&style=flat-square)](../../../README.md#二叉树树)
[![](https://img.shields.io/static/v1?label=&message=%E7%BB%8F%E5%85%B8&color=blue&style=flat-square)](../../../README.md#经典)

<!--END_SECTION:badge-->
<!--info
tags: [二叉树, 经典]
source: LeetCode
level: 中等
number: '0958'
name: 二叉树的完全性检验
companies: []
-->

<summary><b>问题简述</b></summary>

```txt
给定一个二叉树的 root ，确定它是否是一个 完全二叉树 。
```
> [958. 二叉树的完全性检验 - 力扣（LeetCode）](https://leetcode-cn.com/problems/check-completeness-of-a-binary-tree/)

<!-- 
<details><summary><b>详细描述</b></summary>

```txt
```

</details>
-->


<!-- <div align="center"><img src="../../../_assets/xxx.png" height="300" /></div> -->

<summary><b>思路1：利用完全二叉树定义</b></summary>

- 判断完全二叉树的条件：
    - 左右子树都是满二叉树，且高度相同（满二叉树）；
    - 左右子树都是满二叉树，且左子树的高度+1；
    - 左子树是满二叉树，右子树是完全二叉树，且高度相同；
    - 左子树是完全二叉树，右子树是满二叉树，且左子树的高度+1；
- 综上：
    - 我们需要存储信息有：高度、是否满二叉树、是否完全二叉树；
    - 对空节点，初始化为：0、是、是；

<details><summary><b>Python：后序遍历</b></summary>

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def isCompleteTree(self, root: TreeNode) -> bool:

        from dataclasses import dataclass

        @dataclass
        class Info:
            height: int     # 树的高度
            is_full: bool   # 是否满二叉树
            is_cbt: bool    # 是否完全二叉树
        
        def dfs(x):
            if not x: return Info(0, True, True)

            l, r = dfs(x.left), dfs(x.right)

            # 利用左右子树的info 构建当前节点的info
            height = max(l.height, r.height) + 1
            is_full = l.is_full and r.is_full and l.height == r.height
            is_cbt = is_full \
                or l.is_full and r.is_full and l.height - 1 == r.height \
                or l.is_full and r.is_cbt and l.height == r.height \
                or l.is_cbt and r.is_full and l.height - 1 == r.height
            
            return Info(height, is_full, is_cbt)
        
        return dfs(root).is_cbt
```

</details>

<summary><b>思路2：利用完全二叉树的节点数性质</b></summary>

- 给每个节点标号，如果是完全二叉树，存在以下性质：
    - 记根节点 `id` 为 `1`；
    - 若父节点的 `id` 为 `i`，则其左右子节点分别为 `2*i` 和 `2*i + 1`；
    - 如果是完全二叉树则有最大的 `id == n`，其中 `n` 为总节点数； 

<details><summary><b>Python 写法1：DFS：前序+后序遍历</b></summary>

```python
class Solution:
    def isCompleteTree(self, root: TreeNode) -> bool:

        from dataclasses import dataclass

        @dataclass
        class Info:
            n: int        # 总节点数
            mx_id: int    # 最大 id
            is_cbt: bool  # 是否完全二叉树
        
        def dfs(x, i):
            if not x: return Info(0, float('-inf'), True)

            # 前序遍历向下传递 id
            l, r = dfs(x.left, i * 2), dfs(x.right, i * 2 + 1)

            # 后序遍历计算是否完全二叉树
            n = l.n + r.n + 1
            mx_id = max(i, l.mx_id, r.mx_id)
            is_cbt = n == mx_id  # and l.is_cbt and r.is_cbt
            return Info(n, mx_id, is_cbt)
        
        return dfs(root, 1).is_cbt
```

</details>

<details><summary><b>Python 写法2：BFS</b></summary>

```python
class Solution:
    def isCompleteTree(self, root: TreeNode) -> bool:
        # if not root: return True

        from collections import deque

        q = deque()
        q.append([root, 1])
        n = 1       # 记录节点数
        mx_id = 1   # 记录最大 id
        while q:
            node, id_ = q.popleft()
            if node.left:
                n += 1
                q.append([node.left, id_ * 2])
            if node.right:
                n += 1
                q.append([node.right, id_ * 2 + 1])
            mx_id = id_  # max(mx_id, id_)
        return n == mx_id
```

</details>