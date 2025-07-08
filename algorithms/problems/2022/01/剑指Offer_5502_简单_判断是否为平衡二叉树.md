## 判断是否为平衡二叉树
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2022-10-14%2014%3A59%3A33&color=yellowgreen&style=flat-square)
[![](https://img.shields.io/static/v1?label=&message=%E7%AE%80%E5%8D%95&color=yellow&style=flat-square)](../../../README.md#简单)
[![](https://img.shields.io/static/v1?label=&message=%E5%89%91%E6%8C%87Offer&color=green&style=flat-square)](../../../README.md#剑指offer)
[![](https://img.shields.io/static/v1?label=&message=%E4%BA%8C%E5%8F%89%E6%A0%91/%E6%A0%91&color=blue&style=flat-square)](../../../README.md#二叉树树)

<!--END_SECTION:badge-->
<!--info
tags: [二叉树]
source: 剑指Offer
level: 简单
number: '5502'
name: 判断是否为平衡二叉树
companies: []
-->

<summary><b>问题简述</b></summary>

```txt
输入一棵二叉树的根节点，判断该树是不是平衡二叉树。
```

<details><summary><b>详细描述</b></summary>

```txt
输入一棵二叉树的根节点，判断该树是不是平衡二叉树。如果某二叉树中任意节点的左右子树的深度相差不超过1，那么它就是一棵平衡二叉树。

示例 1:
    给定二叉树 [3,9,20,null,null,15,7]

        3
       / \
      9  20
        /  \
       15   7
    返回 true 。

示例 2:
    给定二叉树 [1,2,2,3,3,null,null,4,4]

           1
          / \
         2   2
        / \
       3   3
      / \
     4   4
    返回 false 。

限制：
    0 <= 树的结点个数 <= 10000

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/ping-heng-er-cha-shu-lcof
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```

</details>

<!-- <div align="center"><img src="../../../_assets/xxx.png" height="300" /></div> -->

<summary><b>思路1: 先序遍历，自顶向下（次优解）</b></summary>

- 设计一个求树高度的子函数；
- 如果左右子树的高度差 <= 1 则返回 True；然后递归遍历左右子树；
- 存在大量重复计算，时间复杂度 `O(NlogN)`

<details><summary><b>Python</b></summary>

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution:
    def isBalanced(self, root: TreeNode) -> bool:

        def depth(node):
            if node is None:
                return 0
            return 1 + max(depth(node.left), depth(node.right))
        
        def dfs(node):
            if node is None:
                return True
            
            return abs(depth(node.left) - depth(node.right)) <= 1 \
                and dfs(node.left) \
                and dfs(node.right)
            
        return dfs(root)
```

</details>

<summary><b>思路2: 后序遍历，自底向上（最优解）</b></summary>

> [平衡二叉树（从底至顶、从顶至底，清晰图解）](https://leetcode-cn.com/problems/ping-heng-er-cha-shu-lcof/solution/mian-shi-ti-55-ii-ping-heng-er-cha-shu-cong-di-zhi/)

<details><summary><b>Python</b></summary>

- 可以在求二叉树深度的过程中，提前判断是否为平衡二叉树，若不是则提前结束（剪枝）；
- 时间复杂度：`O(N)`；

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution:
    def isBalanced(self, root: TreeNode) -> bool:

        def dfs(node):
            if node is None:
                return 0

            lh = dfs(node.left)  # 左子树的高度
            if lh == -1:
                return -1

            rh = dfs(node.right)  # 右子树的高度
            if rh == -1:
                return -1

            if abs(lh - rh) <= 1:
                return 1 + max(lh, rh) + 1
            else:
                return -1

        return dfs(root) != -1
```

</details>