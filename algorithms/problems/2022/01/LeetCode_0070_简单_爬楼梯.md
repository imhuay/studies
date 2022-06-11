## LeetCode_0070_爬楼梯（简单, 2022-01）
<!--{
    "tags": ["动态规划"],
    "来源": "LeetCode",
    "难度": "简单",
    "编号": "0070",
    "标题": "爬楼梯"
}-->

<summary><b>问题简述</b></summary>

```txt
规定每次可以爬1级或2级台阶。求爬一个 n 级台阶总共有多少种方法。
```

<details><summary><b>详细描述</b></summary>

```txt
假设你正在爬楼梯。需要 n 阶你才能到达楼顶。

每次你可以爬 1 或 2 个台阶。你有多少种不同的方法可以爬到楼顶呢？

注意：给定 n 是一个正整数。

示例 1：
    输入： 2
    输出： 2
    解释： 有两种方法可以爬到楼顶。
    1.  1 阶 + 1 阶
    2.  2 阶
示例 2：
    输入： 3
    输出： 3
    解释： 有三种方法可以爬到楼顶。
    1.  1 阶 + 1 阶 + 1 阶
    2.  1 阶 + 2 阶
    3.  2 阶 + 1 阶

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/climbing-stairs
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```

</details>

<!-- <div align="center"><img src="../../../_assets/xxx.png" height="300" /></div> -->

<summary><b>思路：动态规划</b></summary>

<details><summary><b>Python</b></summary>

```python
class Solution:
    def climbStairs(self, n: int) -> int:
        if n == 1:
            return 1
        if n == 2:
            return 2

        dp1, dp2 = 1, 2
        for _  in range(3, n + 1):
            dp1, dp2 = dp2, dp1 + dp2
        
        return dp2
```

</details>

