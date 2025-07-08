## 连续子数组的最大和
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2025-07-08%2016%3A53%3A13&color=yellowgreen&style=flat-square)
[![](https://img.shields.io/static/v1?label=&message=%E7%AE%80%E5%8D%95&color=yellow&style=flat-square)](../../../README.md#简单)
[![](https://img.shields.io/static/v1?label=&message=%E5%89%91%E6%8C%87Offer&color=green&style=flat-square)](../../../README.md#剑指offer)
[![](https://img.shields.io/static/v1?label=&message=%E5%8A%A8%E6%80%81%E8%A7%84%E5%88%92&color=blue&style=flat-square)](../../../README.md#动态规划)

<!--END_SECTION:badge-->
<!--info
tags: [动态规划]
source: 剑指Offer
level: 简单
number: '4200'
name: 连续子数组的最大和
companies: []
-->

<summary><b>问题简述</b></summary>

```txt
给定一个整型数组，求其连续子数组的最大和。
```

<details><summary><b>详细描述</b></summary>

```txt
输入一个整型数组，数组中的一个或连续多个整数组成一个子数组。求所有子数组的和的最大值。

要求时间复杂度为O(n)。

示例1:
    输入: nums = [-2,1,-3,4,-1,2,1,-5,4]
    输出: 6
    解释: 连续子数组 [4,-1,2,1] 的和最大，为 6。

提示：
    1 <= arr.length <= 10^5
    -100 <= arr[i] <= 100

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/lian-xu-zi-shu-zu-de-zui-da-he-lcof
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```

</details>

<summary><b>思路：动态规划</b></summary>

- **状态定义**：记 `dp[i]` 表示以 `nums[i]` 结尾的连续子数组最大和；
  > “以 `nums[i]` 结尾”表示就是这个数一定会加上去，那么要看的就是这个数前面的部分要不要加上去——大于零就加，小于零就舍弃。
- **转移方程**：
    - 当 $dp[i-1] > 0$ 时：执行 $dp[i] = dp[i-1] + nums[i]$；
    - 当 $dp[i-1] \le 0$ 时：执行 $dp[i] = nums[i]$；


<details><summary><b>Python</b></summary>

```python
class Solution:
    def maxSubArray(self, nums: List[int]) -> int:

        n = len(nums)
        dp = [float('-inf')] * n

        dp[0] = nums[0]
        for i in range(1, n):
            dp[i] = max(nums[i], dp[i-1] + nums[i])
        
        return max(dp)
```

</details>

**优化**：因为每次只与上一个状态有关，所以可以只使用一个变量来存储；

<details><summary><b>Python：空间优化</b></summary>

```python
class Solution:
    def maxSubArray(self, nums: List[int]) -> int:

        ret = dp = nums[0]
        for x in nums[1:]:
            dp = max(dp + x, x)
            ret = max(dp, ret)
        
        return ret
```

</details>
