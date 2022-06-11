## 剑指Offer_6300_买卖股票的最佳时机（中等, 2022-01）
<!--{
    "tags": ["模拟"],
    "来源": "剑指Offer",
    "编号": "6300",
    "难度": "中等",
    "标题": "买卖股票的最佳时机"
}-->

<summary><b>问题简述</b></summary>

```txt
把某股票的价格按照时间顺序存储在数组中，求买卖一次的最大利润。
示例: 输入: [7,1,5,3,6,4]，输出: 5（在价格 1 时买入，价格 6 时卖出）
```

<details><summary><b>详细描述</b></summary>

```txt
假设把某股票的价格按照时间先后顺序存储在数组中，请问买卖该股票一次可能获得的最大利润是多少？

示例 1:
    输入: [7,1,5,3,6,4]
    输出: 5
    解释: 在第 2 天（股票价格 = 1）的时候买入，在第 5 天（股票价格 = 6）的时候卖出，最大利润 = 6-1 = 5 。
        注意利润不能是 7-1 = 6, 因为卖出价格需要大于买入价格。
示例 2:
    输入: [7,6,4,3,1]
    输出: 0
    解释: 在这种情况下, 没有交易完成, 所以最大利润为 0。
 

限制：
    0 <= 数组长度 <= 10^5
    0 <= 股票价格 <= 10^5

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/gu-piao-de-zui-da-li-run-lcof
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

