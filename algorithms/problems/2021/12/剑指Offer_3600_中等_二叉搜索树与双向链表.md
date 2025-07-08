## 二叉搜索树与双向链表
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2022-10-14%2014%3A59%3A33&color=yellowgreen&style=flat-square)
[![](https://img.shields.io/static/v1?label=&message=%E4%B8%AD%E7%AD%89&color=yellow&style=flat-square)](../../../README.md#中等)
[![](https://img.shields.io/static/v1?label=&message=%E5%89%91%E6%8C%87Offer&color=green&style=flat-square)](../../../README.md#剑指offer)
[![](https://img.shields.io/static/v1?label=&message=%E4%BA%8C%E5%8F%89%E6%A0%91/%E6%A0%91&color=blue&style=flat-square)](../../../README.md#二叉树树)
[![](https://img.shields.io/static/v1?label=&message=%E9%80%92%E5%BD%92&color=blue&style=flat-square)](../../../README.md#递归)
[![](https://img.shields.io/static/v1?label=&message=%E7%BB%8F%E5%85%B8&color=blue&style=flat-square)](../../../README.md#经典)

<!--END_SECTION:badge-->
<!--info
tags: [二叉树, 递归, 经典]
source: 剑指Offer
level: 中等
number: '3600'
name: 二叉搜索树与双向链表
companies: []
-->

<summary><b>问题简述</b></summary>

```txt
输入一棵二叉搜索树，将该二叉搜索树转换成一个排序的循环双向链表。
```

<details><summary><b>详细描述</b></summary>

```txt
输入一棵二叉搜索树，将该二叉搜索树转换成一个排序的循环双向链表。要求不能创建任何新的节点，只能调整树中节点指针的指向。

为了让您更好地理解问题，以下面的二叉搜索树为例：

     4
    / \
   2   5
  / \
 1   3

我们希望将这个二叉搜索树转化为双向循环链表。链表中的每个节点都有一个前驱和后继指针。对于双向循环链表，第一个节点的前驱是最后一个节点，最后一个节点的后继是第一个节点。

下图展示了上面的二叉搜索树转化成的链表。“head” 表示指向链表中有最小元素的节点。

 head -> 1 <-> 2 <-> 3 <-> 4 <-> 5 (1 和 5 也互连)
         ↑-----------------------↑

特别地，我们希望可以就地完成转换操作。当转化完成以后，树中节点的左指针需要指向前驱，树中节点的右指针需要指向后继。还需要返回链表中的第一个节点的指针。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/er-cha-sou-suo-shu-yu-shuang-xiang-lian-biao-lcof
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```

</details>

<!-- <div align="center"><img src="../../../_assets/xxx.png" height="300" /></div> -->

<summary><b>思路</b></summary>

- 根据二叉搜索树的性质，其**中序遍历**结果就是一个有序的单向链表；
- 因此本题要做的就是在中序遍历的过程中，修改指针的指向，得到双向链表；
- 考虑使用中序遍历访问树的各节点，记 `cur`，初始化前驱节点 `pre=None`；  
  1. 在访问每个节点时构建 `cur` 和前驱节点 `pre` 的引用指向；  
  2. 当 `pre=None` 时，说明该节点是最左叶子节点（中序遍历访问的第一个节点），即头结点 `ret`；否则修改双向节点引用，即 `pre.right = cur`， `cur.left = pre`；
  3. **在访问右子树前，将 `pre` 指向 `cur`；**
  4. 中序遍历完成后，最后构建头节点和尾节点的引用指向。  

<details><summary><b>Python</b></summary>

```python
"""
# Definition for a Node.
class Node:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
"""
class Solution:
    def treeToDoublyList(self, root: 'Node') -> 'Node':
        if not root: return None

        self.ret = self.pre = None

        def dfs(cur):
            if not cur:
                return

            dfs(cur.left)
            if self.pre:
                self.pre.right = cur
                cur.left = self.pre
            else:  # 达到最左叶子节点（只执行一次）
                self.ret = cur  # 双向链表的头结点
            
            self.pre = cur  # 在遍历右子树前，将 pre 指向 cur
            dfs(cur.right)

        dfs(root)
        # 遍历结束时，pre 指向最右叶子节点
        self.ret.left = self.pre 
        self.pre.right = self.ret
        return self.ret
```

</details>

