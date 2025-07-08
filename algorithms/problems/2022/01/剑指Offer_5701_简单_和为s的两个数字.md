## 和为s的两个数字
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2025-07-08%2016%3A53%3A13&color=yellowgreen&style=flat-square)
[![](https://img.shields.io/static/v1?label=&message=%E7%AE%80%E5%8D%95&color=yellow&style=flat-square)](../../../README.md#简单)
[![](https://img.shields.io/static/v1?label=&message=%E5%89%91%E6%8C%87Offer&color=green&style=flat-square)](../../../README.md#剑指offer)
[![](https://img.shields.io/static/v1?label=&message=%E5%8F%8C%E6%8C%87%E9%92%88&color=blue&style=flat-square)](../../../README.md#双指针)

<!--END_SECTION:badge-->
<!--info
tags: [双指针]
source: 剑指Offer
level: 简单
number: '5701'
name: 和为s的两个数字
companies: []
-->

<summary><b>问题简述</b></summary>

```txt
给定一个递增数组和目标值 s，求数组中和为 s 的两个数；
```

<details><summary><b>详细描述</b></summary>

```txt
输入一个递增排序的数组和一个数字s，在数组中查找两个数，使得它们的和正好是s。
如果有多对数字的和等于s，则输出任意一对即可。

示例 1：
    输入：nums = [2,7,11,15], target = 9
    输出：[2,7] 或者 [7,2]
示例 2：
    输入：nums = [10,26,30,31,47,60], target = 40
    输出：[10,30] 或者 [30,10]

限制：
    1 <= nums.length <= 10^5
    1 <= nums[i] <= 10^6

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/he-wei-sde-liang-ge-shu-zi-lcof
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```

</details>

<!-- <div align="center"><img src="../../../_assets/xxx.png" height="300" /></div> -->

<summary><b>思路</b></summary>

- 首尾双指针，相向遍历；

<details><summary><b>Python</b></summary>

```python
class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:

        l, r = 0, len(nums) - 1

        while l <= r:
            s = nums[l] + nums[r]
            if s == target:
                return [nums[l], nums[r]]
            if s < target:
                l += 1
            else:
                r -= 1
        
        return []
```

</details>

