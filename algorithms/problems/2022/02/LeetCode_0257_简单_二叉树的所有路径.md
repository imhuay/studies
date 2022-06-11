## LeetCode_0257_二叉树的所有路径（简单, 2022-02）
<!--{
    "tags": ["二叉树"],
    "来源": "LeetCode",
    "难度": "简单",
    "编号": "0257",
    "标题": "二叉树的所有路径",
    "公司": []
}-->

<summary><b>问题简述</b></summary>

```txt
给你一个二叉树的根节点 root ，按 任意顺序 ，返回所有从根节点到叶子节点的路径。

叶子节点 是指没有子节点的节点。
```
> [257. 二叉树的所有路径 - 力扣（LeetCode）](https://leetcode-cn.com/problems/binary-tree-paths/)

<!-- 
<details><summary><b>详细描述</b></summary>

```txt
```

</details>
-->


<!-- <div align="center"><img src="../../../_assets/xxx.png" height="300" /></div> -->

<summary><b>思路</b></summary>

- 先序遍历，特殊处理叶子节点；

<details><summary><b>Python</b></summary>

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def binaryTreePaths(self, root: Optional[TreeNode]) -> List[str]:
        
        ret = []
        tmp = []

        def dfs(x):
            if not x: return 
            
            tmp.append(str(x.val))
            if not x.left and not x.right:
                ret.append('->'.join(tmp))
            
            dfs(x.left)
            dfs(x.right)
            tmp.pop()
        
        dfs(root)
        return ret
```

</details>

