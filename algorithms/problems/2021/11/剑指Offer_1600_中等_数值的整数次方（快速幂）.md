## 数值的整数次方（快速幂）
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2025-07-08%2016%3A53%3A13&color=yellowgreen&style=flat-square)
[![](https://img.shields.io/static/v1?label=&message=%E4%B8%AD%E7%AD%89&color=yellow&style=flat-square)](../../../README.md#中等)
[![](https://img.shields.io/static/v1?label=&message=%E5%89%91%E6%8C%87Offer&color=green&style=flat-square)](../../../README.md#剑指offer)
[![](https://img.shields.io/static/v1?label=&message=%E9%80%92%E5%BD%92&color=blue&style=flat-square)](../../../README.md#递归)
[![](https://img.shields.io/static/v1?label=&message=%E4%BA%8C%E5%88%86%E6%9F%A5%E6%89%BE&color=blue&style=flat-square)](../../../README.md#二分查找)
[![](https://img.shields.io/static/v1?label=&message=%E7%BB%8F%E5%85%B8&color=blue&style=flat-square)](../../../README.md#经典)

<!--END_SECTION:badge-->
<!--info
tags: [递归, 二分法, 经典]
source: 剑指Offer
level: 中等
number: '1600'
name: 数值的整数次方（快速幂）
companies: []
-->

<summary><b>问题简述</b></summary>

```txt
实现快速幂算法，即 pow(x, n)，不使用库函数；
```

<details><summary><b>详细描述</b></summary>

```txt
实现 pow(x, n) ，即计算 x 的 n 次幂函数（即，xn）。不得使用库函数，同时不需要考虑大数问题。

示例 1：
    输入：x = 2.00000, n = 10
    输出：1024.00000
示例 2：
    输入：x = 2.10000, n = 3
    输出：9.26100
示例 3：
    输入：x = 2.00000, n = -2
    输出：0.25000
    解释：2-2 = 1/22 = 1/4 = 0.25

提示：
    -100.0 < x < 100.0
    -2^31 <= n <= 2^31-1
    -10^4 <= x^n <= 10^4

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/shu-zhi-de-zheng-shu-ci-fang-lcof
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```

</details>

<summary><b>思路</b></summary>

- 直接连乘 n 次会报超时；
- 从二分角度理解快速幂

    ```python
    3^20      
    = (3^2)^10       # 当指数为偶数时，对指数除2取整，底数平方
    = (9^2)^5   
    = (81^2)^2 * 81  # 当指数为奇数时，对指数除2取整，底数平方，同时再乘一个当前的底数（这里是 81）
    = (6561^2)^1 * 81
    = 43046721^0 * 81 * 43046721
    = 1 * 81 * 43046721
    ```

    > [数值的整数次方（快速幂，清晰图解）](https://leetcode-cn.com/problems/shu-zhi-de-zheng-shu-ci-fang-lcof/solution/mian-shi-ti-16-shu-zhi-de-zheng-shu-ci-fang-kuai-s/)

<!-- <div align="center"><img src="../../../_assets/xxx.png" height="300" /></div> -->

<details><summary><b>Python</b></summary>

```python
class Solution:
    def myPow(self, x: float, n: int) -> float:
        if x == 0: 
            return 0
        
        if n == 0:
            return 1

        if n < 0: 
            x = 1 / x
            n = -n

        ret = 1
        while n:
            if n & 1: 
                ret *= x
            x *= x
            n >>= 1
        return ret
```

</details>

