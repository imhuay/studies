## 扑克牌中的顺子
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2025-07-08%2016%3A53%3A13&color=yellowgreen&style=flat-square)
[![](https://img.shields.io/static/v1?label=&message=%E7%AE%80%E5%8D%95&color=yellow&style=flat-square)](../../../README.md#简单)
[![](https://img.shields.io/static/v1?label=&message=%E5%89%91%E6%8C%87Offer&color=green&style=flat-square)](../../../README.md#剑指offer)
[![](https://img.shields.io/static/v1?label=&message=%E6%8E%92%E5%BA%8F&color=blue&style=flat-square)](../../../README.md#排序)
[![](https://img.shields.io/static/v1?label=&message=%E6%A8%A1%E6%8B%9F&color=blue&style=flat-square)](../../../README.md#模拟)

<!--END_SECTION:badge-->
<!--info
tags: [排序, 模拟]
source: 剑指Offer
level: 简单
number: '6100'
name: 扑克牌中的顺子
companies: []
-->

<summary><b>问题简述</b></summary>

```txt
从若干副扑克牌中随机抽 5 张牌，判断是不是一个顺子；
```

<details><summary><b>详细描述</b></summary>

```txt
从若干副扑克牌中随机抽 5 张牌，判断是不是一个顺子，即这5张牌是不是连续的。2～10为数字本身，A为1，J为11，Q为12，K为13，而大、小王为 0 ，可以看成任意数字。A 不能视为 14。

示例 1:
    输入: [1,2,3,4,5]
    输出: True
示例 2:
    输入: [0,0,1,2,5]
    输出: True

限制：
    数组长度为 5 
    数组的数取值为 [0, 13] .

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/bu-ke-pai-zhong-de-shun-zi-lcof
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```

</details>

<!-- <div align="center"><img src="../../../_assets/xxx.png" height="300" /></div> -->

<summary><b>思路</b></summary>

- 排序后，统计 0 出现的次数，以及数组中的 `max_x` 和 `min_x`；
- 当`最大值 - 最小值 < 5` 时即可组成顺子；
- 若出现相同牌则提前返回 False；

<details><summary><b>Python</b></summary>

```python
class Solution:
    def isStraight(self, nums: List[int]) -> bool:

        nums.sort()  # 排序
        # 如果不想排序需的话，就需要另外使用一些变量来记录最大、最小和已经出现过的牌

        cnt_0 = 0
        for i, x in enumerate(nums[:-1]):
            if x == 0:  # 记录 0 的个数
                cnt_0 += 1
            elif x == nums[i + 1]:
                return False
        
        # return nums[-1] - nums[cnt_0] == 4  # Error，因为 0 也可以用来作为最大或最小的牌
        return nums[-1] - nums[cnt_0] < 5

```

</details>

