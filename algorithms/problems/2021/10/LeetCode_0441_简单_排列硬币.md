## 排列硬币
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2022-10-14%2014%3A59%3A33&color=yellowgreen&style=flat-square)
[![](https://img.shields.io/static/v1?label=&message=%E7%AE%80%E5%8D%95&color=yellow&style=flat-square)](../../../README.md#简单)
[![](https://img.shields.io/static/v1?label=&message=LeetCode&color=green&style=flat-square)](../../../README.md#leetcode)
[![](https://img.shields.io/static/v1?label=&message=%E4%BA%8C%E5%88%86%E6%9F%A5%E6%89%BE&color=blue&style=flat-square)](../../../README.md#二分查找)
[![](https://img.shields.io/static/v1?label=&message=%E6%95%B0%E5%AD%A6&color=blue&style=flat-square)](../../../README.md#数学)

<!--END_SECTION:badge-->
<!--info
tags: [二分查找, 数学]
source: LeetCode
level: 简单
number: '0441'
name: 排列硬币
companies: []
-->

<summary><b>问题简述</b></summary>

```txt
你总共有 n 枚硬币，并计划将它们按阶梯状排列。对于一个由 k 行组成的阶梯，其第 i 行必须正好有 i 枚硬币。阶梯的最后一行 可能 是不完整的。

给你一个数字 n ，计算并返回可形成 完整阶梯行 的总行数。

示例 1：
    输入：n = 5
    输出：2
    解释：因为第三行不完整，所以返回 2 。

提示：
    1 <= n <= 2^31 - 1

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/arranging-coins
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```

<div align="center"><img src="../../../_assets/arrangecoins1-grid.jpeg" height="150" /></div>


<summary><b>思路</b></summary>

<details><summary><b>法1）Python：二分查找</b></summary>

- 因为时间复杂度为 `O(logN)`，所以直接在 `[1, n]` 的范围里找即可

```python
class Solution:
    def arrangeCoins(self, n: int) -> int:
        left, right = 1, n
        while left < right:
            mid = (left + right + 1) // 2
            if mid * (mid + 1) <= 2 * n:
                left = mid
            else:
                right = mid - 1
        return left

```

</details>


<details><summary><b>法2）Python：数学公式</b></summary>

- 解方程 $(1+x)*x/2 = n$；
- 去掉小于 0 的解，保留：$x=(-1+\sqrt{8n+1})/2$

```python
class Solution:
    def arrangeCoins(self, n: int) -> int:
        return int((-1 + (8 * n + 1) ** 0.5) / 2)
```

</details>
