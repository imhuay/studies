## 零钱兑换II
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2025-07-08%2016%3A53%3A13&color=yellowgreen&style=flat-square)
[![](https://img.shields.io/static/v1?label=&message=%E4%B8%AD%E7%AD%89&color=yellow&style=flat-square)](../../../README.md#中等)
[![](https://img.shields.io/static/v1?label=&message=LeetCode&color=green&style=flat-square)](../../../README.md#leetcode)
[![](https://img.shields.io/static/v1?label=&message=%E5%8A%A8%E6%80%81%E8%A7%84%E5%88%92&color=blue&style=flat-square)](../../../README.md#动态规划)

<!--END_SECTION:badge-->
<!--info
tags: [动态规划]
source: LeetCode
level: 中等
number: '0518'
name: 零钱兑换II
companies: []
-->

<summary><b>问题简述</b></summary>

```txt
给你一个整数数组 coins 表示不同面额的硬币，另给一个整数 amount 表示总金额。
请你计算并返回可以凑成总金额的硬币组合数。如果任何硬币组合都无法凑出总金额，返回 0 。
假设每一种面额的硬币有无限个。 
```
> [518. 零钱兑换 II - 力扣（LeetCode）](https://leetcode-cn.com/problems/coin-change-2/)

<!-- 
<details><summary><b>详细描述</b></summary>

```txt
```

</details>
-->


<!-- <div align="center"><img src="../../../_assets/xxx.png" height="300" /></div> -->

<summary><b>思路1：递归</b></summary>

- 定义 `dfs(a, i)` 表示目标钱数为 `a` 且从第 `i` 种硬币开始取能得到的组合数；
    > “从第 `i` 种硬币开始取”具体指第 `i` 种之后的硬币可以任意取，前面的 `i-1` 种不能取，详见代码；
- **递归基**
    1. 规定 `dfs(0,i) == 1`；
    2. 隐含中止条件：当 `coins[i] > j` 时，`dfs(a,i) == 0`；

<details><summary><b>Python</b></summary>

```python
class Solution:
    def change(self, amount: int, coins: List[int]) -> int:
        from functools import lru_cache

        N = len(coins)

        @lru_cache(maxsize=None)
        def dfs(a, i):  # 目标钱数为 `a` 且从第 `i` 种硬币开始取能得到的组合数
            if a == 0: return 1

            ret = 0
            while i < N:
                if (x := coins[i]) <= a:
                    ret += dfs(a - x, i)
                i += 1

            return ret

        return dfs(amount, 0)
```

</details>


<summary><b>思路2：动态规划——基于完全背包的组合数问题</b></summary>

- 定义 `dp[a]` 表示构成目标值 `i` 的组合数；
- 转移方程 `dp[a] += dp[a - coins[i]]`，当 `a >= coins[i]` 时；
- 初始状态 `dp[0] = 1`；
- 关键点：先遍历“物品”（这里是硬币），在遍历“容量”（这里是金额）；
    > 关于先后遍历两者的区别见[完全背包 - 代码随想录](https://programmercarl.com/背包问题理论基础完全背包.html)；

<details><summary><b>Python：动态规划</b></summary>

```python
class Solution:
    def change(self, amount: int, coins: List[int]) -> int:
        from functools import lru_cache

        N = len(coins)
        dp = [0] * (amount + 1)
        dp[0] = 1

        for i in range(N):
            x = coins[i]
            for j in range(x, amount + 1):
                dp[j] += dp[j - x]
        
        return dp[amount]
```

</details>

