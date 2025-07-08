## 验证二叉搜索树
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2025-07-08%2016%3A53%3A13&color=yellowgreen&style=flat-square)
[![](https://img.shields.io/static/v1?label=&message=%E4%B8%AD%E7%AD%89&color=yellow&style=flat-square)](../../../README.md#中等)
[![](https://img.shields.io/static/v1?label=&message=LeetCode&color=green&style=flat-square)](../../../README.md#leetcode)
[![](https://img.shields.io/static/v1?label=&message=%E4%BA%8C%E5%8F%89%E6%A0%91/%E6%A0%91&color=blue&style=flat-square)](../../../README.md#二叉树树)

<!--END_SECTION:badge-->
<!--info
tags: [二叉树]
source: LeetCode
level: 中等
number: '0098'
name: 验证二叉搜索树
companies: []
-->

<summary><b>问题简述</b></summary>

```txt
给你一个二叉树的根节点 root ，判断其是否是一个有效的二叉搜索树。
```
> [98. 验证二叉搜索树 - 力扣（LeetCode）](https://leetcode-cn.com/problems/validate-binary-search-tree/)

<!-- 
<details><summary><b>详细描述</b></summary>

```txt
```

</details>
-->


<!-- <div align="center"><img src="../../../_assets/xxx.png" height="300" /></div> -->

<summary><b>思路</b></summary>

- 判断二叉搜索树的条件：
    - 当前节点的值大于左树的最大值，小于右树的最小值，且**左右子树都是二叉搜索树**；

<details><summary><b>Python</b></summary>

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def isValidBST(self, root: TreeNode) -> bool:

        from dataclasses import dataclass

        @dataclass
        class Info:
            mx: int
            mi: int
            is_bst: bool

        def dfs(x):
            if not x: return Info(float('-inf'), float('inf'), True)

            l, r = dfs(x.left), dfs(x.right)

            mx = max(x.val, r.mx)
            mi = min(x.val, l.mi)
            is_bst = l.is_bst and r.is_bst and l.mx < x.val < r.mi

            return Info(mx, mi, is_bst)

        return dfs(root).is_bst
```

</details>

