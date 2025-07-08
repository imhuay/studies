## 序列化二叉树
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2025-07-08%2016%3A53%3A13&color=yellowgreen&style=flat-square)
[![](https://img.shields.io/static/v1?label=&message=%E5%9B%B0%E9%9A%BE&color=yellow&style=flat-square)](../../../README.md#困难)
[![](https://img.shields.io/static/v1?label=&message=%E5%89%91%E6%8C%87Offer&color=green&style=flat-square)](../../../README.md#剑指offer)
[![](https://img.shields.io/static/v1?label=&message=%E4%BA%8C%E5%8F%89%E6%A0%91/%E6%A0%91&color=blue&style=flat-square)](../../../README.md#二叉树树)

<!--END_SECTION:badge-->
<!--info
tags: [二叉树]
source: 剑指Offer
level: 困难
number: '3700'
name: 序列化二叉树
companies: []
-->

<summary><b>问题简述</b></summary>

```txt
实现两个函数，分别用来序列化和反序列化二叉树。
```

<details><summary><b>详细描述</b></summary>

```txt
请实现两个函数，分别用来序列化和反序列化二叉树。

你需要设计一个算法来实现二叉树的序列化与反序列化。这里不限定你的序列 / 反序列化算法执行逻辑，你只需要保证一个二叉树可以被序列化为一个字符串并且将这个字符串反序列化为原始的树结构。

提示：输入输出格式与 LeetCode 目前使用的方式一致，详情请参阅 LeetCode 序列化二叉树的格式。你并非必须采取这种方式，你也可以采用其他的方法解决这个问题。

示例：
    输入：root = [1,2,3,null,null,4,5]
    输出：[1,2,3,null,null,4,5]

注意：本题与主站 297 题相同：https://leetcode-cn.com/problems/serialize-and-deserialize-binary-tree/

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/xu-lie-hua-er-cha-shu-lcof
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```

</details>

<!-- <div align="center"><img src="../../../_assets/xxx.png" height="300" /></div> -->

~~<summary><b>思路1：中序遍历+前序/后序遍历</b></summary>~~

- **只适用于树种节点不重复的情况**；
- 单独的中序/前序/后序能不能还原二叉树；
- 但是中序 + 前序/后序就可以；
- 因此可以序列化可以输出，中序+前序/后序的结果，反序列化时再用他们还原；

<details><summary><b>Python</b></summary>

```python
class Codec:

    def serialize(self, root):
        """Encodes a tree to a single string.

        :type root: TreeNode
        :rtype: str
        """

        inorder = []
        preorder = []

        def in_dfs(r):
            if not r: return

            in_dfs(r.left)
            inorder.append(r.val)
            in_dfs(r.right)

        def pre_dfs(r):
            if not r: return

            preorder.append(r.val)
            pre_dfs(r.left)
            pre_dfs(r.right)

        in_dfs(root)
        pre_dfs(root)
        return str(inorder) + ', ' + str(preorder)

    def deserialize(self, data):
        """Decodes your encoded data to tree.

        :type data: str
        :rtype: TreeNode
        """
        inorder, preorder = eval(data)

        def dfs(inorder, preorder):
            if not inorder and not preorder: return

            root_val = preorder[0]
            root = TreeNode(root_val)
            root_idx = inorder.index(root_val)

            root.left = dfs(inorder[:root_idx], preorder[1:root_idx + 1])
            root.right = dfs(inorder[root_idx + 1:], preorder[root_idx + 1:])
            
            return root
        
        return dfs(inorder, preorder)

# Your Codec object will be instantiated and called as such:
# codec = Codec()
# codec.deserialize(codec.serialize(root))
```

</details>


<summary><b>思路2：层序遍历</b></summary>

- 无论是序列化还是反序列化，都需要用到辅助队列；
- 层序遍历的缺点是可能会保存很多无效的空节点；

<details><summary><b>Python</b></summary>

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Codec:

    def serialize(self, root):
        """Encodes a tree to a single string.
        
        :type root: TreeNode
        :rtype: str
        """
        from collections import deque

        if not root: return '[]'  # 空判断

        buf = deque([root])
        ret = []
        while buf:
            p = buf.popleft()
            if p:
                ret.append(p.val)
                buf.append(p.left)
                buf.append(p.right)
            else:  # 注意空节点也要保存
                ret.append(None)

        return str(ret)

    def deserialize(self, data):
        """Decodes your encoded data to tree.
        
        :type data: str
        :rtype: TreeNode
        """
        from collections import deque

        data = eval(data)  # 利用 python 的 eval 函数方便的将字符串还原为列表
        if not data: return None  # 空判断

        i = 0  # 记录当前节点在 data 中的位置
        root = TreeNode(data[i])
        i += 1
        buf = deque([root])

        while buf:
            p = buf.popleft()
            if data[i] is not None:  # 因为在 if 中 0 也是 False，所以保险起见用 is not None 来判断
                p.left = TreeNode(data[i])
                buf.append(p.left)  # 新节点入队，当生成下一层的节点时，依然按照从左往右的顺序
            i += 1
            if data[i] is not None:
                p.right = TreeNode(data[i])
                buf.append(p.right)
            i += 1

        return root


# Your Codec object will be instantiated and called as such:
# codec = Codec()
# codec.deserialize(codec.serialize(root))
```

</details>
