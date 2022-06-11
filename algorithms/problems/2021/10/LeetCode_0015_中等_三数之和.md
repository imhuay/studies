## LeetCode_0015_三数之和（中等, 2021-10）
<!--{
    "tags": ["双指针"],
    "来源": "LeetCode",
    "编号": "0015",
    "难度": "中等",
    "标题": "三数之和"
}-->

<summary><b>问题简述</b></summary> 

```text
给定一个数组，找出该数组中所有和为 0 的三元组。
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
        
        # assert
        ret = []
        L = len(nums)
        if L < 3:
            return ret

        # 设置目标值
        target = 0
        # 排序
        nums = sorted(nums)

        for i in range(L - 2):  # 固定第一个数
            # 剪枝
            if i > 0 and nums[i] == nums[i - 1]: continue
            if nums[i] + nums[i + 1] + nums[i + 2] > target: break
            if nums[i] + nums[L - 2] + nums[L - 1] < target: continue

            # 设置左右指针
            l, r = i + 1, L - 1
            while l < r:

                s = nums[i] + nums[l] + nums[r]
                if s < target:
                    l += 1
                elif s > target:
                    r -= 1
                else:  # s == target
                    ret.append([nums[i], nums[l], nums[r]])

                    # 同时移动双指针
                    l += 1
                    r -= 1

                    # 如果跟上一个值相同，就跳过
                    while l < r and nums[l] == nums[l - 1]: l += 1
                    while l < r and nums[r] == nums[r + 1]: r -= 1

        return ret

```

</details>
