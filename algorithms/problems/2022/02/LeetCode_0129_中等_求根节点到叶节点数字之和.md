## LeetCode_0129_求根节点到叶节点数字之和（中等, 2022-02）
<!--{
    "tags": ["二叉树"],
    "来源": "LeetCode",
    "难度": "中等",
    "编号": "0129",
    "标题": "求根节点到叶节点数字之和",
    "公司": []
}-->

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

