## 求根节点到叶节点数字之和
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2022-10-14%2014%3A59%3A33&color=yellowgreen&style=flat-square)
[![](https://img.shields.io/static/v1?label=&message=%E4%B8%AD%E7%AD%89&color=yellow&style=flat-square)](../../../README.md#中等)
[![](https://img.shields.io/static/v1?label=&message=LeetCode&color=green&style=flat-square)](../../../README.md#leetcode)
[![](https://img.shields.io/static/v1?label=&message=%E4%BA%8C%E5%8F%89%E6%A0%91/%E6%A0%91&color=blue&style=flat-square)](../../../README.md#二叉树树)

<!--END_SECTION:badge-->
<!--info
tags: [二叉树]
source: LeetCode
level: 中等
number: '0129'
name: 求根节点到叶节点数字之和
companies: []
-->

<summary><b>问题简述</b></summary>

```txt
给你一个二叉树的根节点 root ，树中每个节点都存放有一个 0 到 9 之间的数字。
每条从根节点到叶节点的路径都代表一个数字：

例如，从根节点到叶节点的路径 1 -> 2 -> 3 表示数字 123 。
计算从根节点到叶节点生成的 所有数字之和 。

叶节点 是指没有子节点的节点。
```
> [129. 求根节点到叶节点数字之和 - 力扣（LeetCode）](https://leetcode-cn.com/problems/sum-root-to-leaf-numbers/)

<!-- 
<details><summary><b>详细描述</b></summary>

```txt
```

</details>
-->


<!-- <div align="center"><img src="../../../_assets/xxx.png" height="300" /></div> -->

<summary><b>思路：先序遍历</b></summary>

- 先序遍历，每到一个叶节点，add 一次；
- 注意空节点的处理；

<details><summary><b>Python</b></summary>

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def sumNumbers(self, root: TreeNode) -> int:

        self.ret = 0

        def dfs(x, tmp):
            if not x:
                return

            tmp = tmp * 10 + x.val
            if not x.left and not x.right:
                self.ret += tmp
                return
            
            dfs(x.left, tmp)
            dfs(x.right, tmp)
        
        dfs(root, 0)
        return self.ret
```

</details>

