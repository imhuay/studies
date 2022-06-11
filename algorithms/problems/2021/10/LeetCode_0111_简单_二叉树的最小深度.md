## LeetCode_0111_二叉树的最小深度（简单, 2021-10）
<!--{
    "tags": ["二叉树", "DFS"],
    "来源": "LeetCode",
    "编号": "0111",
    "难度": "简单",
    "标题": "二叉树的最小深度"
}-->

<summary><b>问题描述</b></summary>

```txt
给定一个二叉树，找出其最小深度。

最小深度是从根节点到最近叶子节点的最短路径上的节点数量。

示例：
    给定二叉树 [3,9,20,null,null,15,7]，
        3
       / \
      9  20
        /  \
       15   7
    返回它的最小深度 2 。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/minimum-depth-of-binary-tree
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```

<summary><b>思路</b></summary>

- 深度优先搜索，记录过程中的最小深度；

<details><summary><b>Python：深度优先搜索</b></summary>

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

class Solution:
    def minDepth(self, root: TreeNode) -> int:
        """"""
        if not root:  # 尾递归1
            return 0

        if not root.left and not root.right:  # 尾递归 2 *
            return 1
        
        min_depth = 10**5 + 10
        if root.left:
            min_depth = min(self.minDepth(root.left), min_depth)
        if root.right:
            min_depth = min(self.minDepth(root.right), min_depth)
        
        return min_depth + 1
```

</details>

