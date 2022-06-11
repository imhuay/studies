## 剑指Offer_5701_和为s的两个数字（简单, 2022-01）
<!--{
    "tags": ["双指针"],
    "来源": "剑指Offer",
    "编号": "5701",
    "难度": "简单",
    "标题": "和为s的两个数字"
}-->

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

