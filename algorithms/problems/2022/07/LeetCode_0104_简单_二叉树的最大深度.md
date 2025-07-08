## 二叉树的最大深度
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2025-07-08%2016%3A53%3A13&color=yellowgreen&style=flat-square)
[![](https://img.shields.io/static/v1?label=&message=%E7%AE%80%E5%8D%95&color=yellow&style=flat-square)](../../../README.md#简单)
[![](https://img.shields.io/static/v1?label=&message=LeetCode&color=green&style=flat-square)](../../../README.md#leetcode)
[![](https://img.shields.io/static/v1?label=&message=%E4%BA%8C%E5%8F%89%E6%A0%91/%E6%A0%91&color=blue&style=flat-square)](../../../README.md#二叉树树)
[![](https://img.shields.io/static/v1?label=&message=%E9%80%92%E5%BD%92&color=blue&style=flat-square)](../../../README.md#递归)
[![](https://img.shields.io/static/v1?label=&message=%E7%BB%8F%E5%85%B8&color=blue&style=flat-square)](../../../README.md#经典)

<!--END_SECTION:badge-->
<!--info
tags: [二叉树, 递归, 经典]
source: LeetCode
level: 简单
number: '0104'
name: 二叉树的最大深度
companies: []
-->

<summary><b>问题描述</b></summary>

```txt
给定一个二叉树，找出其最大深度。

二叉树的深度为根节点到最远叶子节点的最长路径上的节点数。

示例：
    给定二叉树 [3,9,20,null,null,15,7]，
        3
       / \
      9  20
        /  \
       15   7
    返回它的最大深度 3 。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/maximum-depth-of-binary-tree
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```

<summary><b>思路</b></summary>

- 递归：当前二叉树的最大深度等于**左右子树的最大深度** `+ 1`

<details><summary><b>Python</b></summary>

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

class Solution:
    def maxDepth(self, root: TreeNode) -> int:
        if not root:  # 尾递归
            return 0
        
        return max(self.maxDepth(root.left), self.maxDepth(root.right)) + 1
```

</details>

