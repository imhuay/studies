## 平衡二叉树
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2025-07-08%2016%3A53%3A13&color=yellowgreen&style=flat-square)
[![](https://img.shields.io/static/v1?label=&message=%E7%AE%80%E5%8D%95&color=yellow&style=flat-square)](../../../README.md#简单)
[![](https://img.shields.io/static/v1?label=&message=LeetCode&color=green&style=flat-square)](../../../README.md#leetcode)
[![](https://img.shields.io/static/v1?label=&message=%E6%A0%91%E5%BD%A2%E9%80%92%E5%BD%92&color=blue&style=flat-square)](../../../README.md#树形递归)
[![](https://img.shields.io/static/v1?label=&message=%E4%BA%8C%E5%8F%89%E6%A0%91/%E6%A0%91&color=blue&style=flat-square)](../../../README.md#二叉树树)
[![](https://img.shields.io/static/v1?label=&message=%E7%83%AD%E9%97%A8&color=blue&style=flat-square)](../../../README.md#热门)

<!--END_SECTION:badge-->
<!--info
tags: [TreeDP, 二叉树, 热门]
source: LeetCode
level: 简单
number: '0110'
name: 平衡二叉树
companies: []
-->

<summary><b>问题简述</b></summary>

```txt
给定一个二叉树，判断它是否是高度平衡的二叉树。
本题中，一棵高度平衡二叉树定义为：
    一个二叉树每个节点 的左右两个子树的高度差的绝对值不超过 1 。
```
> [110. 平衡二叉树 - 力扣（LeetCode）](https://leetcode-cn.com/problems/balanced-binary-tree/)

<!-- 
<details><summary><b>详细描述</b></summary>

```txt
```

</details>
-->


<!-- <div align="center"><img src="../../../_assets/xxx.png" height="300" /></div> -->

<summary><b>思路：树形DP</b></summary>

- 考虑对以 X 为头结点的树，为了确定其是否为平衡二叉树，需要从左右子树获取哪些信息？
- 根据定义，显然需要知道两个信息：
    1. 子树是否为平衡二叉树（`is_balanced: bool`）；
    2. 子树的高度（`height: int`）；
- 假设子树的这些信息已知，怎么求 X 节点的上述信息：
    1. `x_is_balanced = l.is_balanced and r.is_balanced and abs(l.height - r.height) <= 1`
        > 即左右子树都平衡，且高度差小于等于 1
    2. `x_height = max(l.height, r.height) + 1`
- 对空节点，有：
    ```python
    is_balanced = True
    height = 0
    ```

<details><summary><b>Python</b></summary>

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def isBalanced(self, root: TreeNode) -> bool:

        from collections import namedtuple

        # 用一个结构来组织需要的信息，可以直接用 tuple，这里是为了更直观
        Info = namedtuple('Info', ['is_balanced', 'height'])

        def dfs(x):
            if not x:  # 空节点
                return Info(True, 0)
            
            l, r = dfs(x.left), dfs(x.right)
            is_balanced = l.is_balanced and r.is_balanced and abs(l.height - r.height) <= 1
            height = max(l.height, r.height) + 1
            return Info(is_balanced, height)
        
        return dfs(root).is_balanced  # 返回需要的信息
```

</details>

