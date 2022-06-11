## 剑指Offer_3400_二叉树中和为某一值的路径（中等, 2021-12）
<!--{
    "tags": ["二叉树", "DFS"],
    "来源": "剑指Offer",
    "编号": "3400",
    "难度": "中等",
    "标题": "二叉树中和为某一值的路径"
}-->

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

