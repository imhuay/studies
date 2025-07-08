## 二叉树的镜像
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2025-07-08%2016%3A53%3A13&color=yellowgreen&style=flat-square)
[![](https://img.shields.io/static/v1?label=&message=%E7%AE%80%E5%8D%95&color=yellow&style=flat-square)](../../../README.md#简单)
[![](https://img.shields.io/static/v1?label=&message=%E5%89%91%E6%8C%87Offer&color=green&style=flat-square)](../../../README.md#剑指offer)
[![](https://img.shields.io/static/v1?label=&message=%E4%BA%8C%E5%8F%89%E6%A0%91/%E6%A0%91&color=blue&style=flat-square)](../../../README.md#二叉树树)
[![](https://img.shields.io/static/v1?label=&message=%E9%80%92%E5%BD%92&color=blue&style=flat-square)](../../../README.md#递归)

<!--END_SECTION:badge-->
<!--info
tags: [二叉树, 递归]
source: 剑指Offer
level: 简单
number: '2700'
name: 二叉树的镜像
companies: []
-->

<summary><b>问题简述</b></summary>

```txt
输入一个二叉树，输出它的镜像。
```

<details><summary><b>详细描述</b></summary>

```txt
请完成一个函数，输入一个二叉树，该函数输出它的镜像。

例如输入：

     4
   /   \
  2     7
 / \   / \
1   3 6   9

镜像输出：

     4
   /   \
  7     2
 / \   / \
9   6 3   1

示例 1：
    输入：root = [4,2,7,1,3,6,9]
    输出：[4,7,2,9,6,3,1]

限制：
    0 <= 节点个数 <= 1000

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/er-cha-shu-de-jing-xiang-lcof
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```

<!-- <div align="center"><img src="./_assets/xxx.png" height="300" /></div> -->

</details>


<summary><b>思路</b></summary>

- 对当前节点，镜像操作，就是调换左右子树，即 `left, right = right, left`；
- 对整个树镜像，就是将每个节点下的左右子树都调换；
- 具体操作：**先序或后序**遍历每个节点，然后交换该节点的左右子树；
- **为什么不可以中序遍历？**
    - 根据中序遍历的性质，当对根节点进行操作镜像时，其左子树已经完成了镜像，右子树还没有；
    - 此时交换左右子树，相当于把已经完成交换的左子树变成了右子树，之后在右子树上的镜像操作实际还是在对这个原来的左子树操作（相当于又把它还原了）；
    - 所以中序遍历的最终结果，就只是仅仅交换了根节点的左右子树；

<details><summary><b>Python</b></summary>

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution:
    def mirrorTree(self, root: TreeNode) -> TreeNode:
        """"""
        if root is None: return None

        # 交换左右子树
        root.left, root.right = root.right, root.left

        # 递归应用到左右子树
        self.mirrorTree(root.left)
        self.mirrorTree(root.right)

        return root
```

</details>

