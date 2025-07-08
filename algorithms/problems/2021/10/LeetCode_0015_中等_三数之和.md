## 三数之和
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2022-10-14%2014%3A59%3A33&color=yellowgreen&style=flat-square)
[![](https://img.shields.io/static/v1?label=&message=%E4%B8%AD%E7%AD%89&color=yellow&style=flat-square)](../../../README.md#中等)
[![](https://img.shields.io/static/v1?label=&message=LeetCode&color=green&style=flat-square)](../../../README.md#leetcode)
[![](https://img.shields.io/static/v1?label=&message=%E5%8F%8C%E6%8C%87%E9%92%88&color=blue&style=flat-square)](../../../README.md#双指针)
[![](https://img.shields.io/static/v1?label=&message=%E6%8E%92%E5%BA%8F&color=blue&style=flat-square)](../../../README.md#排序)
[![](https://img.shields.io/static/v1?label=&message=LeetCode%20Hot%20100&color=blue&style=flat-square)](../../../README.md#leetcode-hot-100)

<!--END_SECTION:badge-->
<!--info
tags: [首尾双指针, 排序, lc100]
source: LeetCode
level: 中等
number: '0015'
name: 三数之和
companies: []
-->

<summary><b>问题简述</b></summary> 

```text
给定一个数组，找出该数组中所有和为 0 的不重复的三元组。

进阶：不使用 set 去重。
```


<details><summary><b>详细描述</b></summary> 

```text
给你一个包含 n 个整数的数组 nums，判断 nums 中是否存在三个元素 a，b，c ，使得 a + b + c = 0 ？请你找出所有和为 0 且不重复的三元组。

注意：答案中不可以包含重复的三元组。

示例 1：
    输入：nums = [-1,0,1,2,-1,-4]
    输出：[[-1,-1,2],[-1,0,1]]

示例 2：
    输入：nums = []
    输出：[]

示例 3：
    输入：nums = [0]
    输出：[]

提示：
    0 <= nums.length <= 3000
    -10^5 <= nums[i] <= 10^5

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/3sum
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```

</details>


<summary><b>思路</b></summary>

- 排序后，问题可以简化成两数之和（LeetCode-167）；
- 先固定一个数，然后利用首尾双指针进行对向遍历；
- 注意跳过相同结果；

<details><summary><b>Python</b></summary> 

```python
from typing import List

class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:

        ret = []
        target = 0
        nums.sort()

        L = len(nums)
        for i in range(L - 2):  # 固定第一个数

            # 剪枝
            if i > 0 and nums[i] == nums[i - 1]: continue
            if nums[i] + nums[i + 1] + nums[i + 2] > target: break
            if nums[i] + nums[L - 1] + nums[L - 2] < target: continue

            # 首尾指针
            l, r = i + 1, len(nums) - 1
            while l < r:

                if (s := nums[i] + nums[l] + nums[r]) < target:
                    l += 1
                elif s > target:
                    r -= 1
                else:
                    ret.append([nums[i], nums[l], nums[r]])

                    l += 1
                    r -= 1
                    # 剪枝，注意边界条件
                    while l < r and nums[l] == nums[l - 1]: l += 1
                    while l < r and nums[r] == nums[r + 1]: r -= 1

        return ret

```

</details>
