## 剪绳子
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2025-07-08%2016%3A53%3A13&color=yellowgreen&style=flat-square)
[![](https://img.shields.io/static/v1?label=&message=%E4%B8%AD%E7%AD%89&color=yellow&style=flat-square)](../../../README.md#中等)
[![](https://img.shields.io/static/v1?label=&message=%E5%89%91%E6%8C%87Offer&color=green&style=flat-square)](../../../README.md#剑指offer)
[![](https://img.shields.io/static/v1?label=&message=%E6%95%B0%E5%AD%A6&color=blue&style=flat-square)](../../../README.md#数学)

<!--END_SECTION:badge-->
<!--info
tags: [数学]
source: 剑指Offer
level: 中等
number: '1402'
name: 剪绳子
companies: []
-->

<summary><b>问题简述</b></summary>

```txt
将 n 拆分为 m 段（m、n 都是整数，且 n>1 and m>1），求可能的最大乘积；

答案需取模 1e9+7（1000000007）
```

<details><summary><b>详细描述</b></summary>

```txt
给你一根长度为 n 的绳子，请把绳子剪成整数长度的 m 段（m、n都是整数，n>1并且m>1），每段绳子的长度记为 k[0],k[1]...k[m - 1] 。请问 k[0]*k[1]*...*k[m - 1] 可能的最大乘积是多少？例如，当绳子的长度是8时，我们把它剪成长度分别为2、3、3的三段，此时得到的最大乘积是18。

答案需要取模 1e9+7（1000000007），如计算初始结果为：1000000008，请返回 1。

示例 1：
    输入: 2
    输出: 1
    解释: 2 = 1 + 1, 1 × 1 = 1
示例 2:
    输入: 10
    输出: 36
    解释: 10 = 3 + 3 + 4, 3 × 3 × 4 = 36

提示：
    2 <= n <= 1000

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/jian-sheng-zi-ii-lcof
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```

</details>

<!-- <div align="center"><img src="../../../_assets/xxx.png" height="300" /></div> -->

<summary><b>思路</b></summary>

- 本题与“剪绳子1”的区别仅在于 n 的范围；
- 对于较大的 n，使用动态规划可能会超时；

<details><summary><b>Python</b></summary>

```python
class Solution:
    def cuttingRope(self, n: int) -> int:

        if n == 2:
            return 1
        if n == 3:
            return 2

        y = n % 3  # 余数

        if y == 2:
            ret = 3 ** (n // 3) * 2
        elif y == 1:
            ret = 3 ** (n // 3 - 1) * 4
        else:
            ret = 3 ** (n // 3)
        
        return ret % 1000000007
```

</details>

