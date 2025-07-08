## 完全平方数
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2025-07-08%2016%3A53%3A13&color=yellowgreen&style=flat-square)
[![](https://img.shields.io/static/v1?label=&message=%E4%B8%AD%E7%AD%89&color=yellow&style=flat-square)](../../../README.md#中等)
[![](https://img.shields.io/static/v1?label=&message=LeetCode&color=green&style=flat-square)](../../../README.md#leetcode)
[![](https://img.shields.io/static/v1?label=&message=%E5%8A%A8%E6%80%81%E8%A7%84%E5%88%92&color=blue&style=flat-square)](../../../README.md#动态规划)
[![](https://img.shields.io/static/v1?label=&message=%E6%9A%B4%E5%8A%9B%E9%80%92%E5%BD%92%E4%B8%8E%E5%8A%A8%E6%80%81%E8%A7%84%E5%88%92&color=blue&style=flat-square)](../../../README.md#暴力递归与动态规划)

<!--END_SECTION:badge-->
<!--info
tags: [dfs2dp]
source: LeetCode
level: 中等
number: '0279'
name: 完全平方数
companies: []
-->

<summary><b>问题简述</b></summary>

```txt
给你一个整数 n ，返回 和为 n 的完全平方数的最少数量 。

完全平方数 是一个整数，其值等于另一个整数的平方；换句话说，其值等于一个整数自乘的积。例如，1、4、9 和 16 都是完全平方数，而 3 和 11 不是。
```
> [279. 完全平方数 - 力扣（LeetCode）](https://leetcode-cn.com/problems/perfect-squares/)

<!-- 
<details><summary><b>详细描述</b></summary>

```txt
```

</details>
-->


<!-- <div align="center"><img src="../../../_assets/xxx.png" height="300" /></div> -->

<summary><b>思路1：朴素完全背包（超时）</b></summary>

- 定义 `dfs(i, j)` 表示用 `1~i` 的完全平方数凑出 `j` 需要的最小数量；
- 不能 AC，仅离线验证了正确性；
    <!-- - 优化一下剪枝应该是能过的 -->


<details><summary><b>Python：递归</b></summary>

```python
class Solution:
    def numSquares(self, n: int) -> int:
        from functools import lru_cache

        @lru_cache(maxsize=None)
        def dfs(i, j):
            if i == 0 and j == 0: return 0  # 显然
            if i == 0: return float('inf')  # 凑不出的情况，返回不可能，注意此时 j != 0
            # if i == 1: return j

            ret = j  # 最大值为 j，因为任意数字最差都可以用 1 组成
            times = 0  # i 使用的次数，0 次也考虑在内
            while (x := (i ** 2) * times) <= j:
                ret = min(ret, dfs(i - 1, j - x) + times)
                times += 1

            return ret

        N = int(n ** 0.5)  # 可以使用数字的范围
        return dfs(N, n)
```

</details>


<details><summary><b>Python：动态规划（从递归修改而来）</b></summary>

```python
class Solution:
    def numSquares(self, n: int) -> int:
        from functools import lru_cache

        N = int(n ** 0.5)
        dp = [[0] * (n + 1) for _ in range(N + 1)]
        dp[0] = [float('inf')] * (n + 1)
        dp[0][0] = 0

        for i in range(1, N + 1):
            for j in range(1, n + 1):
                dp[i][j] = j
                times = 0
                while (x := i * i * times) <= j:
                    dp[i][j] = min(dp[i][j], dp[i - 1][j - x] + times)
                    times += 1

        return dp[-1][-1]
```

</details>


<summary><b>思路2：完全背包（优化）</b></summary>

- 定义 `dfs(j)` 表示目标和为`j`时需要完全平方数的最少个数；
    > 这里隐含了完全平方数的范围 `i*i <= j`；
- 【递归基】`j == 0` 时，返回 `0`；
<!-- - 这里的递归含义并不直观，直接看代码吧； -->

<details><summary><b>Python：递归</b></summary>

```python
class Solution:
    def numSquares(self, n: int) -> int:
        from functools import lru_cache

        @lru_cache(maxsize=None)
        def dfs(j):
            if j == 0: return 0

            # 这里设置初始化为一个上界
            #   本题中初始化为无穷大、j（全部 1）、4（四平方和定理）都可以；
            #   为了使解法更通用，故初始化为无穷大
            ret = float('inf')
            i = 1
            while (x := i * i) <= j:
                ret = min(ret, dfs(j - x) + 1)
                i += 1

            return ret

        return dfs(n)
```

</details>

<details><summary><b>Python：动态规划（从递归修改而来）</b></summary>

```python
class Solution:
    def numSquares(self, n: int) -> int:

        dp = [i for i in range(n + 1)]
        dp[0] = 0

        for j in range(1, n + 1):
            i = 1
            while (x := i * i) <= n:
                dp[j] = min(dp[j], dp[j - x] + 1)
                i += 1

        return dp[-1]
```

</details>


<details><summary><b>Python：动态规划（更快的写法）</b></summary>

- 交换内外层遍历顺序（本题无影响），减小 `j` 的遍历范围；
    > 关于遍历“物品”和“容量”的顺序影响，见：[零钱兑换 - 代码随想录](https://programmercarl.com/0322.零钱兑换.html)

```python
class Solution:
    def numSquares(self, n: int) -> int:

        dp = [i for i in range(n + 1)]
        dp[0] = 0

        i = 1
        while (x := i * i) <= n:
            for j in range(x, n + 1):
                dp[j] = min(dp[j], dp[j - x] + 1)
            i += 1

        return dp[-1]
```

</details>


<summary><b>其他思路</b></summary>

- 数学（时间复杂度 $O(\sqrt{n})$）：[完全平方数 - 力扣官方题解](https://leetcode-cn.com/problems/perfect-squares/solution/wan-quan-ping-fang-shu-by-leetcode-solut-t99c/)
    > [四平方和定理](https://baike.baidu.com/item/四平方和定理)证明了任意一个正整数都可以被表示为至多四个正整数的平方和；
- BFS：[完全平方数 - 自来火](https://leetcode-cn.com/problems/perfect-squares/solution/python3zui-ji-chu-de-bfstao-lu-dai-ma-gua-he-ru-me/)
