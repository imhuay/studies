## 数组中的第K个最大元素
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2023-07-17%2004%3A19%3A17&color=yellowgreen&style=flat-square)
[![](https://img.shields.io/static/v1?label=&message=%E4%B8%AD%E7%AD%89&color=yellow&style=flat-square)](../../../README.md#中等)
[![](https://img.shields.io/static/v1?label=&message=LeetCode&color=green&style=flat-square)](../../../README.md#leetcode)
[![](https://img.shields.io/static/v1?label=&message=%E6%8E%92%E5%BA%8F&color=blue&style=flat-square)](../../../README.md#排序)
[![](https://img.shields.io/static/v1?label=&message=LeetCode%20Hot%20100&color=blue&style=flat-square)](../../../README.md#leetcode-hot-100)

<!--END_SECTION:badge-->
<!--START_SECTION:badge-->
<!--END_SECTION:badge-->
<!--info
tags: [排序, lc100]
source: LeetCode
level: 中等
number: '0215'
name: 数组中的第K个最大元素
companies: []
-->

> [215. 数组中的第K个最大元素 - 力扣（LeetCode）](https://leetcode.cn/problems/kth-largest-element-in-an-array/?favorite=2cktkvj)

<summary><b>问题简述</b></summary>

```txt
给定整数数组 nums 和整数 k，请返回数组中第 k 个最大的元素。
请注意，你需要找的是数组排序后的第 k 个最大的元素，而不是第 k 个不同的元素。
你必须设计并实现时间复杂度为 O(n) 的算法解决此问题。
```

<!-- 
<details><summary><b>详细描述</b></summary>

```txt
```

</details>
-->

<!-- <div align="center"><img src="../../../_assets/xxx.png" height="300" /></div> -->

<summary><b>思路</b></summary>

- 利用快排的 partition 操作;
- 技巧: 利用 "三数取中" 或者随机选择 pivot 避免最坏情况;

<details><summary><b>Python</b></summary>

```python
class Solution:
    def findKthLargest(self, nums: List[int], k: int) -> int:
        
        def reset(l, r):

            # 三数取中
            # m = (l + r) // 2
            # if nums[l] < nums[m] < nums[r] or nums[r] < nums[m] < nums[l]:
            #     nums[m], nums[l] = nums[l], nums[m]
            # elif nums[l] < nums[r] < nums[m] or nums[m] < nums[r] < nums[l]:
            #     nums[r], nums[l] = nums[l], nums[r]
            
            # 随机
            i = random.randint(l, r)
            nums[l], nums[i] = nums[i], nums[l]

        def dfs(lo, hi):
            if lo >= hi: return

            reset(lo, hi - 1)  # 加速, 避免最坏情况
            p = nums[lo]
            l, r = lo, hi - 1
            while l < r:
                while l < r and nums[r] <= p: r -= 1
                while l < r and nums[l] >= p: l += 1
                nums[l], nums[r] = nums[r], nums[l]
            nums[l], nums[lo] = nums[lo], nums[l]

            if l > k - 1: dfs(lo, l)
            if l < k - 1: dfs(l + 1, hi)
        
        dfs(0, len(nums))
        return nums[k - 1]
```

</details>

<!-- 
<summary><b>相关问题</b></summary>

-->
