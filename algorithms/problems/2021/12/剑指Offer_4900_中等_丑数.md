## 丑数
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2025-07-08%2016%3A53%3A13&color=yellowgreen&style=flat-square)
[![](https://img.shields.io/static/v1?label=&message=%E4%B8%AD%E7%AD%89&color=yellow&style=flat-square)](../../../README.md#中等)
[![](https://img.shields.io/static/v1?label=&message=%E5%89%91%E6%8C%87Offer&color=green&style=flat-square)](../../../README.md#剑指offer)
[![](https://img.shields.io/static/v1?label=&message=%E5%8A%A8%E6%80%81%E8%A7%84%E5%88%92&color=blue&style=flat-square)](../../../README.md#动态规划)
[![](https://img.shields.io/static/v1?label=&message=%E7%BB%8F%E5%85%B8&color=blue&style=flat-square)](../../../README.md#经典)

<!--END_SECTION:badge-->
<!--info
tags: [动态规划, 经典]
source: 剑指Offer
level: 中等
number: '4900'
name: 丑数
companies: []
-->

<summary><b>问题简述</b></summary>

```txt
我们把只包含质因子 2、3 和 5 的数称作丑数（Ugly Number）。
求按从小到大的顺序的第 n 个丑数。
```

<details><summary><b>详细描述</b></summary>

```txt
我们把只包含质因子 2、3 和 5 的数称作丑数（Ugly Number）。求按从小到大的顺序的第 n 个丑数。

示例:
    输入: n = 10
    输出: 12
    解释: 1, 2, 3, 4, 5, 6, 8, 9, 10, 12 是前 10 个丑数。
说明:
    1 是丑数。
    n 不超过1690。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/chou-shu-lcof
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```

</details>

<!-- <div align="center"><img src="../../../_assets/xxx.png" height="300" /></div> -->

<summary><b>思路：暴力解</b></summary>

- 根据丑数的定义，有如下推论：
    - 一个丑数乘以 2、3、5 之后，还是丑数；
    - 从 1 开始，对每个丑数都乘以 2、3、5，再加入丑数序列（移除重复），那么不会产生遗漏；
- 对已有的丑数乘以 2、3、5，取其中大于已知最大丑数的最小值；

<details><summary><b>Python</b></summary>

```python
class Solution:
    def nthUglyNumber(self, n: int) -> int:

        dp = [1]
        for i in range(1, n):
            M = dp[-1]  # 当前最大丑数

            tmp = []
            for x in dp[::-1]:  # 逆序遍历
                if x * 5 < M:
                    break
                    
                if x * 2 > M:
                    tmp.append(x * 2)
                if x * 3 > M:
                    tmp.append(x * 3)
                if x * 5 > M:
                    tmp.append(x * 5)

            dp.append(min(tmp))

        return dp[-1]
```

</details>

<summary><b>思路：动态规划</b></summary>

- 暴力解中存在大量重复计算，可以考虑动态规划；

<details><summary><b>Python</b></summary>

- 代码解读：[丑数，清晰的推导思路](https://leetcode-cn.com/problems/chou-shu-lcof/solution/chou-shu-ii-qing-xi-de-tui-dao-si-lu-by-mrsate/)

```python
class Solution:
    def nthUglyNumber(self, n: int) -> int:

        dp = [1] * n
        p1, p2, p3 = 0, 0, 0  # 三指针归并

        for i in range(1, n):
            n2, n3, n5 = dp[p1] * 2, dp[p2] * 3, dp[p3] * 5
            dp[i] = min(n2, n3, n5)

            # 去重：使用 if 而不是 elif
            if dp[i] == n2:
                p1 += 1
            if dp[i] == n3:
                p2 += 1
            if dp[i] == n5:
                p3 += 1

        return dp[-1]

```

</details>
