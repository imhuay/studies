## LeetCode_0104_二叉树的最大深度（简单, 2021-10）
<!--{
    "tags": ["二叉树", "递归"],
    "来源": "LeetCode",
    "编号": "0104",
    "难度": "简单",
    "标题": "二叉树的最大深度"
}-->

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

