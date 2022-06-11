## LeetCode_0096_不同的二叉搜索树（中等, 2022-03）
<!--{
    "tags": ["动态规划"],
    "来源": "LeetCode",
    "难度": "中等",
    "编号": "0096",
    "标题": "不同的二叉搜索树",
    "公司": []
}-->

<summary><b>问题简述</b></summary>

```txt
给你一个整数 n ，求恰由 n 个节点组成且节点值从 1 到 n 互不相同的 二叉搜索树 有多少种？返回满足题意的二叉搜索树的种数。
```
> [96. 不同的二叉搜索树 - 力扣（LeetCode）](https://leetcode-cn.com/problems/unique-binary-search-trees/)

<!-- 
<details><summary><b>详细描述</b></summary>

```txt
```

</details>
-->


<!-- <div align="center"><img src="../../../_assets/xxx.png" height="300" /></div> -->

<summary><b>思路：动态规划</b></summary>

- 对一个有序数组，无论值是多少，它能构成的方法数都是一样的；
- 对一个长度为 `n` 的有序数组，取第 `i` 个值作为根节点，分成左右两个规模分别为 `l=i-1` 和 `r=n-i` 的子问题；
    - 则选择该节点作为根节点的方法数 `=` 左子树的方法数 `*` 右子树的方法数；
    - 得递推公式： `dp(n) = sum( dp(i-1) * dp(n-i) )`，其中 `i in [1, n+1)`；
- 实际上本题就是一个卡特兰数的实例；

<details><summary><b>Python：递归写法</b></summary>

```python
class Solution:
    def numTrees(self, n: int) -> int:

        from functools import lru_cache

        @lru_cache(maxsize=None)
        def dp(n):
            if n in (0, 1): return 1

            ret = 0
            for i in range(1, n + 1):   # 选择第 i 个数字作为根节点
                l, r = i - 1, n - i     # 此时左右子树的节点个数
                ret += dp(l) * dp(r)    # 左边 l 个节点的方法数 * 右边 r 个节点的方法数
            return ret
        
        return dp(n)
```

</details>


<details><summary><b>Python：迭代写法（略）</b></summary>

```python
```

</details>