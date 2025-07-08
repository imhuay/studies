## 最小路径和
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2022-10-14%2014%3A59%3A33&color=yellowgreen&style=flat-square)
[![](https://img.shields.io/static/v1?label=&message=%E4%B8%AD%E7%AD%89&color=yellow&style=flat-square)](../../../README.md#中等)
[![](https://img.shields.io/static/v1?label=&message=LeetCode&color=green&style=flat-square)](../../../README.md#leetcode)
[![](https://img.shields.io/static/v1?label=&message=%E5%8A%A8%E6%80%81%E8%A7%84%E5%88%92&color=blue&style=flat-square)](../../../README.md#动态规划)

<!--END_SECTION:badge-->
<!--info
tags: [动态规划]
source: LeetCode
level: 中等
number: '0064'
name: 最小路径和
companies: []
-->

<summary><b>问题简述</b></summary>

```txt
给定一个非负整数的 m x n 网格 grid，请找出一条从左上角到右下角的路径，使得路径上的数字总和为最小。

说明：每次只能向下或者向右移动一步。
```
> [64. 最小路径和 - 力扣（LeetCode）](https://leetcode-cn.com/problems/minimum-path-sum/)

<details><summary><b>详细描述</b></summary>

```txt
给定一个包含非负整数的 m x n 网格 grid ，请找出一条从左上角到右下角的路径，使得路径上的数字总和为最小。

说明：每次只能向下或者向右移动一步。

示例 1：
    输入：grid = [[1,3,1],[1,5,1],[4,2,1]]
    输出：7
    解释：因为路径 1→3→1→1→1 的总和最小。
示例 2：
    输入：grid = [[1,2,3],[4,5,6]]
    输出：12

提示：
    m == grid.length
    n == grid[i].length
    1 <= m, n <= 200
    0 <= grid[i][j] <= 100

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/minimum-path-sum
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```

</details>

<!-- <div align="center"><img src="../../../_assets/xxx.png" height="300" /></div> -->

<summary><b>思路：动态规划</b></summary>

<details><summary><b>Python</b></summary>

```python
class Solution:
    def minPathSum(self, grid: List[List[int]]) -> int:
        if not grid: return 0

        m, n = len(grid), len(grid[0])
        dp = [[0] * n for _ in range(m)]

        # 初始化
        dp[0][0] = grid[0][0]
        for i in range(1, m):
            dp[i][0] = dp[i - 1][0] + grid[i][0]
        for j in range(1, n):
            dp[0][j] = dp[0][j - 1] + grid[0][j]

        # print(dp)
        for i in range(1, m):
            for j in range(1, n):
                dp[i][j] = min(dp[i - 1][j], dp[i][j - 1]) + grid[i][j]
        
        return dp[-1][-1]
```

</details>

**空间优化**：展开循环可以发现，内循环每次遍历实际只会用到上一层的和当前层左边的结果（详见代码）；

<details><summary><b>Python</b></summary>

```python
class Solution:
    def minPathSum(self, grid: List[List[int]]) -> int:
        if not grid: return 0

        m, n = len(grid), len(grid[0])
        dp = [0] * n

        # 初始化
        dp[0] = grid[0][0]
        for j in range(1, n):
            dp[j] = dp[j - 1] + grid[0][j]

        # print(dp)
        for i in range(1, m):
            dp[0] = dp[0] + grid[i][0]  # 初始化每一层最左边的结果
            for j in range(1, n):
                # dp[j - 1] + grid[i][j] 表示从左边移动
                # dp[j] + grid[i][j] 表示从上方移动
                dp[j] = min(dp[j - 1], dp[j]) + grid[i][j]
        
        return dp[-1]

```

</details>