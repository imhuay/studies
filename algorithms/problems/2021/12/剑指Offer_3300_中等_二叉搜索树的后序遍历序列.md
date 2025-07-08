## 二叉搜索树的后序遍历序列
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2025-07-08%2016%3A53%3A13&color=yellowgreen&style=flat-square)
[![](https://img.shields.io/static/v1?label=&message=%E4%B8%AD%E7%AD%89&color=yellow&style=flat-square)](../../../README.md#中等)
[![](https://img.shields.io/static/v1?label=&message=%E5%89%91%E6%8C%87Offer&color=green&style=flat-square)](../../../README.md#剑指offer)
[![](https://img.shields.io/static/v1?label=&message=%E4%BA%8C%E5%8F%89%E6%A0%91/%E6%A0%91&color=blue&style=flat-square)](../../../README.md#二叉树树)

<!--END_SECTION:badge-->
<!--info
tags: [二叉树]
source: 剑指Offer
level: 中等
number: '3300'
name: 二叉搜索树的后序遍历序列
companies: []
-->

<summary><b>问题简述</b></summary>

```txt
输入一个整数数组，判断该数组是不是某二叉搜索树的后序遍历结果。
```

<details><summary><b>详细描述</b></summary>

```txt
输入一个整数数组，判断该数组是不是某二叉搜索树的后序遍历结果。如果是则返回 true，否则返回 false。假设输入的数组的任意两个数字都互不相同。

参考以下这颗二叉搜索树：

     5
    / \
   2   6
  / \
 1   3

示例 1：
    输入: [1,6,3,2,5]
    输出: false
示例 2：
    输入: [1,3,2,6,5]
    输出: true

提示：
    数组长度 <= 1000

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/er-cha-sou-suo-shu-de-hou-xu-bian-li-xu-lie-lcof
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```

</details>

<!-- <div align="center"><img src="../../../_assets/xxx.png" height="300" /></div> -->

<summary><b>思路</b></summary>

- 记后序遍历的结果为 `p`，则 `p` 有如下结论：
    - `p[-1]` 为根节点：
    - `p[:-1]` 可以划分为左右子树两个部分，分别记为 `pl` 和 `pr`；
- 而该二叉树为二叉搜索树，又有 `all(x < p[-1] for x in pl)` 和 `all(x > p[-1] for x in pr)`
- 然后递归判断左右子树是否满足以上性质即可；

<details><summary><b>Python</b></summary>

```python
class Solution:
    def verifyPostorder(self, postorder: List[int]) -> bool:

        def dfs(p):
            if not p: return True  # 记空树为二叉搜索树

            root_val = p[-1]
            pl = []  # 左子树
            for idx, x in enumerate(p):
                if x < root_val:  # 题目规定 p 中元素互不相等
                    pl.append(x)
                else:
                    break
            
            pr = p[idx: -1]  # 右子树
            flag = all(x > root_val for x in pr)
            return flag and dfs(pl) and dfs(pr)

        return dfs(postorder)
```

</details>

<details><summary><b>Python：优化</b></summary>

- 可以用索引范围代替 `pl` 和 `pr`，避免使用额外空间；
- 还有其他判断方法，这里是严格按照上面的思路来写的；
    > [二叉搜索树的后序遍历序列（递归分治 / 单调栈，清晰图解）](https://leetcode-cn.com/problems/er-cha-sou-suo-shu-de-hou-xu-bian-li-xu-lie-lcof/solution/mian-shi-ti-33-er-cha-sou-suo-shu-de-hou-xu-bian-6/)

```python
class Solution:
    def verifyPostorder(self, postorder: List[int]) -> bool:
        p = postorder

        def dfs(l, r):  # [l, r]
            if l >= r: return True

            root_val = p[r]
            cnt = 0  # 记录小于root的节点数量，即左子树
            for i in range(l, r):  # 这里踩了个坑，不能直接用 i 代替 cnt，因为退出循环时不能保证 i 一定指向第一个大于 root 的元素，比如右子树为空的情况
                if p[i] > root_val:
                    break
                else:
                    cnt += 1
            flag = all(p[i] > root_val for i in range(l + cnt, r))
            return flag and dfs(l, l + cnt - 1) and dfs(l + cnt, r - 1)

        return dfs(0, len(p) - 1)
```

</details>

