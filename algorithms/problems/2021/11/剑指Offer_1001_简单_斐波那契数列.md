## 斐波那契数列
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2025-07-08%2016%3A53%3A13&color=yellowgreen&style=flat-square)
[![](https://img.shields.io/static/v1?label=&message=%E7%AE%80%E5%8D%95&color=yellow&style=flat-square)](../../../README.md#简单)
[![](https://img.shields.io/static/v1?label=&message=%E5%89%91%E6%8C%87Offer&color=green&style=flat-square)](../../../README.md#剑指offer)
[![](https://img.shields.io/static/v1?label=&message=%E5%8A%A8%E6%80%81%E8%A7%84%E5%88%92&color=blue&style=flat-square)](../../../README.md#动态规划)

<!--END_SECTION:badge-->
<!--info
tags: [dp, 记忆化搜索]
source: 剑指Offer
level: 简单
number: '1001'
name: 斐波那契数列
companies: []
-->

<summary><b>问题简述</b></summary>

```txt
输入 n ，求斐波那契（Fibonacci）数列的第 n 项
```

<details><summary><b>详细描述</b></summary>

```txt
写一个函数，输入 n ，求斐波那契（Fibonacci）数列的第 n 项（即 F(N)）。斐波那契数列的定义如下：
    F(0) = 0,   F(1) = 1
    F(N) = F(N - 1) + F(N - 2), 其中 N > 1.
斐波那契数列由 0 和 1 开始，之后的斐波那契数就是由之前的两数相加而得出。

答案需要取模 1e9+7（1000000007），如计算初始结果为：1000000008，请返回 1。

示例 1：
    输入：n = 2
    输出：1
示例 2：
    输入：n = 5
    输出：5

提示：
    0 <= n <= 100

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/fei-bo-na-qi-shu-lie-lcof
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```

<!-- <div align="center"><img src="../../../_assets/xxx.png" height="300" /></div> -->

</details>


<summary><b>思路</b></summary>

- 法1）递归
- 法2）dp（记忆化搜索），因为每个答案只与固定的前两个结果有关，因此可以使用滚动 dp；


<details><summary><b>Python：递归（会超时）</b></summary>

```python
class Solution:
    
    def fib(self, n: int) -> int:
        if n == 0:
            return 0
        if n == 1:
            return 1
        
        MAX = 1000000007
        return (self.fib(n-1) + self.fib(n-2)) % MAX
```

</details>


<details><summary><b>Python：动态规划</b></summary>

```python
class Solution:
    
    def fib(self, n: int) -> int:
        if n == 0:
            return 0
        if n == 1:
            return 1
        
        MAX = 1000000007

        dp = [0, 1]  # 因为每个答案只与固定的前两个结果有关，所以只需要“记忆”两个答案
        for _ in range(n - 1):
            dp[0], dp[1] = dp[1], dp[0] + dp[1]
        
        return dp[1] % MAX
```

</details>
