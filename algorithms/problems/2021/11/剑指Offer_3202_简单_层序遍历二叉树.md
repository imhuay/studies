## 剑指Offer_3202_层序遍历二叉树（简单, 2021-11）
<!--{
    "tags": ["BFS", "二叉树", "队列"],
    "来源": "剑指Offer",
    "编号": "3202",
    "难度": "简单",
    "标题": "层序遍历二叉树"
}-->

<summary><b>问题简述</b></summary>

```txt
从上到下按层打印二叉树，同一层的节点按从左到右的顺序打印，每一层打印到一行。
```

<details><summary><b>详细描述</b></summary>

```txt
从上到下按层打印二叉树，同一层的节点按从左到右的顺序打印，每一层打印到一行。

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
        [9,20],
        [15,7]
    ]

提示：
    节点总数 <= 1000

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/cong-shang-dao-xia-da-yin-er-cha-shu-ii-lcof
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```

</details>

<!-- <div align="center"><img src="../../../_assets/xxx.png" height="300" /></div> -->

<summary><b>思路</b></summary>

- 相比 “层序遍历二叉树-1”，本题需要同时记录当前层的节点数量（写法1）；
- 实际上每一层的节点数量包含在了保存的队列信息中，详见（写法2）；

<details><summary><b>Python：写法1</b></summary>

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
        cnt = 1  # 记录当前层的节点数量
        ret = []
        while buf:
            tmp = []  # 记录层结果
            for _ in range(cnt):  # 循环当前层节点数量的次数，期间改变 cnt 不会影响遍历次数
                cur = buf.popleft()
                tmp.append(cur.val)
                cnt -= 1

                if cur.left:
                    buf.append(cur.left)
                    cnt += 1
                if cur.right:
                    buf.append(cur.right)
                    cnt += 1
            ret.append(tmp)

        return ret
```

</details>

<details><summary><b>Python：写法2</b></summary>

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
        ret = []
        while buf:
            tmp = []
            for _ in range(len(buf)):
                cur = buf.popleft()
                tmp.append(cur.val)
                
                if cur.left:
                    buf.append(cur.left)
                if cur.right:
                    buf.append(cur.right)
            
            ret.append(tmp)
        
        return ret
```

</details>

