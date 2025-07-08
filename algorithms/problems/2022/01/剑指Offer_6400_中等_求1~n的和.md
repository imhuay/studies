## 求1~n的和
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2022-10-14%2014%3A59%3A33&color=yellowgreen&style=flat-square)
[![](https://img.shields.io/static/v1?label=&message=%E4%B8%AD%E7%AD%89&color=yellow&style=flat-square)](../../../README.md#中等)
[![](https://img.shields.io/static/v1?label=&message=%E5%89%91%E6%8C%87Offer&color=green&style=flat-square)](../../../README.md#剑指offer)
[![](https://img.shields.io/static/v1?label=&message=%E9%80%92%E5%BD%92&color=blue&style=flat-square)](../../../README.md#递归)

<!--END_SECTION:badge-->
<!--info
tags: [递归]
source: 剑指Offer
level: 中等
number: '6400'
name: 求1~n的和
companies: []
-->

<summary><b>问题简述</b></summary>

```txt
求 1+2+...+n ，要求不能使用乘除法、for、while、if、else、switch、case等关键字及三目运算符。
```

<details><summary><b>详细描述</b></summary>

```txt
求 1+2+...+n ，要求不能使用乘除法、for、while、if、else、switch、case等关键字及条件判断语句（A?B:C）。

示例 1：
    输入: n = 3
    输出: 6
示例 2：
    输入: n = 9
    输出: 45

限制：
    1 <= n <= 10000

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/qiu-12n-lcof
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```

</details>

<!-- <div align="center"><img src="../../../_assets/xxx.png" height="300" /></div> -->

<summary><b>思路</b></summary>

- 通过“短路”中止递归；
- 在 Python 中 `and` 操作如果最后结果为真，返回最后一个表达式的值，`or` 操作如果结果为真，返回第一个结果为真的表达式的值（写法2）；

<details><summary><b>Python：写法1</b></summary>

```python
class Solution:
    def __init__(self):
        self.res = 0

    def sumNums(self, n: int) -> int:
        n > 1 and self.sumNums(n - 1)  # 当 n <= 1 时，因为短路导致递归中止
        self.res += n
        return self.res
```

</details>

<details><summary><b>Python：写法2</b></summary>

```python
class Solution:
    def sumNums(self, n: int) -> int:
        return n > 0 and (n + self.sumNums(n-1))
```

</details>

