## 最大子数组和
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2025-07-08%2016%3A53%3A13&color=yellowgreen&style=flat-square)
[![](https://img.shields.io/static/v1?label=&message=%E7%AE%80%E5%8D%95&color=yellow&style=flat-square)](../../../README.md#简单)
[![](https://img.shields.io/static/v1?label=&message=LeetCode&color=green&style=flat-square)](../../../README.md#leetcode)
[![](https://img.shields.io/static/v1?label=&message=%E5%8A%A8%E6%80%81%E8%A7%84%E5%88%92&color=blue&style=flat-square)](../../../README.md#动态规划)

<!--END_SECTION:badge-->
<!--info
tags: [动态规划]
source: LeetCode
level: 简单
number: '0053'
name: 最大子数组和
companies: []
-->

<summary><b>问题简述</b></summary>

```txt
给定整数数组 nums ，返回连续子数组的最大和（子数组最少包含一个元素）。
```

<details><summary><b>详细描述</b></summary>

```txt
给你一个整数数组 nums ，请你找出一个具有最大和的连续子数组（子数组最少包含一个元素），返回其最大和。

子数组 是数组中的一个连续部分。

示例 1：
    输入：nums = [-2,1,-3,4,-1,2,1,-5,4]
    输出：6
    解释：连续子数组 [4,-1,2,1] 的和最大，为 6 。
示例 2：
输入：nums = [1]
输出：1
示例 3：
    输入：nums = [5,4,-1,7,8]
    输出：23

提示：
    1 <= nums.length <= 10^5
    -10^4 <= nums[i] <= 10^4

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/maximum-subarray
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```

</details>

<!-- <div align="center"><img src="../../../_assets/xxx.png" height="300" /></div> -->

<summary><b>思路</b></summary>

<details><summary><b>Python</b></summary>

```python
class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        
        # 因为始终只与上一个状态有关，因此可以通过“滚动变量”的方式优化空间
        dp = nums[0]
        ret = nums[0]
        for i in range(1, len(nums)):
            dp = max(nums[i], dp + nums[i])
            ret = max(ret, dp)
        
        return ret
```

</details>

