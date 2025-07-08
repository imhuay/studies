## 整数除法
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2022-10-14%2014%3A59%3A33&color=yellowgreen&style=flat-square)
[![](https://img.shields.io/static/v1?label=&message=%E4%B8%AD%E7%AD%89&color=yellow&style=flat-square)](../../../README.md#中等)
[![](https://img.shields.io/static/v1?label=&message=%E5%89%91%E6%8C%87Offer2&color=green&style=flat-square)](../../../README.md#剑指offer2)
[![](https://img.shields.io/static/v1?label=&message=%E4%BA%8C%E5%88%86%E6%9F%A5%E6%89%BE&color=blue&style=flat-square)](../../../README.md#二分查找)
[![](https://img.shields.io/static/v1?label=&message=%E7%BB%8F%E5%85%B8&color=blue&style=flat-square)](../../../README.md#经典)

<!--END_SECTION:badge-->
<!--info
tags: [二分, 经典]
source: 剑指Offer2
level: 中等
number: '001'
name: 整数除法
companies: []
-->

<summary><b>问题简述</b></summary>

```txt
给定两个整数 a 和 b ，求它们的除法的商 a/b。
要求不得使用乘号 '*'、除号 '/' 以及求余符号 '%'。
```

<details><summary><b>详细描述</b></summary>

```txt
给定两个整数 a 和 b ，求它们的除法的商 a/b ，要求不得使用乘号 '*'、除号 '/' 以及求余符号 '%'。

注意：
    整数除法的结果应当截去（truncate）其小数部分，例如：truncate(8.345) = 8 以及 truncate(-2.7335) = -2
    假设我们的环境只能存储 32 位有符号整数，其数值范围是 [−2^31, 2^31−1]。本题中，如果除法结果溢出，则返回 2^31 − 1

示例 1：
    输入：a = 15, b = 2
    输出：7
    解释：15/2 = truncate(7.5) = 7
示例 2：
    输入：a = 7, b = -3
    输出：-2
    解释：7/-3 = truncate(-2.33333..) = -2
示例 3：
    输入：a = 0, b = 1
    输出：0
示例 4：
    输入：a = 1, b = 1
    输出：1
提示:
    -2^31 <= a, b <= 2^31 - 1
    b != 0

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/xoh6Oh
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```

</details>

<!-- <div align="center"><img src="../../../_assets/xxx.png" height="300" /></div> -->

<summary><b>思路1：减法（超时）</b></summary>

- 用 a 循环减 b，直到为负；
- 越界讨论：因为是整数除法，实际的越界情况就一种，就是 `a=-2^31,b=-1`
- 极端情况：`a=2^31-1, b=1` 要循坏 `2^31-1` 次；

<details><summary><b>Python</b></summary>

```python
class Solution:
    def divide(self, a: int, b: int) -> int:
        assert b != 0
        
        MAX = 2 ** 31 - 1
        if a == 0: return 0
        if a == -2 ** 31 and b == -1: return MAX  # 越界
        
        # 转为两个整数操作
        sign = 1
        if a < 0:
            sign *= -1
            a = -a
        
        if b < 0:
            sign *= -1
            b = -b

        # 循坏减去 b
        ret = -1
        while a > 0:
            a -= b
            ret += 1

        if a == 0:  # 整除的情况
            ret += 1 
        
        return sign * ret
```

</details>


<summary><b>思路2：二分思想</b></summary>

1. 初始化返回值 `ret = 0`
2. `a > b` 时，不断将 `b` 翻倍（乘 2），直到再翻倍一次就大于 `a`，记翻倍后的数为 `tmp_b`，翻的倍数为 `tmp`，然后将 `ret` 加上 `tmp`、`a` 减去 `tmp_b`；
3. `a` 减去 `tmp_b` 后循环以上过程，直到 `a` 小于 `b`；

```
以 a = 32, b = 3 为例，模拟过程如下：

初始化 ret = 0
第一轮：
    32 / (3*2*2*2) = t1 / (1*2*2*2)  # 再乘一个 2 会大于 32
    32 / 24 = 1 = t1 / 8 -> t1 = 8
    (32 - 24) / 3 = 8 / 3
    ret += t1 -> 8
第二轮：
    8 / (3*2) = t2 / (1*2)
    8 / 6 = 1 = t2 / 2 -> t2 = 2
    (8 - 6) / 3 = 0
    ret += t2 -> 10
因为 2 < 3 退出循环
```

<details><summary><b>Python</b></summary>

```python
class Solution:
    def divide(self, a: int, b: int) -> int:
        assert b != 0
        if a == 0: return 0
        if a == -2**31 and b == -1: return 2 ** 31 - 1
        sign = 1 if (a > 0 and b > 0) or (a < 0 and b < 0) else -1
        a = a if a > 0 else -a
        b = b if b > 0 else -b
        
        # if a < b: return 0

        ret = 0
        while a >= b:
            tmp, tmp_b = 1, b
            while tmp_b * 2 < a:
                tmp_b *= 2
                tmp *= 2
            
            ret += tmp
            a -= tmp_b

        return ret * sign
```

</details>