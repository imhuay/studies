## 剑指Offer_5501_求二叉树的深度（简单, 2022-01）
<!--{
    "tags": ["二叉树"],
    "来源": "剑指Offer",
    "编号": "5501",
    "难度": "简单",
    "标题": "求二叉树的深度"
}-->

<summary><b>问题简述</b></summary>

```txt
输入一棵二叉树的根节点，求该树的深度。
```

<details><summary><b>详细描述</b></summary>

```txt
输入一棵二叉树的根节点，求该树的深度。从根节点到叶节点依次经过的节点（含根、叶节点）形成树的一条路径，最长路径的长度为树的深度。

例如：
    给定二叉树 [3,9,20,null,null,15,7]，
    
        3
       / \
      9  20
        /  \
       15   7
    返回它的最大深度 3 。

提示：
    节点总数 <= 10000

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/er-cha-shu-de-shen-du-lcof
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```

<!-- <div align="center"><img src="./_assets/xxx.png" height="300" /></div> -->

</details>


<summary><b>思路</b></summary>

- 递归公式：`最大深度 := 1 + 子树的最大深度`


<details><summary><b>C++</b></summary>

```cpp
/**
 * Definition for a binary tree node.
 * struct TreeNode {
 *     int val;
 *     TreeNode *left;
 *     TreeNode *right;
 *     TreeNode(int x) : val(x), left(NULL), right(NULL) {}
 * };
 */
class Solution {
public:
    int maxDepth(TreeNode* root) {
        if (root == NULL) return 0;

        return 1 + max(maxDepth(root->left), maxDepth(root->right));
    }
};
```

</details>


<details><summary><b>Python</b></summary>

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution:
    def maxDepth(self, root: TreeNode) -> int:

        def dfs(node):
            if node is None:
                return 0

            return 1 + max(dfs(node.left), dfs(node.right))

        # def dfs(node):  # 可以看做是一个后序遍历的过程
        #     if node is None:
        #         return 0
            
        #     lh = dfs(node.left)
        #     # ...
        #     rh = dfs(node.right)
        #     # ...
        #     return 1 + max(lh, rh)

        return dfs(root)
```

</details>

