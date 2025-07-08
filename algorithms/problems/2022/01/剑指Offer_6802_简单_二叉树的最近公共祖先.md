## 二叉树的最近公共祖先
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2022-10-14%2014%3A59%3A33&color=yellowgreen&style=flat-square)
[![](https://img.shields.io/static/v1?label=&message=%E7%AE%80%E5%8D%95&color=yellow&style=flat-square)](../../../README.md#简单)
[![](https://img.shields.io/static/v1?label=&message=%E5%89%91%E6%8C%87Offer&color=green&style=flat-square)](../../../README.md#剑指offer)
[![](https://img.shields.io/static/v1?label=&message=%E4%BA%8C%E5%8F%89%E6%A0%91/%E6%A0%91&color=blue&style=flat-square)](../../../README.md#二叉树树)
[![](https://img.shields.io/static/v1?label=&message=%E6%A0%91%E5%BD%A2%E9%80%92%E5%BD%92&color=blue&style=flat-square)](../../../README.md#树形递归)

<!--END_SECTION:badge-->
<!--info
tags: [二叉树, TreeDP]
source: 剑指Offer
level: 简单
number: '6802'
name: 二叉树的最近公共祖先
companies: []
-->

<summary><b>问题简述</b></summary>

```txt
给定一个二叉树, 找到该树中两个指定节点的最近公共祖先。
```
> [剑指 Offer 68 - II. 二叉树的最近公共祖先 - 力扣（LeetCode）](https://leetcode-cn.com/problems/er-cha-shu-de-zui-jin-gong-gong-zu-xian-lcof/)

<details><summary><b>详细描述</b></summary>

```txt
给定一个二叉树, 找到该树中两个指定节点的最近公共祖先。

百度百科中最近公共祖先的定义为：“对于有根树 T 的两个结点 p、q，最近公共祖先表示为一个结点 x，满足 x 是 p、q 的祖先且 x 的深度尽可能大（一个节点也可以是它自己的祖先）。”

例如，给定如下二叉搜索树

            3
          /   \
         5     1
        / \   / \
       6   2 0   8
          / \
         7   4

示例 1:
    输入: root = [3,5,1,6,2,0,8,null,null,7,4], p = 5, q = 1
    输出: 3
    解释: 节点 5 和节点 1 的最近公共祖先是节点 3。
示例 2:
    输入: root = [3,5,1,6,2,0,8,null,null,7,4], p = 5, q = 4
    输出: 5
    解释: 节点 5 和节点 4 的最近公共祖先是节点 5。因为根据定义最近公共祖先节点可以为节点本身。

说明:
    所有节点的值都是唯一的。
    p、q 为不同节点且均存在于给定的二叉树中。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/er-cha-shu-de-zui-jin-gong-gong-zu-xian-lcof
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```

</details>

<!-- <div align="center"><img src="../../../_assets/xxx.png" height="300" /></div> -->

<summary><b>思路1</b></summary>

- 记录 p, q 从上到下的路径，路径中最后一个相同节点即答案；

<details><summary><b>Python</b></summary>

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution:
    def lowestCommonAncestor(self, root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:

        # 后序遍历记录所有祖先
        def dfs(node, target, trace):
            if node is None:
                return False
            
            # 注意自己也是自己的祖先
            if node.val == target.val or dfs(node.left, target, trace) or dfs(node.right, target, trace):
                trace.append(node)
                return True
            else:
                return False
        
        # 分别找出 p 和 q 的祖先路径
        trace_p = []
        dfs(root, p, trace_p)
        # print(trace_p)
        trace_q = []
        dfs(root, q, trace_q)
        # print(trace_q)

        # 遍历找出最后一个相同的祖先
        ret = None
        for l, r in zip(trace_p[::-1], trace_q[::-1]):
            if l.val == r.val:
                ret = l
            else:
                break
        
        return ret
```

</details>


<summary><b>思路2</b></summary>

- 考虑判断节点 x 是否为 p、q 的最近祖先需要哪些信息：
- 文字描述太繁琐，直接看代码，非常清晰；

<details><summary><b>Python</b></summary>

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution:
    def lowestCommonAncestor(self, root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
        
        from dataclasses import dataclass

        @dataclass
        class Info:  # 判断当前节点是否为答案需要从子节点了解到的信息
            has_p: bool
            has_q: bool
            ret: TreeNode
        
        def dfs(x):
            if not x: return Info(False, False, None)

            # l, r = dfs(x.left), dfs(x.right)
            # 提前结束
            l = dfs(x.left)
            if l.ret: return l
            r = dfs(x.right)
            if r.ret: return r

            has_p = x.val == p.val or l.has_p or r.has_p
            has_q = x.val == q.val or l.has_q or r.has_q
            ret = None

            if has_p and has_q:
                ret = l.ret if r.ret is None else r.ret  # 左右子节点
                ret = x if ret is None else ret  # x 节点才是
            
            return Info(has_p, has_q, ret)
        
        return dfs(root).ret
```

</details>