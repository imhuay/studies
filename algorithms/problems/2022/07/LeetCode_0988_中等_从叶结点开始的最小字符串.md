## 从叶结点开始的最小字符串
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2022-10-14%2014%3A59%3A33&color=yellowgreen&style=flat-square)
[![](https://img.shields.io/static/v1?label=&message=%E4%B8%AD%E7%AD%89&color=yellow&style=flat-square)](../../../README.md#中等)
[![](https://img.shields.io/static/v1?label=&message=LeetCode&color=green&style=flat-square)](../../../README.md#leetcode)
[![](https://img.shields.io/static/v1?label=&message=%E4%BA%8C%E5%8F%89%E6%A0%91/%E6%A0%91&color=blue&style=flat-square)](../../../README.md#二叉树树)

<!--END_SECTION:badge-->
<!--info
tags: [二叉树]
source: LeetCode
level: 中等
number: '0988'
name: 从叶结点开始的最小字符串
companies: []
-->

<summary><b>问题简述</b></summary>

```txt
给定一颗根结点为 root 的二叉树，树中的每一个结点都有一个从 0 到 25 的值，分别代表字母 'a' 到 'z'：值 0 代表 'a'，值 1 代表 'b'，依此类推。

找出按字典序最小的字符串，该字符串从这棵树的一个叶结点开始，到根结点结束。
```
> [988. 从叶结点开始的最小字符串 - 力扣（LeetCode）](https://leetcode-cn.com/problems/smallest-string-starting-from-leaf/)

<!-- 
<details><summary><b>详细描述</b></summary>

```txt
```

</details>
-->


<!-- <div align="center"><img src="../../../_assets/xxx.png" height="300" /></div> -->

<summary><b>思路：先序遍历</b></summary>

- 自顶向下先序遍历即可，使用一个全局变量记录最小值；
- 踩坑：第一眼想到的是后序遍历，即贪心的查找每个节点的最小值，但在这里局部最优不能推出全局最优；
    > 用例1：`[4,0,1,1]` 错误: `"be"` 预期: `"bae"`  
    > 用例2：`[25,1,null,0,0,1,null,null,null,0]` 错误: `"abz"` 预期: `"ababz"`


<details><summary><b>Python：写法1）回溯（推荐）</b></summary>

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def smallestFromLeaf(self, root: Optional[TreeNode]) -> str:

        from collections import deque
        
        self.ret = '~'  # '~' > 'z'

        def get_c(v):  # 数字转字母
            return chr(97 + v)

        def dfs(x, buf):  # 先序遍历
            if not x: return

            buf.appendleft(get_c(x.val))
            if not x.left and not x.right:  # 当达到叶子节点时比较
                self.ret = min(self.ret, ''.join(buf))

            dfs(x.left, buf)
            dfs(x.right, buf)
            buf.popleft()  # 记得回溯
        
        dfs(root, deque())
        return self.ret
```

</details>


<details><summary><b>Python：写法2）不回溯，直接修改实参</b></summary>

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def smallestFromLeaf(self, root: Optional[TreeNode]) -> str:

        self.ret = '~'  # '~' > 'z'

        def get_c(v):  # 数字转字母
            return chr(97 + v)

        def dfs(x, buf):  # 先序遍历
            if not x: return

            if not x.left and not x.right:  # 当达到叶子节点时比较
                self.ret = min(self.ret, get_c(x.val) + buf)

            # 不回溯，直接修改实参
            dfs(x.left, get_c(x.val) + buf)
            dfs(x.right, get_c(x.val) + buf)
        
        dfs(root, '')
        return self.ret
```

</details>
