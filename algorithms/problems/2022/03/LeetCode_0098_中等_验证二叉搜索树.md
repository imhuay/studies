## LeetCode_0098_验证二叉搜索树（中等, 2022-03）
<!--{
    "tags": ["二叉树"],
    "来源": "LeetCode",
    "难度": "中等",
    "编号": "0098",
    "标题": "验证二叉搜索树",
    "公司": []
}-->

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

