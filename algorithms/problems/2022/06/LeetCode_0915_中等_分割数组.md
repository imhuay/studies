## 分割数组
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2022-10-14%2014%3A59%3A33&color=yellowgreen&style=flat-square)
[![](https://img.shields.io/static/v1?label=&message=%E4%B8%AD%E7%AD%89&color=yellow&style=flat-square)](../../../README.md#中等)
[![](https://img.shields.io/static/v1?label=&message=LeetCode&color=green&style=flat-square)](../../../README.md#leetcode)
[![](https://img.shields.io/static/v1?label=&message=%E6%A8%A1%E6%8B%9F&color=blue&style=flat-square)](../../../README.md#模拟)

<!--END_SECTION:badge-->
<!--info
tags: [模拟]
source: LeetCode
level: 中等
number: '0915'
name: 分割数组
companies: [小红书]
-->

<summary><b>问题简述</b></summary>

```txt
给定整数数组 nums，将其划分为 left 和 right 两部分，要求：
    1. left 中的每个元素都小于或等于 right 中的每个元素；
    2. left 的长度要尽可能小。
返回 left 的长度，题目保证 left 和 right 都非空；

要求：
    时间复杂度 O(n)
    空间复杂度 O(n) 或 O(1)
```
> [915. 分割数组 - 力扣（LeetCode）](https://leetcode-cn.com/problems/partition-array-into-disjoint-intervals/)

<!-- 
<details><summary><b>详细描述</b></summary>

```txt
```

</details>
-->


<!-- <div align="center"><img src="../../../_assets/xxx.png" height="300" /></div> -->

<summary><b>思路1</b></summary>

- 记 `lmax[i]` 表示 `nums[:i]` 中的最大值，`rmin[i]` 表示 `nums[i:]` 中的最小值；
- 返回使 `lmax[i - 1] <= rmin[i]` 的最小 `i`；
    > 这里要 `<=`，否则意味着所有相同的最小值会被分到 left，不符合题意；

<details><summary><b>Python</b></summary>

```python
class Solution:
    def partitionDisjoint(self, nums: List[int]) -> int:
        
        n = len(nums)

        # 计算 lmax
        lmax = [float('-inf')] * n
        lmax[0] = nums[0]
        for i in range(1, n):
            lmax[i] = max(lmax[i - 1], nums[i])
        
        # 计算 rmin
        rmin = [float('inf')] * n
        for i in range(n - 2, -1, -1):
            rmin[i] = min(rmin[i + 1], nums[i])
        
        for i in range(1, n):
            if lmax[i - 1] <= rmin[i]:  # 注意这里要 <=；如果是 <，意味着所有相同的最小值会分到 left，不符合题意
                return i
        
        return -1
```

</details>

**优化**：计算 `lmax` 和比较的过程都是顺序遍历，可以合并到一起，节省部分空间；

<details><summary><b>Python：优化1</b></summary>

```python
class Solution:
    def partitionDisjoint(self, nums: List[int]) -> int:
        
        n = len(nums)
        rmin = [float('inf')] * n
        for i in range(n - 2, -1, -1):
            rmin[i] = min(rmin[i + 1], nums[i])
        
        # 合并计算 lmax 和比较过程
        lmax = nums[0]
        for i in range(1, n):
            if lmax <= rmin[i]:
                return i
            lmax = max(lmax, nums[i])
        
        return -1
```

</details>


<summary><b>思路2</b></summary>

> [【贪心法】 - 分割数组 - qwf](https://leetcode-cn.com/problems/partition-array-into-disjoint-intervals/solution/tan-xin-fa-by-qwf-snem/)
>> 时间复杂度 `O(n)`，空间复杂度 `O(1)`

- 使用 `lmax` 记录已划分 left 中的最大值；
    - 根据题意，left 的中至少会存在一个元素，因此可以初始化 `lmax=nums[0]`；
- 使用 `amax` 记录遍历过程中的最大值；
- 当 `nums[i] < lmax` 时，说明需要扩充 left，即需要把 `i` 之前的所有元素都添加到 left；同时更新 `lmax=amax`；

```
以 nums=[3,4,1,5,6] 为例，下面是：

初始化：
    amax = 3
    lmax = 3
    ret = 1

for i in range(1, len(nums)):

    i  amax  lmax  ret
    1  3     3     1
    2  4     3     1
    3  5     4     3
    4  6     4     3

返回：
    ret = 3
```

<details><summary><b>Python</b></summary>

```python
class Solution:
    def partitionDisjoint(self, nums: List[int]) -> int:

        lmax = amax = nums[0]
        ret = 1
        for i in range(1, len(nums)):
            amax = max(amax, nums[i])
            if nums[i] < lmax:
                ret = i + 1
                lmax = amax
        
        return ret
```

</details>