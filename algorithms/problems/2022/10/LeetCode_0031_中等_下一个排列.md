## 下一个排列
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2022-10-14%2014%3A59%3A33&color=yellowgreen&style=flat-square)
[![](https://img.shields.io/static/v1?label=&message=%E4%B8%AD%E7%AD%89&color=yellow&style=flat-square)](../../../README.md#中等)
[![](https://img.shields.io/static/v1?label=&message=LeetCode&color=green&style=flat-square)](../../../README.md#leetcode)
[![](https://img.shields.io/static/v1?label=&message=%E5%8F%8C%E6%8C%87%E9%92%88&color=blue&style=flat-square)](../../../README.md#双指针)
[![](https://img.shields.io/static/v1?label=&message=%E7%BB%8F%E5%85%B8&color=blue&style=flat-square)](../../../README.md#经典)
[![](https://img.shields.io/static/v1?label=&message=LeetCode%20Hot%20100&color=blue&style=flat-square)](../../../README.md#leetcode-hot-100)

<!--END_SECTION:badge-->
<!--info
tags: [双指针, 经典, lc100]
source: LeetCode
level: 中等
number: '0031'
name: 下一个排列
companies: []
-->

> [31. 下一个排列 - 力扣（LeetCode）](https://leetcode.cn/problems/next-permutation)

<summary><b>问题简述</b></summary>

```txt
给定一个整数数组，求该数组的下一个排列。
注意：完全逆序的下一个排列是正序。
要求：原地修改数组。
```

<!-- 
<details><summary><b>详细描述</b></summary>

```txt
```

</details>
-->

<!-- <div align="center"><img src="../../../_assets/xxx.png" height="300" /></div> -->

<summary><b>思路</b></summary>

- 为了**使下一个排列更大**，一个方法是将一个左边的「较小数」与一个右边的「较大数」交换；而为了**使变大的幅度最小**，需要让这个「较小数」尽量靠右，而「较大数」尽可能小。
- 具体实现：
    1. **找左边界**：从后往前遍历，找到第一个 `l` 使 `a[l]` **小于** `a[l + 1]`，此时必有 `a[l+1:]` 为逆序；
    2. **找右边界**：再次从后往前遍历，找到第一个**大于** `a[l]` 的位置 `r`；因为 `a[l+1:]`，所以 `j` 依次遍历即可，此时 `a[l+1:]` 依然为逆序；
    3. 交换 `a[l]` 和 `a[r]`；
    4. 将 `a[l+1:]` 倒序；
- 第 4 步说明：
    - 在第 3 步交换 `a[l]` 和 `a[r]` 后，无论 `a[l+1:]` 无论怎么调整，都是比原来更大的排列，而其中最小的排列就是 `a[l+1:]` 为顺序的情况，又因为此时 `a[l+1:]` 正好为逆序，所以将其做倒置即可；

<details><summary><b>Python</b></summary>

```python
class Solution:
    def nextPermutation(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        if (L := len(nums)) < 2:
            return 
        # 1.
        l = len(nums) - 2
        while l >= 0 and nums[l] >= nums[l + 1]:  # 因为要找 nums[l] < nums[l + 1]，所以这里是 >=
            l -= 1
        # 2.
        if l >= 0:
            r = L - 1
            while r > 0 and nums[r] <= nums[l]:  # 同理要找 nums[r] > nums[l]，所以这里是 <=
                r -= 1
            # 3.
            nums[l], nums[r] = nums[r], nums[l]
        # 4.
        nums[l+1:] = nums[l+1:][::-1]
```

提示：
- 这里要求完全逆序的下一个排序是正序；
- 如果取消这个要求，那么当找到 `l < -1` 时，退出即可，此时说明整个数组时逆序的；

</details>
