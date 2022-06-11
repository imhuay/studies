## 剑指Offer_1001_斐波那契数列（简单, 2021-11）
<!--{
    "tags": ["DP", "记忆化搜索"],
    "来源": "剑指Offer",
    "编号": "1001",
    "难度": "简单",
    "标题": "斐波那契数列"
}-->

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
- 法2）DP（记忆化搜索），因为每个答案只与固定的前两个结果有关，因此可以使用滚动 DP；


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

