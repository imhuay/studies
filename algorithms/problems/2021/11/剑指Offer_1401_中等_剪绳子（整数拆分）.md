## 剪绳子（整数拆分）
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2022-10-16%2016%3A24%3A13&color=yellowgreen&style=flat-square)
[![](https://img.shields.io/static/v1?label=&message=%E4%B8%AD%E7%AD%89&color=yellow&style=flat-square)](../../../README.md#中等)
[![](https://img.shields.io/static/v1?label=&message=%E5%89%91%E6%8C%87Offer&color=green&style=flat-square)](../../../README.md#剑指offer)
[![](https://img.shields.io/static/v1?label=&message=%E5%8A%A8%E6%80%81%E8%A7%84%E5%88%92&color=blue&style=flat-square)](../../../README.md#动态规划)
[![](https://img.shields.io/static/v1?label=&message=%E8%B4%AA%E5%BF%83&color=blue&style=flat-square)](../../../README.md#贪心)
[![](https://img.shields.io/static/v1?label=&message=%E6%95%B0%E5%AD%A6&color=blue&style=flat-square)](../../../README.md#数学)

<!--END_SECTION:badge-->
<!--info
tags: [动态规划, 贪心, 数学]
source: 剑指Offer
level: 中等
number: '1401'
name: 剪绳子（整数拆分）
companies: []
-->

<summary><b>问题简述</b></summary>

```txt
给定一个正整数 n，将其拆分为至少两个正整数的和，使这些整数的乘积最大化。返回最大乘积。
```

<details><summary><b>详细描述</b></summary>

```txt
给你一根长度为 n 的绳子，请把绳子剪成整数长度的 m 段（m、n都是整数，n>1并且m>1），每段绳子的长度记为 k[0],k[1]...k[m-1] 。请问 k[0]*k[1]*...*k[m-1] 可能的最大乘积是多少？例如，当绳子的长度是8时，我们把它剪成长度分别为2、3、3的三段，此时得到的最大乘积是18。

示例 1：
    输入: 2
    输出: 1
    解释: 2 = 1 + 1, 1 × 1 = 1
示例 2:
    输入: 10
    输出: 36
    解释: 10 = 3 + 3 + 4, 3 × 3 × 4 = 36
提示：
    2 <= n <= 58

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/jian-sheng-zi-lcof
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```

</details>

<summary><b>思路1：动态规划</b></summary>

<!-- <div align="center"><img src="../../../_assets/xxx.png" height="300" /></div> -->

- 在不使用任何数学结论的前提下，可以把本题当做纯 dp 来做：

<details><summary><b>Python（写法1）</b></summary>

> LeetCode 官方题解中的写法：[整数拆分](https://leetcode-cn.com/problems/integer-break/solution/zheng-shu-chai-fen-by-leetcode-solution/)

```python
class Solution:
    def integerBreak(self, n: int) -> int:
        dp = [1] * (n + 1)

        for i in range(2, n + 1):
            for j in range(1, i):
                # 状态定义：dp[i] 表示长度为 i 并拆分成至少两个正整数后的最大乘积（i>=1）
                #   j * (i - j)   表示将 i 拆分成 j 和 i-j，且 i-j 不再拆分
                #   j * dp[i - j] 表示将 i 拆分成 j 和 i-j，且 i-j 会继续拆分，dp[i-j] 即为继续拆分的最优结果（最优子结构）
                dp[i] = max(dp[i], max(j * (i - j), j * dp[i - j]))

        return dp[n]
```

</details>

<details><summary><b>Python（写法2，推荐）</b></summary>

> 《剑指Offer》中的写法

```python
class Solution:
    def cuttingRope(self, n: int) -> int:
        # 对于 n = 2、3 的情况，直接硬编码
        if n == 2:
            return 1
        if n == 3:
            return 2

        # 状态定义：dp[i] 表示长度为 i 并拆分成至少两个正整数后的最大乘积（i>3）
        #   当 i <= 3 时，不满足该定义，此时不拆效率最高
        #   初始状态（dp[0] 仅用于占位）
        dp = [0,1,2,3] + [0] * (n - 3) 

        for i in range(4, n + 1):
            for j in range(2, i):
                dp[i] = max(dp[i], dp[i-j] * dp[j])

        return dp[n]
```

</details>


<summary><b>思路2：数学/贪心</b></summary>

- 数学上可证：尽可能按长度为 3 切，如果剩余 4，则按 2、2 切；
  > 证明见：[剪绳子1（数学推导 / 贪心思想，清晰图解）](https://leetcode-cn.com/problems/jian-sheng-zi-lcof/solution/mian-shi-ti-14-i-jian-sheng-zi-tan-xin-si-xiang-by/)

- **简述**：当 `x >= 4` 时，有 `2(x-2) = 2x - 4 >= x`；简言之，对任意大于等于 4 的因子，都可以拆成 2 和 x-2 而不损失性能；因此只需考虑拆成 2 或 3 两种情况（1除外）；而由于 `2*2 > 3*1` 和 `3*3 > 2*2*2`，可知最多使用两个 2；

<details><summary><b>Python</b></summary>

```python
class Solution:
    def cuttingRope(self, n: int) -> int:
        import math
        if n <= 3:
            return n - 1
        
        a, b = n // 3, n % 3
        if b == 1:
            return int(math.pow(3, a - 1) * 4)
        elif b == 2:
            return int(math.pow(3, a) * 2)
        else:
            return int(math.pow(3, a))
```

</details>
