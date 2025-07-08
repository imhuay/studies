## 表示数值的字符串
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2022-10-14%2014%3A59%3A33&color=yellowgreen&style=flat-square)
[![](https://img.shields.io/static/v1?label=&message=%E4%B8%AD%E7%AD%89&color=yellow&style=flat-square)](../../../README.md#中等)
[![](https://img.shields.io/static/v1?label=&message=%E5%89%91%E6%8C%87Offer&color=green&style=flat-square)](../../../README.md#剑指offer)
[![](https://img.shields.io/static/v1?label=&message=%E5%AD%97%E7%AC%A6%E4%B8%B2&color=blue&style=flat-square)](../../../README.md#字符串)
[![](https://img.shields.io/static/v1?label=&message=%E6%9C%89%E9%99%90%E7%8A%B6%E6%80%81%E8%87%AA%E5%8A%A8%E6%9C%BA&color=blue&style=flat-square)](../../../README.md#有限状态自动机)

<!--END_SECTION:badge-->
<!--info
tags: [字符串, 有限状态自动机]
source: 剑指Offer
level: 中等
number: '2000'
name: 表示数值的字符串
companies: []
-->

<summary><b>问题简述</b></summary>

```txt
请实现一个函数用来判断字符串是否表示数值（包括整数和小数）。
```

<details><summary><b>详细描述</b></summary>

```txt
请实现一个函数用来判断字符串是否表示数值（包括整数和小数）。

数值（按顺序）可以分成以下几个部分：

    1. 若干空格
    2. 一个 小数 或者 整数
    3. （可选）一个 'e' 或 'E' ，后面跟着一个 整数
    4. 若干空格

小数（按顺序）可以分成以下几个部分：
    1. （可选）一个符号字符（'+' 或 '-'）
    2. 下述格式之一：
        1. 至少一位数字，后面跟着一个点 '.'
        2. 至少一位数字，后面跟着一个点 '.' ，后面再跟着至少一位数字
        3. 一个点 '.' ，后面跟着至少一位数字

整数（按顺序）可以分成以下几个部分：
    1. （可选）一个符号字符（'+' 或 '-'）
    2. 至少一位数字

部分数值列举如下：
    ["+100", "5e2", "-123", "3.1416", "-1E-16", "0123"]
部分非数值列举如下：
    ["12e", "1a3.14", "1.2.3", "+-5", "12e+5.4"]

示例 1：
    输入：s = "0"
    输出：true
示例 2：
    输入：s = "e"
    输出：false
示例 3：
    输入：s = "."
    输出：false
示例 4：
    输入：s = "    .1  "
    输出：true
 
提示：
    1 <= s.length <= 20
    s 仅含英文字母（大写和小写），数字（0-9），加号 '+' ，减号 '-' ，空格 ' ' 或者点 '.' 。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/biao-shi-shu-zhi-de-zi-fu-chuan-lcof
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```

</details>

<!-- <div align="center"><img src="../../../_assets/xxx.png" height="300" /></div> -->

<summary><b>思路：有限状态自动机</b></summary>

<div align="center"><img src="../../../_assets/剑指Offer_020_中等_表示数值的字符串.png" height="300" /></div>

- 其中合法的结束状态有：2, 3, 7, 8

> [表示数值的字符串（有限状态自动机，清晰图解） - Krahets](https://leetcode-cn.com/problems/biao-shi-shu-zhi-de-zi-fu-chuan-lcof/solution/mian-shi-ti-20-biao-shi-shu-zhi-de-zi-fu-chuan-y-2/)

<details><summary><b>Python</b></summary>

```python
class Solution:
    def isNumber(self, s: str) -> bool:
        # '.'
        # ' '
        # 's': sign
        # 'd': digit
        # 'e': e/E
        states = [
            {' ': 0, 's': 1, 'd': 2, '.': 4},   # 0. start 'blank'
            {'d': 2, '.': 4},                   # 1. 'sign' before 'e'
            {'d': 2, '.': 3, 'e': 5, ' ': 8},   # 2. 'digit' before 'dot'
            {'d': 3, 'e': 5, ' ': 8},           # 3. 'digit' after 'dot'
            {'d': 3},                           # 4. 'digit' after 'dot' ('blank' before 'dot')
            {'s': 6, 'd': 7},                   # 5. 'e'
            {'d': 7},                           # 6. 'sign' after 'e'
            {'d': 7, ' ': 8},                   # 7. 'digit' after 'e'
            {' ': 8}                            # 8. end with 'blank'
        ]

        p = 0  # 开始状态 0
        for c in s:
            if '0' <= c <= '9':
                t = 'd'  # digit
            elif c in "+-":
                t = 's'  # sign
            elif c in "eE":
                t = 'e'  # e or E
            elif c in ". ":
                t = c  # dot, blank
            else:
                t = '?'  # unknown

            if t not in states[p]:
                return False

            p = states[p][t]

        return p in (2, 3, 7, 8)
```

</details>

