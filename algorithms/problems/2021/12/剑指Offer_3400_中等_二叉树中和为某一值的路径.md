## 二叉树中和为某一值的路径
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2025-07-08%2016%3A53%3A13&color=yellowgreen&style=flat-square)
[![](https://img.shields.io/static/v1?label=&message=%E4%B8%AD%E7%AD%89&color=yellow&style=flat-square)](../../../README.md#中等)
[![](https://img.shields.io/static/v1?label=&message=%E5%89%91%E6%8C%87Offer&color=green&style=flat-square)](../../../README.md#剑指offer)
[![](https://img.shields.io/static/v1?label=&message=%E4%BA%8C%E5%8F%89%E6%A0%91/%E6%A0%91&color=blue&style=flat-square)](../../../README.md#二叉树树)
[![](https://img.shields.io/static/v1?label=&message=%E6%B7%B1%E5%BA%A6%E4%BC%98%E5%85%88%E6%90%9C%E7%B4%A2&color=blue&style=flat-square)](../../../README.md#深度优先搜索)

<!--END_SECTION:badge-->
<!--info
tags: [二叉树, DFS]
source: 剑指Offer
level: 中等
number: '3400'
name: 二叉树中和为某一值的路径
companies: []
-->

<summary><b>问题简述</b></summary>

```txt
给定二叉树 root 和一个整数 targetSum ，找出所有从根节点到叶子节点路径总和等于给定目标和的路径。
```

<details><summary><b>详细描述</b></summary>

```txt
给你二叉树的根节点 root 和一个整数目标和 targetSum ，找出所有 从根节点到叶子节点 路径总和等于给定目标和的路径。

叶子节点 是指没有子节点的节点。

示例 1：
    输入：root = [5,4,8,11,null,13,4,7,2,null,null,5,1], targetSum = 22
    输出：[[5,4,11,2],[5,8,4,5]]
示例 2：
    输入：root = [1,2,3], targetSum = 5
    输出：[]
示例 3：
    输入：root = [1,2], targetSum = 0
    输出：[]

提示：
    树中节点总数在范围 [0, 5000] 内
    -1000 <= Node.val <= 1000
    -1000 <= targetSum <= 1000

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/er-cha-shu-zhong-he-wei-mou-yi-zhi-de-lu-jing-lcof
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```

</details>

<!-- <div align="center"><img src="../../../_assets/xxx.png" height="300" /></div> -->

<summary><b>思路</b></summary>

- 先序深度优先搜索；
- 因为要保存路径，所以还要加上回溯序列；

<details><summary><b>Python</b></summary>

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

class Solution:
    def pathSum(self, root: TreeNode, target: int) -> List[List[int]]:
        if not root: return []

        ret = []
        buf = []
        def dfs(R, T):
            # 这样写会导致结果输出两次，原因是如果当前叶节点满足后，会继续遍历其左右两个空节点，导致结果被添加两次
            # if not R:
            #     if T == 0:
            #         ret.append(buf[:])
            #     return

            if not R: return
            if R.left is None and R.right is None:
                if T == R.val:
                    ret.append(buf[:] + [R.val])  # 直接传 buf 会有问题，而 buf[:] 相对于 buf 的一份浅拷贝
                return

            buf.append(R.val)
            dfs(R.left, T - R.val)
            dfs(R.right, T - R.val)
            buf.pop()
        
        dfs(root, target)
        return ret
```

</details>

