## 剑指Offer_1002_跳台阶（简单, 2021-11）
<!--{
    "tags": ["DP"],
    "来源": "剑指Offer",
    "编号": "1002",
    "难度": "简单",
    "标题": "跳台阶"
}-->

<summary><b>问题简述</b></summary>

```txt
规定一次可以跳1级台阶或2级台阶。求跳上一个 n 级台阶总共有多少种跳法。
```

<details><summary><b>详细描述</b></summary>

```txt
一只青蛙一次可以跳上1级台阶，也可以跳上2级台阶。求该青蛙跳上一个 n 级的台阶总共有多少种跳法。

答案需要取模 1e9+7（1000000007），如计算初始结果为：1000000008，请返回 1。

示例 1：
    输入：n = 2
    输出：2
示例 2：
    输入：n = 7
    输出：21
示例 3：
    输入：n = 0
    输出：1
提示：
    0 <= n <= 100

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/qing-wa-tiao-tai-jie-wen-ti-lcof
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```

<!-- <div align="center"><img src="../../../_assets/xxx.png" height="300" /></div> -->

</details>


<summary><b>思路</b></summary>

- 本题实际上就是求斐波那契数列，跳上 n 级台阶的方法数 `f(n) = f(n-1) + f(n-2)`，
- 只是初始状态不同，这里是 `f(0) = 1, f(1) = 1`；


<details><summary><b>Python：动态规划</b></summary>

```python
class Solution:
    def numWays(self, n: int) -> int:
        MAX = 1000000007

        dp = [1, 1]  # 
        for _ in range(n - 1):
            dp[0], dp[1] = dp[1], dp[0] + dp[1]
        
        return dp[1] % MAX if n > 0 else dp[0]
```

</details>

