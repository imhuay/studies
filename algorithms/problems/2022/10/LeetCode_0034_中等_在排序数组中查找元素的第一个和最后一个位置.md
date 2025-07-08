## 在排序数组中查找元素的第一个和最后一个位置
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2025-07-08%2016%3A53%3A13&color=yellowgreen&style=flat-square)
[![](https://img.shields.io/static/v1?label=&message=%E4%B8%AD%E7%AD%89&color=yellow&style=flat-square)](../../../README.md#中等)
[![](https://img.shields.io/static/v1?label=&message=LeetCode&color=green&style=flat-square)](../../../README.md#leetcode)
[![](https://img.shields.io/static/v1?label=&message=%E4%BA%8C%E5%88%86%E6%9F%A5%E6%89%BE&color=blue&style=flat-square)](../../../README.md#二分查找)
[![](https://img.shields.io/static/v1?label=&message=LeetCode%20Hot%20100&color=blue&style=flat-square)](../../../README.md#leetcode-hot-100)

<!--END_SECTION:badge-->
<!--info
tags: [二分, lc100]
source: LeetCode
level: 中等
number: '0034'
name: 在排序数组中查找元素的第一个和最后一个位置
companies: []
-->

> [34. 在排序数组中查找元素的第一个和最后一个位置 - 力扣（LeetCode）](https://leetcode.cn/problems/find-first-and-last-position-of-element-in-sorted-array/)

<summary><b>问题简述</b></summary>

```txt
给你一个按照非递减顺序排列的整数数组 nums，和一个目标值 target。请你找出给定目标值在数组中的开始位置和结束位置。
如果数组中不存在目标值 target，返回 [-1, -1]。
要求：时间复杂度 O(logN)
```

<!-- 
<details><summary><b>详细描述</b></summary>

```txt
```

</details>
-->

<!-- <div align="center"><img src="../../../_assets/xxx.png" height="300" /></div> -->

<summary><b>思路：二分查找</b></summary>

- 参考 `from bisect import bisect_left, bisect_right`
- 代码细节见注释；

<details><summary><b>Python 写法 1：左闭右开区间</b></summary>

```python
class Solution:
    def searchRange(self, nums: List[int], target: int) -> List[int]:
        if not nums: return [-1, -1]

        # 找最左侧的 target
        l, r = 0, len(nums)
        while l < r:  # 退出循环时 l == r
            m = l + (r - l) // 2
            if nums[m] < target:
                l = m + 1
            else:
                r = m

        # 不存在 target
        if l == len(nums) or nums[l] != target:
            return [-1, -1]
        
        L = l
        # 找最右侧的 target
        l, r = 0, len(nums)
        while l < r:
            m = l + (r - l) // 2
            if nums[m] <= target:  # 与找最左侧只有 <= 这一处区别
                l = m + 1
            else:
                r = m
        
        R = r - 1  # 注意 r 是开区间
        return [L, R]
```

</details>


<details><summary><b>Python 写法 2：利用 Python 特性减少代码量</b></summary>

```python
class Solution:
    def searchRange(self, nums: List[int], target: int) -> List[int]:
        if not nums: return [-1, -1]

        def bisect(l, r, com):
            while l < r:
                m = l + (r - l) // 2
                if eval(f'{nums[m]} {com} {target}'):
                    l = m + 1
                else:
                    r = m
            return l  # 退出循环时 l == r

        # 找最左侧的 target
        L = bisect(0, len(nums), '<')
        # 不存在 target
        if L == len(nums) or nums[L] != target:
            return [-1, -1]
        
        R = bisect(0, len(nums), '<=') - 1
        return [L, R]
```

</details>
