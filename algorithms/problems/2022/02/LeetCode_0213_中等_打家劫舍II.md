## LeetCode_0213_打家劫舍II（中等, 2022-02）
<!--{
    "tags": ["动态规划"],
    "来源": "LeetCode",
    "难度": "中等",
    "编号": "0213",
    "标题": "打家劫舍II",
    "公司": []
}-->

<summary><b>问题简述</b></summary>

```txt
你是一个专业的小偷，计划偷窃沿街的房屋，每间房内都藏有一定的现金。这个地方所有的房屋都 围成一圈 ，这意味着第一个房屋和最后一个房屋是紧挨着的。同时，相邻的房屋装有相互连通的防盗系统，如果两间相邻的房屋在同一晚上被小偷闯入，系统会自动报警 。

给定一个代表每个房屋存放金额的非负整数数组，计算你 在不触动警报装置的情况下 ，今晚能够偷窃到的最高金额。
```
> [213. 打家劫舍 II - 力扣（LeetCode）](https://leetcode-cn.com/problems/house-robber-ii/)

<!-- 
<details><summary><b>详细描述</b></summary>

```txt
```

</details>
-->


<!-- <div align="center"><img src="../../../_assets/xxx.png" height="300" /></div> -->

<summary><b>思路</b></summary>

- 与[打家劫舍](https://leetcode-cn.com/problems/house-robber/)的唯一区别就是不能同时偷首尾两家；
- 因此可以考虑分别计算 `nums[1:]` 和 `nums[:-1]`，求较大值；
    > [打家劫舍 II（动态规划，结构化思路，清晰题解） - Krahets](https://leetcode-cn.com/problems/house-robber-ii/solution/213-da-jia-jie-she-iidong-tai-gui-hua-jie-gou-hua-/)

<details><summary><b>Python</b></summary>

```python
class Solution:
    def rob(self, nums: List[int]) -> int:
        if len(nums) == 1: return nums[0]

        def f(nums):
            N = len(nums)
            dp = [0] * (N + 1)
            dp[1] = nums[0]

            for i in range(2, N + 1):
                dp[i] = max(dp[i-1], dp[i-2] + nums[i - 1])
            
            return dp[-1]
        
        return max(f(nums[1:]), f(nums[:-1]))
```

</details>

