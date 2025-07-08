## 零钱兑换
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2022-10-16%2016%3A55%3A02&color=yellowgreen&style=flat-square)
[![](https://img.shields.io/static/v1?label=&message=%E4%B8%AD%E7%AD%89&color=yellow&style=flat-square)](../../../README.md#中等)
[![](https://img.shields.io/static/v1?label=&message=LeetCode&color=green&style=flat-square)](../../../README.md#leetcode)
[![](https://img.shields.io/static/v1?label=&message=%E5%8A%A8%E6%80%81%E8%A7%84%E5%88%92&color=blue&style=flat-square)](../../../README.md#动态规划)
[![](https://img.shields.io/static/v1?label=&message=%E6%9A%B4%E5%8A%9B%E9%80%92%E5%BD%92%E4%B8%8E%E5%8A%A8%E6%80%81%E8%A7%84%E5%88%92&color=blue&style=flat-square)](../../../README.md#暴力递归与动态规划)

<!--END_SECTION:badge-->
<!--info
tags: [dfs2dp, 动态规划]
source: LeetCode
level: 中等
number: '0322'
name: 零钱兑换
companies: []
-->

<summary><b>问题简述</b></summary>

```txt
给你一个整数数组 coins ，表示不同面额的硬币；以及一个整数 amount ，表示总金额。
计算并返回可以凑成总金额所需的 最少的硬币个数 。如果没有任何一种硬币组合能组成总金额，返回 -1 。
你可以认为每种硬币的数量是无限的。
```
> [322. 零钱兑换 - 力扣（LeetCode）](https://leetcode-cn.com/problems/coin-change/)

<!-- 
<details><summary><b>详细描述</b></summary>

```txt
```

</details>
-->


<!-- <div align="center"><img src="../../../_assets/xxx.png" height="300" /></div> -->

<summary><b>思路：完全背包</b></summary>

- 定义 `dfs(a)` 表示凑成金额 `a` 需要的最少硬币数；
- **递归基**：1）显然 `dfs(0) = 0`；2）当 `a` 小于币值时，返回无穷大，表示无效结果；

<details><summary><b>Python：递归</b></summary>

```python
class Solution:
    def coinChange(self, coins: List[int], amount: int) -> int:

        from functools import lru_cache

        N = len(coins)

        @lru_cache(maxsize=None)
        def dfs(a):
            if a == 0: return 0
            if a < 0: return float('inf')

            ret = float('inf')
            for i in range(N):
                if a >= coins[i]:
                    ret = min(ret, dfs(a - coins[i]) + 1)
            return ret

        ret = dfs(amount)
        return -1 if ret == float('inf') else ret
```

</details>


<details><summary><b>Python：动态规划 写法1）根据递归过程改写</b></summary>

```python
class Solution:
    def coinChange(self, coins: List[int], amount: int) -> int:

        N = len(coins)
        dp = [float('inf')] * (amount + 1)
        dp[0] = 0

        for a in range(1, amount + 1):
            for i in range(N):
                if a >= coins[i]:
                    dp[a] = min(dp[a], dp[a - coins[i]] + 1)
        
        return -1 if dp[-1] == float('inf') else dp[-1]
```

</details>

<details><summary><b>Python：动态规划 写法2）先遍历“物品”，在遍历“容量”</b></summary>

> 关于先后遍历两者的区别见[完全背包 - 代码随想录](https://programmercarl.com/背包问题理论基础完全背包.html)，本题中没有区别；

```python
class Solution:
    def coinChange(self, coins: List[int], amount: int) -> int:

        N = len(coins)
        dp = [float('inf')] * (amount + 1)
        dp[0] = 0

        for i in range(N):
            for a in range(coins[i], amount + 1):
                dp[a] = min(dp[a], dp[a - coins[i]] + 1)
        
        return -1 if dp[-1] == float('inf') else dp[-1]
```

</details>
