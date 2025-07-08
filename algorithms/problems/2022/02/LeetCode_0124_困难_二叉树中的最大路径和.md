## 二叉树中的最大路径和
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2022-10-14%2014%3A59%3A33&color=yellowgreen&style=flat-square)
[![](https://img.shields.io/static/v1?label=&message=%E5%9B%B0%E9%9A%BE&color=yellow&style=flat-square)](../../../README.md#困难)
[![](https://img.shields.io/static/v1?label=&message=LeetCode&color=green&style=flat-square)](../../../README.md#leetcode)
[![](https://img.shields.io/static/v1?label=&message=%E6%A0%91%E5%BD%A2%E9%80%92%E5%BD%92&color=blue&style=flat-square)](../../../README.md#树形递归)

<!--END_SECTION:badge-->
<!--info
tags: [TreeDP]
source: LeetCode
level: 困难
number: '0124'
name: 二叉树中的最大路径和
companies: []
-->

<summary><b>问题简述</b></summary>

```txt
路径 被定义为一条从树中任意节点出发，沿父节点-子节点连接，达到任意节点的序列。同一个节点在一条路径序列中 至多出现一次 。该路径 至少包含一个 节点，且不一定经过根节点。

路径和 是路径中各节点值的总和。

给你一个二叉树的根节点 root ，返回其 最大路径和 。
```
> [124. 二叉树中的最大路径和 - 力扣（LeetCode）](https://leetcode-cn.com/problems/binary-tree-maximum-path-sum/)

<!-- 
<details><summary><b>详细描述</b></summary>

```txt
```

</details>
-->


<!-- <div align="center"><img src="../../../_assets/xxx.png" height="300" /></div> -->

<summary><b>思路：树形DP</b></summary>

- 考虑对以 X 为头结点的树，为了求得最大路径和，需要从左右子树获取哪些信息？
- 根据要求，显然需要知道：
    1. 子树能提供的最大和路径，即以子树节点为终点的最大路径，记 `h: int`；
        > 为什么需要这个信息：**为了计算经过 X 节点的最大路径**，这条路径的特点是：从某一节点出发到达子树节点，经过 X 节点后，再进入另一个子节点的最大和路径；
        >> 这是本题除 coding 外最大的难点，能想出这个信息也就基本解决这个问题了；
    2. 子树中的最大路径和（即子问题）：为了比较得出全局最大路径和，记 `s: int`；
- 假设子树的这些信息已知，怎么求 X 节点的上述信息：
    1. `x_h = x.val + max(0, l.h, r.h)`
        > 因为需要经过 X 节点，所以必须加上 x.val，同时如果左右子树提供的 h 小于 0，那么不如舍去；
    2. `x_s = max(l.s, r.s, max(l.h, 0) + max(r.h, 0) + x.val)`
        > 这一步容易写成 `x_s = max(l.s, r.s, x_h)` 或者 `x_s = max(l.s, r.s, l.h + r.h + x.val)`，都是对问题理解不到位；
    > 重申：模板只是帮我们解决怎么组织代码的问题，而写出正确的代码一靠观察，二靠积累；
- 对空节点，有：
    ```python
    h = 0
    s = -inf  # 因为题目要求至少包含一个节点，如果设为 0，那么当所有节点为负数时，就会出错
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
    def maxPathSum(self, root: Optional[TreeNode]) -> int:
        
        from dataclasses import dataclass

        @dataclass
        class Info:
            h: int  # 该节点能提供的最大路径（含节点本身）
            s: int  # 该节点下的最大路径（可能不包含该节点）

        # 事实上 Info 里的 s 完全可以用一个全局变量来代替，这里是为了尽量拟合模板；熟练之后就不必这么做了。
        
        def dfs(x):
            if not x:
                # 对空节点，初始化 h=0, s=负无穷
                return Info(0, float('-inf'))
            
            l, r = dfs(x.left), dfs(x.right)
            x_h = x.val + max(0, l.h, r.h)
            x_s = max(l.s, r.s, max(l.h, 0) + max(r.h, 0) + x.val)
            return Info(x_h, x_s)
        
        return dfs(root).s
```

</details>

