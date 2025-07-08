## 层序遍历二叉树（之字形遍历）
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2022-10-14%2014%3A59%3A33&color=yellowgreen&style=flat-square)
[![](https://img.shields.io/static/v1?label=&message=%E7%AE%80%E5%8D%95&color=yellow&style=flat-square)](../../../README.md#简单)
[![](https://img.shields.io/static/v1?label=&message=%E5%89%91%E6%8C%87Offer&color=green&style=flat-square)](../../../README.md#剑指offer)
[![](https://img.shields.io/static/v1?label=&message=%E5%B9%BF%E5%BA%A6%E4%BC%98%E5%85%88%E6%90%9C%E7%B4%A2&color=blue&style=flat-square)](../../../README.md#广度优先搜索)
[![](https://img.shields.io/static/v1?label=&message=%E4%BA%8C%E5%8F%89%E6%A0%91/%E6%A0%91&color=blue&style=flat-square)](../../../README.md#二叉树树)
[![](https://img.shields.io/static/v1?label=&message=%E6%A0%88/%E9%98%9F%E5%88%97&color=blue&style=flat-square)](../../../README.md#栈队列)

<!--END_SECTION:badge-->
<!--info
tags: [BFS, 二叉树, 队列]
source: 剑指Offer
level: 简单
number: '3203'
name: 层序遍历二叉树（之字形遍历）
companies: []
-->

<summary><b>问题简述</b></summary>

```txt
按照之字形顺序打印二叉树，即第一行按照从左到右的顺序打印，第二层按照从右到左的顺序打印，第三行再按照从左到右的顺序打印，其他行以此类推。
```

<details><summary><b>详细描述</b></summary>

```txt
请实现一个函数按照之字形顺序打印二叉树，即第一行按照从左到右的顺序打印，第二层按照从右到左的顺序打印，第三行再按照从左到右的顺序打印，其他行以此类推。

例如:
    给定二叉树: [3,9,20,null,null,15,7],

        3
       / \
      9  20
        /  \
       15   7
    返回其层次遍历结果：

    [
        [3],
        [20,9],
        [15,7]
    ]

提示：
    节点总数 <= 1000

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/cong-shang-dao-xia-da-yin-er-cha-shu-iii-lcof
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```

</details>

<!-- <div align="center"><img src="../../../_assets/xxx.png" height="300" /></div> -->

<summary><b>思路</b></summary>

- 在“层序遍历二叉树-2”的基础上，加入奇偶层的处理即可；

<details><summary><b>Python</b></summary>

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution:
    def levelOrder(self, root: TreeNode) -> List[List[int]]:
        from collections import deque

        if not root: return []

        buf = deque([root])
        lv = 1  # 记录当前层数
        cnt = 1  # 记录当前层的节点数
        ret = []
        while buf:
            tmp = []
            for _ in range(cnt):
                cur = buf.popleft()
                tmp.append(cur.val)
                cnt -= 1

                if cur.left:
                    buf.append(cur.left)
                    cnt += 1
                if cur.right:
                    buf.append(cur.right)
                    cnt += 1
            
            # 上面的代码跟 层序遍历二叉树-2 完全相同，
            # 在将 tmp 加入 ret 时，对偶数层的 tmp 做一下倒序
            if lv & 1:  # 奇数层
                ret.append(tmp)
            else:
                ret.append(tmp[::-1])
            lv += 1
        
        return ret
```

</details>

