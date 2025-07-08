## 路径总和II
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
number: '0113'
name: 路径总和II
companies: []
-->

<summary><b>问题简述</b></summary>

```txt
给你二叉树的根节点 root 和一个整数目标和 targetSum ，找出所有 从根节点到叶子节点 路径总和等于给定目标和的路径。

叶子节点 是指没有子节点的节点。
```
> [113. 路径总和 II - 力扣（LeetCode）](https://leetcode-cn.com/problems/path-sum-ii/)

<!-- 
<details><summary><b>详细描述</b></summary>

```txt
```

</details>
-->


<!-- <div align="center"><img src="../../../_assets/xxx.png" height="300" /></div> -->

<summary><b>思路</b></summary>

- 先序遍历+回溯；

<details><summary><b>Python</b></summary>

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def pathSum(self, root: Optional[TreeNode], targetSum: int) -> List[List[int]]:
        
        ret = []
        tmp = []

        def dfs(x, rest):
            if not x:
                return 
            
            rest -= x.val
            tmp.append(x.val)
            if not x.left and not x.right:
                if rest == 0:
                    ret.append(tmp[:])
                
            dfs(x.left, rest)
            dfs(x.right, rest)
            rest += x.val
            tmp.pop()
        
        dfs(root, targetSum)
        return ret
```

</details>

