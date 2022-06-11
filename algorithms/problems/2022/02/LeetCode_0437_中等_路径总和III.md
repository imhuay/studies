## LeetCode_0437_路径总和III（中等, 2022-02）
<!--{
    "tags": ["二叉树", "深度优先搜索", "前缀和", "TreeDP"],
    "来源": "LeetCode",
    "编号": "0437",
    "难度": "中等",
    "标题": "路径总和III",
    "公司": []
}-->

<summary><b>问题简述</b></summary>

```txt
给定一个二叉树的根节点 root ，和一个整数 targetSum ，求该二叉树里节点值之和等于 targetSum 的 路径 的数目。

路径 不需要从根节点开始，也不需要在叶子节点结束，但是路径方向必须是向下的（只能从父节点到子节点）。
```
> [437. 路径总和 III - 力扣（LeetCode）](https://leetcode-cn.com/problems/path-sum-iii/)

<!-- 
<details><summary><b>详细描述</b></summary>

```txt
```

</details>
-->


<!-- <div align="center"><img src="../../../_assets/xxx.png" height="300" /></div> -->

<summary><b>思路1：先序遍历</b></summary>

- 先序遍历每个节点，每个节点再先序遍历找目标值；

<details><summary><b>Python</b></summary>

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def pathSum(self, root: TreeNode, targetSum: int) -> int:  # noqa
        """"""
        if root is None:
            return 0

        def dfs(x, rest):
            if not x:
                return 0

            ans = 0 if x.val != rest else 1  # 如果相等说明，从头结点开始到该节点可以形成一条路径

            # 继续遍历左右子树
            rest -= x.val
            ans += dfs(x.left, rest)
            ans += dfs(x.right, rest)
            rest += x.val  # 回溯
            return ans

        # dfs 是一个先序遍历
        ret = dfs(root, targetSum)
        # pathSum 本身也是一个先序遍历，相当于对每个点都做一次 dfs
        ret += self.pathSum(root.left, targetSum)
        ret += self.pathSum(root.right, targetSum)

        return ret
```

</details>


<summary><b>思路2：先序遍历+前缀和（最优）</b></summary>

> [【宫水三叶】一题双解 :「DFS」&「前缀和」 - 路径总和 III - 力扣（LeetCode）](https://leetcode-cn.com/problems/path-sum-iii/solution/gong-shui-san-xie-yi-ti-shuang-jie-dfs-q-usa7/)

<details><summary><b>Python</b></summary>

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def pathSum(self, root: TreeNode, targetSum: int) -> int:
        from collections import defaultdict
        self.prefix = defaultdict(int)  # 保存前缀和
        self.prefix[0] = 1
        self.targetSum = targetSum

        def dfs(x, preSum):
            if not x: return 0

            ret = 0
            preSum += x.val
            ret += self.prefix[preSum - targetSum]

            self.prefix[preSum] += 1
            ret += dfs(x.left, preSum)
            ret += dfs(x.right, preSum)
            self.prefix[preSum] -= 1

            return ret

        return dfs(root, 0)
```

</details>


<summary><b>思路3：后序遍历（树形DP）（推荐）</b></summary>

<details><summary><b>Python</b></summary>

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def pathSum(self, root: TreeNode, targetSum: int) -> int:
        from collections import defaultdict
        self.prefix = defaultdict(int)  # 保存前缀和
        self.prefix[0] = 1
        self.targetSum = targetSum

        def dfs(x, preSum):
            if not x: return 0

            ret = 0
            preSum += x.val
            ret += self.prefix[preSum - targetSum]

            self.prefix[preSum] += 1
            ret += dfs(x.left, preSum)
            ret += dfs(x.right, preSum)
            self.prefix[preSum] -= 1

            return ret

        return dfs(root, 0)
```

</details>
