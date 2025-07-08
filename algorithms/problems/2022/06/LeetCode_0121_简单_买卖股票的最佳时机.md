## 买卖股票的最佳时机
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2025-07-08%2016%3A53%3A13&color=yellowgreen&style=flat-square)
[![](https://img.shields.io/static/v1?label=&message=%E7%AE%80%E5%8D%95&color=yellow&style=flat-square)](../../../README.md#简单)
[![](https://img.shields.io/static/v1?label=&message=LeetCode&color=green&style=flat-square)](../../../README.md#leetcode)
[![](https://img.shields.io/static/v1?label=&message=%E5%8A%A8%E6%80%81%E8%A7%84%E5%88%92&color=blue&style=flat-square)](../../../README.md#动态规划)

<!--END_SECTION:badge-->
<!--info
tags: [动态规划]
source: LeetCode
level: 简单
number: '0121'
name: 买卖股票的最佳时机
companies: []
-->

<summary><b>问题简述</b></summary>

```txt
给定数组 prices，它的第 i 个元素 prices[i] 表示一支给定股票第 i 天的价格。
你只能进行一次买卖。求最大利润。
```

<details><summary><b>详细描述</b></summary>

```txt
给定一个数组 prices，它的第 i 个元素 prices[i] 表示一支给定股票第 i 天的价格。

你只能选择 某一天 买入这只股票，并选择在 未来的某一个不同的日子 卖出该股票。设计一个算法来计算你所能获取的最大利润。

返回你可以从这笔交易中获取的最大利润。如果你不能获取任何利润，返回 0 。

示例 1：
    输入：[7,1,5,3,6,4]
    输出：5
    解释：在第 2 天（股票价格 = 1）的时候买入，在第 5 天（股票价格 = 6）的时候卖出，最大利润 = 6-1 = 5 。
        注意利润不能是 7-1 = 6, 因为卖出价格需要大于买入价格；同时，你不能在买入前卖出股票。
示例 2：
    输入：prices = [7,6,4,3,1]
    输出：0
    解释：在这种情况下, 没有交易完成, 所以最大利润为 0。

提示：
    1 <= prices.length <= 10^5
    0 <= prices[i] <= 10^4


来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/best-time-to-buy-and-sell-stock
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```

<!-- <div align="center"><img src="./_assets/xxx.png" height="300" /></div> -->

</details>


<summary><b>思路</b></summary>

```txt
1. 遍历 prices，以 min_p 记录当前的最小值（非全局最小值）；
2. 用当前价格 p 减去 min_p，得到当天卖出的利润；
3. 使用 ret 记录遍历过程中的最大利润。
```

- 以上思路只适用于一次买卖的情况；

<details><summary><b>Python</b></summary>

```python
class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        """"""
        ret = 0
        min_p = 10001
        for p in prices:
            min_p = min(p, min_p)
            ret = max(ret, p - min_p)
        
        return ret
```

</details>

