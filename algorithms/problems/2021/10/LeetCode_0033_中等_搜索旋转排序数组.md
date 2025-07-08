## 搜索旋转排序数组
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2022-10-29%2023%3A59%3A13&color=yellowgreen&style=flat-square)
[![](https://img.shields.io/static/v1?label=&message=%E4%B8%AD%E7%AD%89&color=yellow&style=flat-square)](../../../README.md#中等)
[![](https://img.shields.io/static/v1?label=&message=LeetCode&color=green&style=flat-square)](../../../README.md#leetcode)
[![](https://img.shields.io/static/v1?label=&message=%E4%BA%8C%E5%88%86%E6%9F%A5%E6%89%BE&color=blue&style=flat-square)](../../../README.md#二分查找)
[![](https://img.shields.io/static/v1?label=&message=LeetCode%20Hot%20100&color=blue&style=flat-square)](../../../README.md#leetcode-hot-100)
[![](https://img.shields.io/static/v1?label=&message=%E7%83%AD%E9%97%A8&color=blue&style=flat-square)](../../../README.md#热门)

<!--END_SECTION:badge-->
<!--info
tags: [二分查找, lc100, 热门]
source: LeetCode
level: 中等
number: '0033'
name: 搜索旋转排序数组
companies: [Soul]
-->

> [33. 搜索旋转排序数组 - 力扣（LeetCode）](https://leetcode.cn/problems/search-in-rotated-sorted-array)

<summary><b>问题简述</b></summary>

```txt
在一个旋转过的有序数组中搜索某值，若存在返回下标，否则返回 -1。
进阶：时间复杂度要求 O(log n)
```


<!-- 
<details><summary><b>详细描述</b></summary>

```txt
```

</details>
-->


<summary><b>思路</b></summary>

- “二分”的本质是两段性，而不是单调性；即只要二分后，左边满足某个性质，右边不满足某个性质，即可使用二分；
    > [LogicStack-LeetCode/33.搜索旋转排序数组（中等）](https://github.com/SharingSource/LogicStack-LeetCode/blob/main/LeetCode/31-40/33.%20搜索旋转排序数组（中等）.md#二分解法)
- 本题中，将数组从中间分开后，其中一个部分一定是有序的: 
    - 有序部分可以通过比较 `a[m]` 和 `a[0]` 得到；
    - 此时**如果 target 在有序部分**，那么可以排除无序的一半，否则可以排除有序的一半；
- 细节详见代码；

<details><summary><b>Python</b></summary>

```python
class Solution:
    def search(self, nums: List[int], target: int) -> int:

        l, r = 0, len(nums)  # [l, r) 左闭右开区间
        while l < r:
            m = l + (r - l) // 2

            if nums[m] == target: 
                return m
            
            if nums[0] < nums[m]:
                # 此时 m 左边是有序的
                if nums[l] <= target < nums[m]:
                    # 如果 target 在有序部分, 即在左侧
                    r = m
                else:
                    l = m + 1
            else:
                # 此时 m 右边是有序的
                if nums[m] < target <= nums[r - 1]:  # r 是开区间, 所以 - 1
                    # 如果 target 在有序部分, 此时在右侧
                    l = m + 1
                else:
                    r = m  # 右边界

        return -1
```

</details>
