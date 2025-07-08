## 树的子结构
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2022-10-14%2014%3A59%3A33&color=yellowgreen&style=flat-square)
[![](https://img.shields.io/static/v1?label=&message=%E4%B8%AD%E7%AD%89&color=yellow&style=flat-square)](../../../README.md#中等)
[![](https://img.shields.io/static/v1?label=&message=%E5%89%91%E6%8C%87Offer&color=green&style=flat-square)](../../../README.md#剑指offer)
[![](https://img.shields.io/static/v1?label=&message=%E4%BA%8C%E5%8F%89%E6%A0%91/%E6%A0%91&color=blue&style=flat-square)](../../../README.md#二叉树树)
[![](https://img.shields.io/static/v1?label=&message=%E9%80%92%E5%BD%92&color=blue&style=flat-square)](../../../README.md#递归)

<!--END_SECTION:badge-->
<!--info
tags: [二叉树, 递归]
source: 剑指Offer
level: 中等
number: '2600'
name: 树的子结构
companies: []
-->

<summary><b>问题简述</b></summary>

```txt
输入两棵二叉树A和B，判断B是不是A的子结构(约定空树不是任意一个树的子结构)
```

<details><summary><b>详细描述</b></summary>

```txt
输入两棵二叉树A和B，判断B是不是A的子结构。(约定空树不是任意一个树的子结构)

B是A的子结构， 即 A中有出现和B相同的结构和节点值。

例如:
    给定的树 A:
         3
        / \
       4   5
      / \
     1   2
    
    给定的树 B：
       4 
      /
     1
    返回 true，因为 B 与 A 的一个子树拥有相同的结构和节点值。

示例 1：
    输入：A = [1,2,3], B = [3,1]
    输出：false
示例 2：
    输入：A = [3,4,5,1,2], B = [4,1]
    输出：true

限制：
    0 <= 节点个数 <= 10000

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/shu-de-zi-jie-gou-lcof
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```

<!-- <div align="center"><img src="./_assets/xxx.png" height="300" /></div> -->

</details>


<summary><b>思路：递归遍历</b></summary>

> [树的子结构（先序遍历 + 包含判断，清晰图解）](https://leetcode-cn.com/problems/shu-de-zi-jie-gou-lcof/solution/mian-shi-ti-26-shu-de-zi-jie-gou-xian-xu-bian-li-p/)


1. 确定 b 是 a（以 a 为根节点） 的子结构：
    - 如果 b 与 a 是否相等；
    - 递归判断 b 和 a 的**左、右子节点是否分别相等**；
    - 如果 b 比 a 先达到空节点，则 b 是 a 的子结构；
2. 遍历 A 中的每个节点 a（以任意顺序遍历均可），然后确定 B 是否为 a 的子结构；

<details><summary><b>Python</b></summary>

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution:
    def isSubStructure(self, A: TreeNode, B: TreeNode) -> bool:
        # 题目设定如果原始输入的 B 是空树，则不是 A 的子树
        # 显然当 A 是空树是，B 也不是 A 的子树
        if not B or not A: return False

        def dfs(a, b):
            """同时从 a 和 b 的根节点开始，判断 b 是不是 a 的子树"""
            # 递归中止条件：
            #   如果 b 先于 a 达到空节点，则 b 是 a 的子树；反之不是；所以需要先判断 b
            if not b: return True
            if not a: return False

            if a.val == b.val:  # 如果当前节点值相同，分别递归判断 a 和 b 的左右子树（这里不要求顺序）
                return dfs(a.left, b.left) and dfs(a.right, b.right)
            else:
                return False
        
        # 遍历 A 中的每个节点，判断以其作为根节点，是否包含 B
        #   这里任意遍历顺序都可以，只要能达到 A 中每个节点
        
        # 先序
        # return dfs(A, B) or self.isSubStructure(A.left, B) or self.isSubStructure(A.right, B)
        
        # 中序
        # return self.isSubStructure(A.left, B) or dfs(A, B) or self.isSubStructure(A.right, B)
        
        # 后序
        return self.isSubStructure(A.left, B) or self.isSubStructure(A.right, B) or dfs(A, B)
```

</details>

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
    bool isSubStructure(TreeNode* A, TreeNode* B) {
        if (A == nullptr || B == nullptr) return false;

        return isSubTree(A, B)
            || isSubStructure(A->left, B) 
            || isSubStructure(A->right, B);
    }

    bool isSubTree(TreeNode* A, TreeNode* B) {
        if (B == nullptr) return true; 
        if (A == nullptr) return false;

        if (A->val == B->val) {
            return isSubTree(A->left, B->left) && isSubTree(A->right, B->right);
        } else {
            return false;
        }
    }
};
```

</details>

