## 层序遍历二叉树
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2025-07-08%2016%3A53%3A13&color=yellowgreen&style=flat-square)
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
number: '3201'
name: 层序遍历二叉树
companies: []
-->

<summary><b>问题简述</b></summary>

```txt
层序遍历二叉树
```

<details><summary><b>详细描述</b></summary>

```txt
从上到下打印出二叉树的每个节点，同一层的节点按照从左到右的顺序打印。

例如:
    给定二叉树: [3,9,20,null,null,15,7],

        3
    / \
    9  20
        /  \
    15   7
返回：
    [3,9,20,15,7]
 
提示：
    节点总数 <= 1000


来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/cong-shang-dao-xia-da-yin-er-cha-shu-lcof
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```

<!-- <div align="center"><img src="./_assets/xxx.png" height="300" /></div> -->

</details>


<summary><b>思路</b></summary>

- 利用辅助队列 q；
    1. 将树的根结点入队；
    2. 如果 q 不为空，则将头结点出队记为 node；如果 node 的左节点不为空，则将左节点入队；如果 node 的右节点不为空，则将右节点入队；
    3. 重复 2、3，直到 q 为空


<details><summary><b>Python</b></summary>

- `list` 也可以模拟队列，为什么还要用 `collections.deque`？
    - `list.pop(0)` 的时间复杂度为 `O(N)`；而 `deque.popleft()` 只要 `O(1)`；

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution:
    def levelOrder(self, root: TreeNode) -> List[int]:
        from collections import deque

        if not root: return []

        buf = deque([root])  # 队列
        ret = []
        while buf:
            cur = buf.popleft()  # 弹出队列头
            ret.append(cur.val)

            if cur.left:
                buf.append(cur.left)
            if cur.right:
                buf.append(cur.right)
        
        return ret
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
    vector<int> levelOrder(TreeNode* root) {
        
        vector<int> ret;
        queue<TreeNode*> q;  // 辅助队列
        
        if (root)
            q.push(root);

        while (!q.empty()) {
            TreeNode* node = q.front();
            q.pop();

            ret.push_back(node->val);
            if (node->left) {
                q.push(node->left);
            }
            if (node->right) {
                q.push(node->right);
            }
        }

        return ret;
    }
};
```

</details>
