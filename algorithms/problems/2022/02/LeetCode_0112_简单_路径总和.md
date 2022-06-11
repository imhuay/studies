## LeetCode_0112_路径总和（简单, 2022-02）
<!--{
    "tags": ["二叉树"],
    "来源": "LeetCode",
    "难度": "简单",
    "编号": "0112",
    "标题": "路径总和",
    "公司": []
}-->

<summary><b>问题简述</b></summary>

```txt
给你二叉树的根节点 root 和一个表示目标和的整数 targetSum 。判断该树中是否存在 根节点到叶子节点 的路径，这条路径上所有节点值相加等于目标和 targetSum 。如果存在，返回 true ；否则，返回 false 。

叶子节点 是指没有子节点的节点。
```
> [112. 路径总和 - 力扣（LeetCode）](https://leetcode-cn.com/problems/path-sum/)

<!-- 
<details><summary><b>详细描述</b></summary>

```txt
```

</details>
-->


<!-- <div align="center"><img src="../../../_assets/xxx.png" height="300" /></div> -->

<summary><b>思路</b></summary>

- 先序遍历，达到叶子节点是进行判断；
- 注意空节点的判断；

<details><summary><b>Python</b></summary>

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def hasPathSum(self, root: Optional[TreeNode], targetSum: int) -> bool:

        def dfs(x, rest):
            if not x:
                return False
            
            rest -= x.val
            if not x.left and not x.right:
                return rest == 0
            l, r = dfs(x.left, rest), dfs(x.right, rest)
            rest += x.val
            return l or r
        
        ret = dfs(root, targetSum)
        return ret
```

</details>

