## 买卖股票的最佳时机II
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2025-07-08%2016%3A53%3A13&color=yellowgreen&style=flat-square)
[![](https://img.shields.io/static/v1?label=&message=%E4%B8%AD%E7%AD%89&color=yellow&style=flat-square)](../../../README.md#中等)
[![](https://img.shields.io/static/v1?label=&message=LeetCode&color=green&style=flat-square)](../../../README.md#leetcode)
[![](https://img.shields.io/static/v1?label=&message=%E5%8A%A8%E6%80%81%E8%A7%84%E5%88%92&color=blue&style=flat-square)](../../../README.md#动态规划)
[![](https://img.shields.io/static/v1?label=&message=%E8%B4%AA%E5%BF%83&color=blue&style=flat-square)](../../../README.md#贪心)
[![](https://img.shields.io/static/v1?label=&message=%E7%83%AD%E9%97%A8&color=blue&style=flat-square)](../../../README.md#热门)

<!--END_SECTION:badge-->
<!--info
tags: [动态规划, 贪心, 热门]
source: LeetCode
level: 中等
number: '0122'
name: 买卖股票的最佳时机II
companies: []
-->

<summary><b>问题简述</b></summary>

```txt
给定数组 prices ，其中 prices[i] 是一支给定股票第 i 天的价格。
设计一个算法来计算你所能获取的最大利润。你可以尽可能地完成更多的交易（多次买卖一支股票）。
```

<details><summary><b>详细描述</b></summary>

```txt
给定一个数组 prices ，其中 prices[i] 是一支给定股票第 i 天的价格。

设计一个算法来计算你所能获取的最大利润。你可以尽可能地完成更多的交易（多次买卖一支股票）。

注意：你不能同时参与多笔交易（你必须在再次购买前出售掉之前的股票）。

示例 1:
    输入: prices = [7,1,5,3,6,4]
    输出: 7
    解释: 在第 2 天（股票价格 = 1）的时候买入，在第 3 天（股票价格 = 5）的时候卖出, 这笔交易所能获得利润 = 5-1 = 4 。
        随后，在第 4 天（股票价格 = 3）的时候买入，在第 5 天（股票价格 = 6）的时候卖出, 这笔交易所能获得利润 = 6-3 = 3 。
示例 2:
    输入: prices = [1,2,3,4,5]
    输出: 4
    解释: 在第 1 天（股票价格 = 1）的时候买入，在第 5 天 （股票价格 = 5）的时候卖出, 这笔交易所能获得利润 = 5-1 = 4 。
        注意你不能在第 1 天和第 2 天接连购买股票，之后再将它们卖出。因为这样属于同时参与了多笔交易，你必须在再次购买前出售掉之前的股票。
示例 3:
    输入: prices = [7,6,4,3,1]
    输出: 0
    解释: 在这种情况下, 没有交易完成, 所以最大利润为 0。

提示：
    1 <= prices.length <= 3 * 10^4
    0 <= prices[i] <= 10^4

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/best-time-to-buy-and-sell-stock-ii
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```

</details>

<!-- <div align="center"><img src="../../../_assets/xxx.png" height="300" /></div> -->

<summary><b>思路1：动态规划</b></summary>

TODO

<details><summary><b>Python</b></summary>

```python
```

</details>


<summary><b>思路2：贪心</b></summary>

> [买卖股票的最佳时机 II - 力扣官方题解](https://leetcode-cn.com/problems/best-time-to-buy-and-sell-stock-ii/solution/mai-mai-gu-piao-de-zui-jia-shi-ji-ii-by-leetcode-s/)

- 考虑一共有三种情况：
    1. 有涨有跌：只有连续两天交易的收益为正，就应该交易；
    2. 连续上涨：按题意应该在头尾交易一次，但注意到：$p_3-p_1$等价于$(p_3-p_2)+(p_2-p_1)$，换言之，等价于当天买入，次日卖出再买入（实际计算过程不等于交易过程）
    3. 连续下跌：不交易
- 综上：比较连续两天的价格，只要收益为正，就交易；

<details><summary><b>Python</b></summary>

```python
class Solution:
    def maxProfit(self, prices: List[int]) -> int:

        ret = 0
        for i in range(1, len(prices)):
            dif = prices[i] - prices[i - 1]
            if dif > 0:
                ret += dif

        return ret
```

</details>
