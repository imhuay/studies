## n个骰子的点数
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2025-07-08%2016%3A53%3A13&color=yellowgreen&style=flat-square)
[![](https://img.shields.io/static/v1?label=&message=%E4%B8%AD%E7%AD%89&color=yellow&style=flat-square)](../../../README.md#中等)
[![](https://img.shields.io/static/v1?label=&message=%E5%89%91%E6%8C%87Offer&color=green&style=flat-square)](../../../README.md#剑指offer)
[![](https://img.shields.io/static/v1?label=&message=%E5%8A%A8%E6%80%81%E8%A7%84%E5%88%92&color=blue&style=flat-square)](../../../README.md#动态规划)
[![](https://img.shields.io/static/v1?label=&message=%E6%9A%B4%E5%8A%9B%E9%80%92%E5%BD%92%E4%B8%8E%E5%8A%A8%E6%80%81%E8%A7%84%E5%88%92&color=blue&style=flat-square)](../../../README.md#暴力递归与动态规划)

<!--END_SECTION:badge-->
<!--info
tags: [动态规划, dfs2dp]
source: 剑指Offer
level: 中等
number: '6000'
name: n个骰子的点数
companies: []
-->

> [剑指 Offer 60. n个骰子的点数 - 力扣（LeetCode）](https://leetcode.cn/problems/nge-tou-zi-de-dian-shu-lcof/)

<summary><b>问题简述</b></summary>

```txt
把 n 个骰子扔在地上，所有骰子朝上一面的点数之和为 s。
输入 n，打印出 s 的所有可能的值出现的概率（按 s 从小到大排列）。
```

<details><summary><b>详细描述</b></summary>

```txt
把n个骰子扔在地上，所有骰子朝上一面的点数之和为s。输入n，打印出s的所有可能的值出现的概率。

你需要用一个浮点数数组返回答案，其中第 i 个元素代表这 n 个骰子所能掷出的点数集合中第 i 小的那个的概率。

示例 1:
    输入: 1
    输出: [0.16667,0.16667,0.16667,0.16667,0.16667,0.16667]
示例 2:
    输入: 2
    输出: [0.02778,0.05556,0.08333,0.11111,0.13889,0.16667,0.13889,0.11111,0.08333,0.05556,0.02778]

限制：
    1 <= n <= 11
```

</details>

<!-- <div align="center"><img src="../../../_assets/xxx.png" height="300" /></div> -->

<summary><b>思路1：从暴力递归到动态规划</b></summary>

- 定义 `dfs(k)` 返回 k 个骰子产生的可能性序列 `dp`，其中 `dp[i]` 表示 k 个骰子掷出点数 i 的可能数；
- 【递归基】`k=1` 时，`dfs(1)` 返回 `dp = [_, 1, 1, 1, 1, 1, 1]`（为方便编码，`dp[:n]` 为占位符，无实际意义）
- 递归过程即使用 `dfs(k-1)` 返回的 `dp_pre` 生成 `dfs(k)` 的 `dp`；
- 然后根据暴力递归过程直接写出动态规划的代码（已经与原问题解耦）；

<details><summary><b>Python：暴力递归</b></summary>

```python
class Solution:
    def dicesProbability(self, n: int) -> List[float]:

        def dfs(k):
            if k == 1:
                return [1] * 7

            dp_pre = dfs(k - 1)
            dp = [0] * (k * 6 + 1)

            # 遍历方式 1（推荐，不需要判断范围）:
            for i in range(1 * (k - 1), 6 * (k - 1) + 1):  # n - 1 个骰子的点数范围
                for d in range(1, 7):  # 当前骰子掷出的点数
                    dp[i + d] += dp_pre[i]

            # 遍历方式 2：
            # for i in range(1 * k, 6 * k + 1):  # n 个骰子的点数范围
            #     for d in range(1, 7):  # 当前骰子掷出的点数
            #         if 1 * (k - 1) <= i - d <= 6 * (k - 1):  # 边界判断
            #             dp[i] += dp_pre[i - d]

            return dp

        dp = dfs(n)
        return [x / (6 ** n) for x in dp[n:]]
```

</details>

<details><summary><b>Python：动态规划</b></summary>

```python
class Solution:
    def dicesProbability(self, n: int) -> List[float]:

        dp = [1] * 7

        for k in range(2, n + 1):
            dp_pre = dp
            dp = [0] * (k * 6 + 1)
            for i in range(1 * k, 6 * k + 1):  # n 个骰子的点数范围
                for d in range(1, 7):  # 当前骰子掷出的点数
                    if 1 * (k - 1) <= i - d <= 6 * (k - 1):
                        dp[i] += dp_pre[i - d]

        return [x / (6 ** n) for x in dp[n:]]
```

</details>


<summary><b>思路2：从“跳台阶”理解本题</b></summary>

- “跳台阶”的递推公式为：`dp[i] = dp[i-1] + dp[i-2]`；
- 在本题中，可以看做目标台阶数为 `i`，每次可以跳 `1~6` 步；对 `k` 个骰子，`i` 的范围为 `k ~ 6*k`，每次都是从 `n-1` 个骰子的可能性出发；
- 因此本题的递推公式为：`dp[k][i] = dp[k-1][i-1] + dp[k-1][i-2] + .. + dp[k-1][i-6]`；
    - 同时因为每一轮只和上一轮相关，可以使用两个数组滚动优化空间；
        > 也可以只是用一个数组，参考：[n个骰子的点数 - 路漫漫我不畏](https://leetcode-cn.com/problems/nge-tou-zi-de-dian-shu-lcof/solution/nge-tou-zi-de-dian-shu-dong-tai-gui-hua-ji-qi-yo-3/)
- 代码同上。
