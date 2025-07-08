## 盛最多水的容器
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2022-10-14%2014%3A59%3A33&color=yellowgreen&style=flat-square)
[![](https://img.shields.io/static/v1?label=&message=%E4%B8%AD%E7%AD%89&color=yellow&style=flat-square)](../../../README.md#中等)
[![](https://img.shields.io/static/v1?label=&message=LeetCode&color=green&style=flat-square)](../../../README.md#leetcode)
[![](https://img.shields.io/static/v1?label=&message=%E5%8F%8C%E6%8C%87%E9%92%88&color=blue&style=flat-square)](../../../README.md#双指针)
[![](https://img.shields.io/static/v1?label=&message=%E8%B4%AA%E5%BF%83&color=blue&style=flat-square)](../../../README.md#贪心)
[![](https://img.shields.io/static/v1?label=&message=LeetCode%20Hot%20100&color=blue&style=flat-square)](../../../README.md#leetcode-hot-100)

<!--END_SECTION:badge-->
<!--info
tags: [双指针, 贪心, lc100]
source: LeetCode
level: 中等
number: '0011'
name: 盛最多水的容器
companies: []
-->

<summary><b>问题描述</b></summary>

```txt
给你 n 个非负整数 a1，a2，...，an，每个数代表坐标中的一个点 (i, ai) 。在坐标内画 n 条垂直线，垂直线 i 的两个端点分别为 (i, ai) 和 (i, 0) 。找出其中的两条线，使得它们与 x 轴共同构成的容器可以容纳最多的水。

说明：不能倾斜容器。

示例 1：
    输入：[1,8,6,2,5,4,8,3,7]
    输出：49 
    解释：图中垂直线代表输入数组 [1,8,6,2,5,4,8,3,7]。在此情况下，容器能够容纳水（表示为蓝色部分）的最大值为 49。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/container-with-most-water
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```

<div align="center"><img src="../../../_assets/question_11.jpeg" height="150" /></div>


<summary><b>思路</b></summary>

- 首尾双指针遍历；
- 每次移动左指针还是右指针？——贪心

<details><summary><b>Python</b></summary>

```python
class Solution:
    def maxArea(self, height: List[int]) -> int:

        def cur_amount():
            return (r - l) * min(height[l], height[r])

        l, r = 0, len(height) - 1
        ret = cur_amount()
        while l < r:
            if height[l] < height[r]:
                l += 1
            else:
                r -= 1
            
            ret = max(ret, cur_amount())
        
        return ret
```

</details>

