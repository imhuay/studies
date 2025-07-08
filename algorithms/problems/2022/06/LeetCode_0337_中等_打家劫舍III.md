## 打家劫舍III
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2022-10-16%2016%3A55%3A02&color=yellowgreen&style=flat-square)
[![](https://img.shields.io/static/v1?label=&message=%E4%B8%AD%E7%AD%89&color=yellow&style=flat-square)](../../../README.md#中等)
[![](https://img.shields.io/static/v1?label=&message=LeetCode&color=green&style=flat-square)](../../../README.md#leetcode)
[![](https://img.shields.io/static/v1?label=&message=%E6%A0%91%E5%BD%A2%E9%80%92%E5%BD%92&color=blue&style=flat-square)](../../../README.md#树形递归)

<!--END_SECTION:badge-->
<!--info
tags: [TreeDP]
source: LeetCode
level: 中等
number: '0337'
name: 打家劫舍III
companies: []
-->

<summary><b>问题简述</b></summary>

```txt
小偷又发现了一个新的可行窃的地区。这个地区只有一个入口，我们称之为 root 。

除了 root 之外，每栋房子有且只有一个“父“房子与之相连。一番侦察之后，聪明的小偷意识到“这个地方的所有房屋的排列类似于一棵二叉树”。 如果 两个直接相连的房子在同一天晚上被打劫 ，房屋将自动报警。

给定二叉树的 root 。返回 在不触动警报的情况下 ，小偷能够盗取的最高金额 。
```
> [337. 打家劫舍 III - 力扣（LeetCode）](https://leetcode-cn.com/problems/house-robber-iii/)

<!-- 
<details><summary><b>详细描述</b></summary>

```txt
```

</details>
-->


<!-- <div align="center"><img src="../../../_assets/xxx.png" height="300" /></div> -->

<summary><b>思路：树形 dp + 记忆化搜索</b></summary>

- 树形 dp 问题，就是否抢劫当前节点分两种情况讨论，详见代码；

<details><summary><b>Python</b></summary>

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def rob(self, root: TreeNode) -> int:

        from functools import lru_cache

        @lru_cache(maxsize=None)
        def dfs(x):
            # 空节点
            if not x: return 0
            # 叶节点
            if not x.left and not x.right: return x.val

            # 不抢当前节点
            r1 = dfs(x.left) + dfs(x.right)
            # 抢当前节点
            r2 = x.val
            if x.left:
                r2 += dfs(x.left.left) + dfs(x.left.right)
            if x.right:
                r2 += dfs(x.right.left) + dfs(x.right.right)
            
            return max(r1, r2)
        
        return dfs(root)
```

</details>
