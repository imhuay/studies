## 两数相除
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2025-07-08%2016%3A53%3A13&color=yellowgreen&style=flat-square)
[![](https://img.shields.io/static/v1?label=&message=%E4%B8%AD%E7%AD%89&color=yellow&style=flat-square)](../../../README.md#中等)
[![](https://img.shields.io/static/v1?label=&message=LeetCode&color=green&style=flat-square)](../../../README.md#leetcode)
[![](https://img.shields.io/static/v1?label=&message=%E4%BD%8D%E8%BF%90%E7%AE%97&color=blue&style=flat-square)](../../../README.md#位运算)
[![](https://img.shields.io/static/v1?label=&message=%E4%BA%8C%E5%88%86%E6%9F%A5%E6%89%BE&color=blue&style=flat-square)](../../../README.md#二分查找)

<!--END_SECTION:badge-->
<!--info
tags: [位运算, 二分查找]
source: LeetCode
level: 中等
number: '0029'
name: 两数相除
companies: []
-->

<summary><b>问题简述</b></summary>

```txt
不使用乘法、除法和 mod 运算符，返回两数相除的整数部分，如 10/3 返回 3。
```

<details><summary><b>详细描述</b></summary>

```txt
给定两个整数，被除数 dividend 和除数 divisor。将两数相除，要求不使用乘法、除法和 mod 运算符。

返回被除数 dividend 除以除数 divisor 得到的商。

整数除法的结果应当截去（truncate）其小数部分，例如：truncate(8.345) = 8 以及 truncate(-2.7335) = -2

示例 1:
    输入: dividend = 10, divisor = 3
    输出: 3
    解释: 10/3 = truncate(3.33333..) = truncate(3) = 3
示例 2:
    输入: dividend = 7, divisor = -3
    输出: -2
    解释: 7/-3 = truncate(-2.33333..) = -2

提示：
    被除数和除数均为 32 位有符号整数。
    除数不为 0。
    假设我们的环境只能存储 32 位有符号整数，其数值范围是 [−2^31,  2^31 − 1]。本题中，如果除法结果溢出，则返回 2^31 − 1。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/divide-two-integers
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```

</details>


<summary><b>思路</b></summary>

<details><summary><b>Python：二分查找</b></summary>

```python
class Solution:
    def divide(self, dividend: int, divisor: int) -> int:
        """"""
        INT_MIN, INT_MAX = -2 ** 31, 2 ** 31 - 1

        # 按照题目要求，只有一种情况会溢出
        if dividend == INT_MIN and divisor == -1:
            return INT_MAX

        sign = (dividend > 0 and divisor > 0) or (dividend < 0 and divisor < 0)

        # 核心操作
        def div(a, b):
            if a < b:
                return 0

            cnt = 1
            tb = b
            while (tb + tb) <= a:
                cnt += cnt
                tb += tb

            return cnt + div(a - tb, b)

        ret = div(abs(dividend), abs(divisor))
        return ret if sign else -ret
```

**核心操作说明**，以 60 / 8 为例：
```txt
第一轮 div(60, 8): 8 -> 32 时停止，因为 32 + 32 > 60，返回 4
第二轮 div(28, 8): 8 -> 16 时停止，因为 16 + 16 > 28，返回 2
第三轮 div(8, 8):  8 -> 8  时停止，因为 8  +  8 >  8，返回 1
第三轮 div(0, 8):  因为 0 < 8，返回 0

因此结果为 1 + 2 + 4 = 7
```

</details>
