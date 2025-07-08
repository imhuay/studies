## 买卖股票的最佳时机III
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2022-10-14%2014%3A59%3A33&color=yellowgreen&style=flat-square)
[![](https://img.shields.io/static/v1?label=&message=%E5%9B%B0%E9%9A%BE&color=yellow&style=flat-square)](../../../README.md#困难)
[![](https://img.shields.io/static/v1?label=&message=LeetCode&color=green&style=flat-square)](../../../README.md#leetcode)
[![](https://img.shields.io/static/v1?label=&message=%E5%8A%A8%E6%80%81%E8%A7%84%E5%88%92&color=blue&style=flat-square)](../../../README.md#动态规划)

<!--END_SECTION:badge-->
<!--info
tags: [动态规划]
source: LeetCode
level: 困难
number: '0123'
name: 买卖股票的最佳时机III
companies: []
-->

<summary><b>问题简述</b></summary>

```txt
给定一个数组，它的第 i 个元素是一支给定的股票在第 i 天的价格。
设计一个算法来计算你所能获取的最大利润。你最多可以完成 两笔 交易。
```

<details><summary><b>详细描述</b></summary>

```txt
给定一个数组，它的第 i 个元素是一支给定的股票在第 i 天的价格。
设计一个算法来计算你所能获取的最大利润。你最多可以完成 两笔 交易。

注意：你不能同时参与多笔交易（你必须在再次购买前出售掉之前的股票）。

示例 1:
    输入：prices = [3,3,5,0,0,3,1,4]
    输出：6
    解释：在第 4 天（股票价格 = 0）的时候买入，在第 6 天（股票价格 = 3）的时候卖出，这笔交易所能获得利润 = 3-0 = 3 。
        随后，在第 7 天（股票价格 = 1）的时候买入，在第 8 天 （股票价格 = 4）的时候卖出，这笔交易所能获得利润 = 4-1 = 3 。
示例 2：
    输入：prices = [1,2,3,4,5]
    输出：4
    解释：在第 1 天（股票价格 = 1）的时候买入，在第 5 天 （股票价格 = 5）的时候卖出, 这笔交易所能获得利润 = 5-1 = 4 。   
        注意你不能在第 1 天和第 2 天接连购买股票，之后再将它们卖出。   
        因为这样属于同时参与了多笔交易，你必须在再次购买前出售掉之前的股票。
示例 3：
    输入：prices = [7,6,4,3,1] 
    输出：0 
    解释：在这个情况下, 没有交易完成, 所以最大利润为 0。
示例 4：
    输入：prices = [1]
    输出：0

提示：
    1 <= prices.length <= 10^5
    0 <= prices[i] <= 10^5

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/best-time-to-buy-and-sell-stock-iii
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```

</details>

<!-- <div align="center"><img src="../../../_assets/xxx.png" height="300" /></div> -->

<summary><b>思路：动态规划</b></summary>

- 分别定义前向、后向两个dp，记 `dp_f` 和 `dp_b`，其中：
    - `dp_f[i]` 表示 `prices[:i]` 区间内的买卖一次的最大值；
    - `dp_b[i]` 表示 `prices[i:]` 区间内的买卖一次的最大值；
- 因为可以只交易一次，所以最终结果为 `max(dp_f[-1], max(dp_f[i] + dp_b[i + 1]))`

<details><summary><b>Python</b></summary>

```python
class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        if len(prices) < 2: return 0
        
        n = len(prices)
        dp_f = [0] * n
        dp_b = [0] * n

        min_p = prices[0]
        for i in range(1, n):
            dp_f[i] = max(dp_f[i-1], prices[i] - min_p)
            min_p = min(min_p, prices[i])
        
        max_b = 0
        max_p = prices[-1]
        for i in range(n - 2, -1, -1):
            dp_b[i] = max(dp_b[i+1], max_p - prices[i])
            max_p = max(max_p, prices[i])
        
        # print(dp_f, dp_b)
        return max(dp_f[-1], max(dp_f[i] + dp_b[i + 1] for i in range(0, n - 1)))
```

</details>

**空间优化**：官方提供了一种空间复杂度为 `O(1)` 的解法：
> [买卖股票的最佳时机 III - 力扣官方题解](https://leetcode-cn.com/problems/best-time-to-buy-and-sell-stock-iii/solution/mai-mai-gu-piao-de-zui-jia-shi-ji-iii-by-wrnt/)

<details><summary><b>Python</b></summary>

```python
class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        n = len(prices)
        buy1 = buy2 = prices[0]
        sell1 = sell2 = 0
        for i in range(1, n):
            buy1 = min(buy1, prices[i])
            sell1 = max(sell1, prices[i] - buy1)
            buy2 = min(buy2, prices[i] - sell1)
            sell2 = max(sell2, prices[i] - buy2)
        return sell2
```

</details>

<!-- 
**空间优化**：通过合理的控制下标，可以用一个循环生成 `dp_f` 和 `dp_b`，这样同时也省去了需要保存历史状态的问题，可以将空间复杂度优化到 `O(1)`

<details><summary><b>Python</b></summary>

```python
class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        if len(prices) < 2: return 0
        
        n = len(prices)
        dp_f = [0] * n
        dp_b = [0] * n

        min_p = prices[0]
        for i in range(1, n):
            dp_f[i] = max(dp_f[i-1], prices[i] - min_p)
            min_p = min(min_p, prices[i])
        
        max_b = 0
        max_p = prices[-1]
        for i in range(n - 2, -1, -1):
            dp_b[i] = max(dp_b[i+1], max_p - prices[i])
            max_p = max(max_p, prices[i])
        
        # print(dp_f, dp_b)
        return max(dp_f[-1], max(dp_f[i] + dp_b[i + 1] for i in range(0, n - 1)))
```

</details>

 -->