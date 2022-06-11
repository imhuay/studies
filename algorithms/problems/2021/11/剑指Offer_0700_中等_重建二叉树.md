## 剑指Offer_0700_重建二叉树（中等, 2021-11）
<!--{
    "tags": ["二叉树", "分治", "经典"],
    "来源": "剑指Offer",
    "编号": "0700",
    "难度": "中等",
    "标题": "重建二叉树"
}-->

<summary><b>问题简述</b></summary>

```txt
给出二叉树前序遍历和中序遍历的结果，重建该二叉树并返回其根节点。
```

<details><summary><b>详细描述</b></summary>

```txt
输入某二叉树的前序遍历和中序遍历的结果，请构建该二叉树并返回其根节点。
假设输入的前序遍历和中序遍历的结果中都不含重复的数字。

示例 1:
    Input: preorder = [3,9,20,15,7], inorder = [9,3,15,20,7]
    Output: [3,9,20,null,null,15,7]
示例 2:
    Input: preorder = [-1], inorder = [-1]
    Output: [-1]

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/zhong-jian-er-cha-shu-lcof
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```

<!-- <div align="center"><img src="../../../_assets/xxx.png" height="300" /></div> -->

</details>


<summary><b>思路</b></summary>

- 前序遍历，节点按照 `[ 根节点 | 左子树 | 右子树 ]` 的顺序输出。
- 中序遍历，节点按照 `[ 左子树 | 根节点 | 右子树 ]` 的顺序输出。
- 可知：
    - 前序遍历的首元素为根节点 node 的值。
    - 在中序遍历的结果中搜索根节点的索引 ，可将**中序遍历**划分为 `[ 左子树 | 根节点 | 右子树 ]` 。
    - 根据中序遍历中的左（右）子树的节点数量，可将**前序遍历**划分为 `[ 根节点 | 左子树 | 右子树 ]` 。

<div align="center"><img src="../../../_assets/剑指Offer_0007_中等_重建二叉树.png" height="300" /></div>


<details><summary><b>Python</b></summary>

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution:
    def buildTree(self, preorder: List[int], inorder: List[int]) -> TreeNode:
        if len(preorder) < 1 or len(inorder) < 1:  # 两个都判断一下
            return None

        # 建立根节点
        root_val = preorder[0]
        root = TreeNode(root_val)
        root_idx = inorder.index(root_val)  # 找到根节点在中序遍历的位置

        # 截取左子树的 preorder 和 inorder，递归建立左子树
        inorder_left = inorder[:root_idx]
        preorder_left = preorder[1: len(inorder_left) + 1]
        root.left = self.buildTree(preorder_left, inorder_left)
        # 截取右子树的 preorder 和 inorder，递归建立右子树
        inorder_right = inorder[root_idx + 1:]
        preorder_right = preorder[-len(inorder_right):]
        root.right = self.buildTree(preorder_right, inorder_right)
        return root
```

- 更常见的写法会使用一个字典来保存每个节点在中序遍历中的位置，取代`root_idx = inorder.index(root_val)` 这一步，
- 但是这样做就必须每次从最初的 preorder 和 inorder 中截取左右子树的片段，代码会变得比较复杂，传递的参数比较多，故没有采用这种写法；

</details>

