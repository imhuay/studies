## 剑指Offer_5400_二叉搜索树的第k大节点（简单, 2022-01）
<!--{
    "tags": ["二叉树", "dfs"],
    "来源": "剑指Offer",
    "编号": "5400",
    "难度": "简单",
    "标题": "二叉搜索树的第k大节点"
}-->

<summary><b>问题简述</b></summary>

```txt
给定一棵二叉搜索树，请找出其中第 k 大的节点的值。
```

<details><summary><b>详细描述</b></summary>

```txt
给定一棵二叉搜索树，请找出其中第 k 大的节点的值。

示例 1:
    输入: root = [3,1,4,null,2], k = 1
       3
      / \
     1   4
      \
       2
    输出: 4
示例 2:
    输入: root = [5,3,6,2,4,null,null,1], k = 3
           5
          / \
         3   6
        / \
       2   4
      /
     1
    输出: 4

限制：
    1 ≤ k ≤ 二叉搜索树元素个数

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/er-cha-sou-suo-shu-de-di-kda-jie-dian-lcof
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```

<!-- <div align="center"><img src="./_assets/xxx.png" height="300" /></div> -->

</details>


<summary><b>思路</b></summary>

- 根据二叉搜索树的性质，其中序遍历的结果为递增序列；
- 为了得到第 k 大的数，需要递减序列，“反向”中序遍历即可：即按“右中左”的顺序深度搜索（正向为“左中右”）；
- 利用辅助变量提前结束搜索；


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
    int k;
    int ret;

    void inOrder(TreeNode* node) {
        if (node == nullptr) return;

        inOrder(node->right);  // 先遍历右子树
        if (--this->k == 0) {  // 因为 k>0，实际上第 1 大指的是索引为 0 的位置，所以要先 --
            this->ret = node->val;
            return;
        }
        inOrder(node->left);
    }
    
public:
    int kthLargest(TreeNode* root, int k) {
        this->k = k;
        inOrder(root);
        return this->ret;
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
    def kthLargest(self, root: TreeNode, k: int) -> int:

        self.cnt = 0
        self.ret = -1
        
        def dfs(node):
            if node is None:
                return 
            
            dfs(node.right)
            self.cnt += 1
            if self.cnt == k:
                self.ret = node.val
                return 
            dfs(node.left)
        
        dfs(root)
        return self.ret
```

</details>

