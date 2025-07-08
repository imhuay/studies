## 最长递增子序列
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2022-10-16%2016%3A55%3A02&color=yellowgreen&style=flat-square)
[![](https://img.shields.io/static/v1?label=&message=%E4%B8%AD%E7%AD%89&color=yellow&style=flat-square)](../../../README.md#中等)
[![](https://img.shields.io/static/v1?label=&message=LeetCode&color=green&style=flat-square)](../../../README.md#leetcode)
[![](https://img.shields.io/static/v1?label=&message=%E5%8A%A8%E6%80%81%E8%A7%84%E5%88%92&color=blue&style=flat-square)](../../../README.md#动态规划)
[![](https://img.shields.io/static/v1?label=&message=%E8%B4%AA%E5%BF%83&color=blue&style=flat-square)](../../../README.md#贪心)
[![](https://img.shields.io/static/v1?label=&message=%E7%BB%8F%E5%85%B8&color=blue&style=flat-square)](../../../README.md#经典)

<!--END_SECTION:badge-->
<!--info
tags: [动态规划, 贪心, 经典]
source: LeetCode
level: 中等
number: '0300'
name: 最长递增子序列
companies: []
-->

<summary><b>问题简述</b></summary>

```txt
给定整数数组 nums，返回最长严格递增子序列的长度；
进阶：
    你可以设计时间复杂度为 O(N^2) 的解决方案吗？
    你能把时间复杂度降到 O(NlogN) 吗?
```

<details><summary><b>详细描述</b></summary>

```txt
给你一个整数数组 nums ，找到其中最长严格递增子序列的长度。

子序列是由数组派生而来的序列，删除（或不删除）数组中的元素而不改变其余元素的顺序。例如，[3,6,2,7] 是数组 [0,3,1,6,2,2,7] 的子序列。

示例 1：
    输入：nums = [10,9,2,5,3,7,101,18]
    输出：4
    解释：最长递增子序列是 [2,3,7,101]，因此长度为 4 。
示例 2：
    输入：nums = [0,1,0,3,2,3]
    输出：4
示例 3：
    输入：nums = [7,7,7,7,7,7,7]
    输出：1

提示：
    1 <= nums.length <= 2500
    -104 <= nums[i] <= 104

进阶：
    你可以设计时间复杂度为 O(n2) 的解决方案吗？
    你能将算法的时间复杂度降低到 O(n log(n)) 吗?

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/longest-increasing-subsequence
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```

</details>

<!-- <div align="center"><img src="../../../_assets/xxx.png" height="300" /></div> -->

<summary><b>思路1：动态规划</b></summary>

**状态定义**：`dp[i]` 表示以 `nums[i]` 结尾的最长递增子序列长度；
> 不能将 `dp[i]` 定义 `nums[:i]` 子数组中的最长递增子序列长度，虽然这样定义很直观，但它不满足**最优子结构**的条件，简单来说，就是你无法通过 `dp[i-1]` 得到 `dp[i]`。

<details><summary><b>Python</b></summary>

```python
class Solution:
    def lengthOfLIS(self, nums: List[int]) -> int:
        
        ret = 1
        dp = [1] * len(nums)
        for i in range(1, len(nums)):
            for j in range(i):
                if nums[i] > nums[j]:  # 如果要求非严格递增，将 '>' 改为 '>=' 即可
                    dp[i] = max(dp[i], dp[j] + 1)
            
            ret = max(ret, dp[i])
        
        return ret
```

</details>

<summary><b>思路2：优化 dp 的状态定义</b></summary>

- 考虑新的**状态定义**：`dp[i]` 表示长度为 `i + 1` 的最长递增子序列末尾的最小值；
    > `dp` 序列一定时单调递增的，可用反证法证明，详见：[最长递增子序列（动态规划 + 二分查找，清晰图解） - Krahets](https://leetcode-cn.com/problems/longest-increasing-subsequence/solution/zui-chang-shang-sheng-zi-xu-lie-dong-tai-gui-hua-2/)
    >> 该怎么想出这个定义？——多看多做
- 是否满足**最优子结构**？
    - 即已知 `dp[i - 1]` 能否递推得到 `dp[i]` ；显然是可以的，当`nums[i] > dp[i - 1]`时，长度 `+1`，否则，长度不变；
- 如何更新`dp`？
    - 当 `nums[i] > dp[i - 1]` 时，直接添加到末尾；
    - 否则，要看是否需要更新 `dp`。根据 `dp` 递增的性质，找到 `nums[i]` 在 `dp` 中应该插入的位置，记 `idx`；比较 `dp[idx]` 与 `nums[i]` 的大小，如果 `dp[idx] > nums[i]` 根据定义，更新 `dp[idx] = nums[i]`；

**从“贪心”角度来解释以上过程**：如果我们要使上升子序列尽可能的长，则应该让序列上升得尽可能慢，即每次在上升子序列最后加上的那个数尽可能的小。
> [最长上升子序列 - 力扣官方题解](https://leetcode-cn.com/problems/longest-increasing-subsequence/solution/zui-chang-shang-sheng-zi-xu-lie-by-leetcode-soluti/)


<details><summary><b>Python</b></summary>

```python
class Solution:
    def lengthOfLIS(self, nums: List[int]) -> int:
        if not nums: return 0

        # from bisect import bisect_left

        # 手写二分查找
        def bisect_left(ls, x):
            l, r = 0, len(ls)
            while l < r:
                m = (l + r) // 2
                if ls[m] < x:  # 注意这里要 <，如果是 <= 就是 bisect_right 了，不满足题意
                    l = m + 1
                else:
                    r = m
            return l

        dp = [nums[0]]  # dp[i] 表示长度为 (i+1) 的 LIS 的最后一个元素的最小值
        for x in nums[1:]:
            if x > dp[-1]:
                dp.append(x)
            else:
                idx = bisect_left(dp, x)  # 不能使用 bisect/bisect_right
                # if dp[idx] > x:
                #     dp[idx] = x
                dp[idx] = x  # 因为 bisect_left 返回的定义就是 dp[idx] <= x，所以可以直接赋值

        return len(dp)
```

</details>
