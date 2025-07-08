## x 的平方根
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2022-10-30%2018%3A01%3A32&color=yellowgreen&style=flat-square)
[![](https://img.shields.io/static/v1?label=&message=%E7%AE%80%E5%8D%95&color=yellow&style=flat-square)](../../../README.md#简单)
[![](https://img.shields.io/static/v1?label=&message=LeetCode&color=green&style=flat-square)](../../../README.md#leetcode)
[![](https://img.shields.io/static/v1?label=&message=%E4%BA%8C%E5%88%86%E6%9F%A5%E6%89%BE&color=blue&style=flat-square)](../../../README.md#二分查找)
[![](https://img.shields.io/static/v1?label=&message=%E7%83%AD%E9%97%A8&color=blue&style=flat-square)](../../../README.md#热门)

<!--END_SECTION:badge-->
<!--START_SECTION:badge-->
<!--END_SECTION:badge-->
<!--info
tags: [二分查找, 热门]
source: LeetCode
level: 简单
number: '0069'
name: x 的平方根
companies: []
-->

> [69. x 的平方根 - 力扣（LeetCode）](https://leetcode.cn/problems/sqrtx/)

<summary><b>问题简述</b></summary>

```txt
给你一个非负整数 x ，计算并返回 x 的 算术平方根 (整数部分)。
```

<!-- 
<details><summary><b>详细描述</b></summary>

```txt
```

</details>
-->

<!-- <div align="center"><img src="../../../_assets/xxx.png" height="300" /></div> -->

<summary><b>思路: 二分查找</b></summary>

<details><summary><b>Python</b></summary>

```python
class Solution:
    def mySqrt(self, x: int) -> int:
        if x in (0, 1): return x

        l, r = 0, x
        while l < r:
            m = (l + r) // 2
            if m ** 2 <= x < (m + 1) ** 2:
                break
            
            if m ** 2 < x:
                l = m
            else:
                r = m
        
        return m
```

</details>


<summary><b>进阶: 浮点数版本</b></summary>

- 定义 `mySqrt(x: float, e: int)`, 其中 `e` 为小数精度;
- 注: 代码未经过严格测试, 可能存在问题;

<details><summary><b>Python</b></summary>

```python
class Solution:
    def mySqrt(self, x: float, e: int) -> int:
        if x in (0, 1): return x
        
        assert x > 0
        flag = False
        if x < 1:  # 小于 1 的情况
            x = 1 / x
            flag = True
        
        l, r = 0, x
        while l < r:
            m = (l + r) / 2
            if abs(m ** 2 - x) <= 0.1 ** e:
                break
            
            if m ** 2 < x:
                l = m
            else:
                r = m
        
        return 1 / m if flag else m
```

</details>

<!-- 
<summary><b>相关问题</b></summary>

-->
