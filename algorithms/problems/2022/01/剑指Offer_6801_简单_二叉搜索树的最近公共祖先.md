## 二叉搜索树的最近公共祖先
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2025-07-08%2016%3A53%3A13&color=yellowgreen&style=flat-square)
[![](https://img.shields.io/static/v1?label=&message=%E7%AE%80%E5%8D%95&color=yellow&style=flat-square)](../../../README.md#简单)
[![](https://img.shields.io/static/v1?label=&message=%E5%89%91%E6%8C%87Offer&color=green&style=flat-square)](../../../README.md#剑指offer)
[![](https://img.shields.io/static/v1?label=&message=%E4%BA%8C%E5%8F%89%E6%A0%91/%E6%A0%91&color=blue&style=flat-square)](../../../README.md#二叉树树)
[![](https://img.shields.io/static/v1?label=&message=%E7%BB%8F%E5%85%B8&color=blue&style=flat-square)](../../../README.md#经典)

<!--END_SECTION:badge-->
<!--info
tags: [二叉搜索树, 经典]
source: 剑指Offer
level: 简单
number: '6801'
name: 二叉搜索树的最近公共祖先
companies: []
-->

<summary><b>问题简述</b></summary>

> [剑指 Offer 68 - I. 二叉搜索树的最近公共祖先 - 力扣（LeetCode）](https://leetcode-cn.com/problems/er-cha-sou-suo-shu-de-zui-jin-gong-gong-zu-xian-lcof/)

```txt
给定一个二叉搜索树, 找到该树中两个指定节点的最近公共祖先。

如果是普通二叉树呢？
```

<details><summary><b>详细描述</b></summary>

```txt
给定一个二叉搜索树, 找到该树中两个指定节点的最近公共祖先。

百度百科中最近公共祖先的定义为：“对于有根树 T 的两个结点 p、q，最近公共祖先表示为一个结点 x，满足 x 是 p、q 的祖先且 x 的深度尽可能大（一个节点也可以是它自己的祖先）。”

例如，给定如下二叉搜索树

            6
          /   \
         2     8
        / \   / \
       0   4 7   9
          / \
         3   5

示例 1:
    输入: root = [6,2,8,0,4,7,9,null,null,3,5], p = 2, q = 8
    输出: 6 
    解释: 节点 2 和节点 8 的最近公共祖先是 6。
示例 2:
    输入: root = [6,2,8,0,4,7,9,null,null,3,5], p = 2, q = 4
    输出: 2
    解释: 节点 2 和节点 4 的最近公共祖先是 2, 因为根据定义最近公共祖先节点可以为节点本身。

说明:
    所有节点的值都是唯一的。
    p、q 为不同节点且均存在于给定的二叉搜索树中。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/er-cha-sou-suo-shu-de-zui-jin-gong-gong-zu-xian-lcof
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```

</details>

<!-- <div align="center"><img src="../../../_assets/xxx.png" height="300" /></div> -->

<summary><b>思路1：基于二叉搜索树</b></summary>

- 根据二叉搜索树的性质：左子树都小于父节点，右子树都大于父节点，快速找出指定节点的父节点路径；
- 然后找出最近的公共祖先；

<details><summary><b>Python</b></summary>

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution:
    def lowestCommonAncestor(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':

        def foo(node, p):
            ret = []
            while p and p.val != node.val:
                ret.append(p)
                if p.val > node.val:
                    p = p.left
                else:
                    p = p.right
            ret.append(p)
            return ret
        
        P = foo(p, root)
        Q = foo(q, root)

        ret = None
        for l, r in zip(P, Q):
            if l.val == r.val:
                ret = l
            else:
                break
        
        return ret
```

</details>


**优化1**：根据二叉搜索树的定义，如果一个节点 node 是 p 和 q 的祖先，则有 node 同时 >= 或 <= p 和 q；因此可以优化为一次遍历；

<details><summary><b>Python</b></summary>

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution:
    def lowestCommonAncestor(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':

        node = root
        while node:
            if node.val > p.val and node.val > q.val:
                node = node.left
            elif node.val < p.val and node.val < q.val:
                node = node.right
            else:
                break
        
        return node
```

</details>

**优化2**：若可保证 `p.val < q.val`，则在循环中可减少判断条件。
> [二叉搜索树的最近公共祖先（迭代 / 递归，清晰图解）](https://leetcode-cn.com/problems/er-cha-sou-suo-shu-de-zui-jin-gong-gong-zu-xian-lcof/solution/mian-shi-ti-68-i-er-cha-sou-suo-shu-de-zui-jin-g-7/)

<details><summary><b>Python</b></summary>

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution:
    def lowestCommonAncestor(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
        if q.val > p.val: 
            p, q = q, p

        node = root
        while node:
            if node.val > p.val:
                node = node.left
            elif node.val < q.val:
                node = node.right
            else:
                break
        
        return node
```

</details>


<summary><b>思路2：普通二叉树</b></summary>

> [剑指 Offer 68 - II. 二叉树的最近公共祖先 - 力扣（LeetCode）](https://leetcode-cn.com/problems/er-cha-shu-de-zui-jin-gong-gong-zu-xian-lcof/)

- 思路1 利用了二叉搜索树的性质快速获取祖先路径；
- 可以不利用二叉搜索树的性质来获取祖先路径（对非二叉搜索树也适用）；
- 因为必须先找到目标节点才能确定路线，所以可以考虑后序遍历；当找到目标节点时，返回 flag，指示上级节点是否为祖先节点；

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

        # 后序遍历搜索历史祖先，因为是后序遍历，所以 trace 是倒序的
        def dfs(node, target, trace):
            if node is None:
                return False
            if node.val == target.val:
                trace.append(node)  # 根据定义，自己也是自己的祖先节点
                return True
            
            if dfs(node.left, target, trace) or dfs(node.right, target, trace):
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


**优化**：不使用额外空间存储祖先路径，即在遍历过程中判断；
> [二叉树的最近公共祖先（DFS ，清晰图解） - Krahets](https://leetcode-cn.com/problems/er-cha-shu-de-zui-jin-gong-gong-zu-xian-lcof/solution/mian-shi-ti-68-ii-er-cha-shu-de-zui-jin-gong-gon-7/)

- 如果 node 仅是 p 和 q 的公共祖先（但不是最近公共祖先），那么 node 的左右子树之一必也是 p 和 q 的公共祖先；
- 如果 node 是 p 和 q 的最近公共祖先，那么 node 的左右子树都不是 p 和 q 的公共祖先；
- 根据以上两条性质，可知，如果 node 是 p、q 的**最近公共祖先**，有：
    - node 是 p、q 的公共祖先，且 p 和 q 分别在 node 的两侧；
    - node 是 p 或 q 之一，且是另一个节点的祖先；


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
        
        def dfs(node):
            # 下面两个判断条件可以写在一起，为了使逻辑更清晰，故分开写
            if node is None:  # 说明当前路径上没有 p 或 q
                return None
            if node == p or node == q:  # 说明当前路径上存在 p 或 q
                return node
            
            l = dfs(node.left)
            r = dfs(node.right)

            # 返回的非 None 节点都是 p 和 q 的公共祖先
            if l is None and r is not None:  # r 是 p 和 q 之一，且是另一个节点的祖先
                return r
            elif r is None and l is not None:  # l 是 p 和 q 之一，且是另一个节点的祖先
                return l
            elif l and r:  # p 和 q 分别在 node 的两侧
                return node
            else:
                return None

        return dfs(root)

```

</details>

