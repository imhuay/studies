## 礼物的最大价值
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2025-07-08%2016%3A53%3A13&color=yellowgreen&style=flat-square)
[![](https://img.shields.io/static/v1?label=&message=%E4%B8%AD%E7%AD%89&color=yellow&style=flat-square)](../../../README.md#中等)
[![](https://img.shields.io/static/v1?label=&message=%E5%89%91%E6%8C%87Offer&color=green&style=flat-square)](../../../README.md#剑指offer)
[![](https://img.shields.io/static/v1?label=&message=%E5%8A%A8%E6%80%81%E8%A7%84%E5%88%92&color=blue&style=flat-square)](../../../README.md#动态规划)

<!--END_SECTION:badge-->
<!--info
tags: [动态规划]
source: 剑指Offer
level: 中等
number: '4700'
name: 礼物的最大价值
companies: []
-->

<summary><b>问题简述</b></summary>

```txt
给定 m*n 的整型数组 grid，求从左上角到右下角路线中和的最大值（每次向下或向右移动一格）

示例输入: 
    [1,3,1]
    [1,5,1]
    [4,2,1]
输出: 12
解释: 路径 1→3→5→2→1 可以拿到最多价值的礼物
```

<details><summary><b>详细描述</b></summary>

```txt
在一个 m*n 的棋盘的每一格都放有一个礼物，每个礼物都有一定的价值（价值大于 0）。你可以从棋盘的左上角开始拿格子里的礼物，并每次向右或者向下移动一格、直到到达棋盘的右下角。给定一个棋盘及其上面的礼物的价值，请计算你最多能拿到多少价值的礼物？

示例 1:
    输入: 
    [
      [1,3,1],
      [1,5,1],
      [4,2,1]
    ]
    输出: 12
    解释: 路径 1→3→5→2→1 可以拿到最多价值的礼物
 
提示：
    0 < grid.length <= 200
    0 < grid[0].length <= 200

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/li-wu-de-zui-da-jie-zhi-lcof
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```

<!-- <div align="center"><img src="./_assets/xxx.png" height="300" /></div> -->

</details>


<summary><b>思路：动态规划</b></summary>

**状态定义**
- 记 `dp[i][j] := 从左上角走至 (i,j) 位置时的最大值` 

**转移方程**
- `dp[i][j] = max(dp[i-1][j], dp[i][j-1]) + grid[i][j]`

**初始状态**
- `dp[i][0] = sum(grid[:i][0])`
- `dp[0][j] = sum(grid[0][:j])`


<details><summary><b>Python：本地修改</b></summary>

因为 `dp[i][j]` 只与 `dp[i-1][j]` 和 `dp[i][j-1]` 有关，因此可以直接将 grid 作为 dp 矩阵，原地修改；
> [题解：礼物的最大价值（动态规划，清晰图解）](https://leetcode-cn.com/problems/li-wu-de-zui-da-jie-zhi-lcof/solution/mian-shi-ti-47-li-wu-de-zui-da-jie-zhi-dong-tai-gu/)

```python
class Solution:
    def maxValue(self, grid: List[List[int]]) -> int:
        m, n = len(grid), len(grid[0])

        # 初始化
        for j in range(1, n): 
            grid[0][j] += grid[0][j - 1]
        for i in range(1, m):
            grid[i][0] += grid[i - 1][0]
        
        for i in range(1, m):
            for j in range(1, n):
                grid[i][j] += max(grid[i][j - 1], grid[i - 1][j])

        return grid[-1][-1]
```

</details>


<details><summary><b>Python：非本地修改，优化空间复杂度</b></summary>

<br/>因为不存在回溯（每次只能向下或向右），所以只需要保存上一行（或上一列）的结果即可；

**状态定义**
- 记 `dp[j] := 从左上角走至 (i,j) 位置时的最大值` 

**转移方程**
- `dp[j] = max(dp[j-1], dp[j]) + grid[i][j]`

    ```
    dp[j-1] + grid[i][j] 表示路线为 grid[i-1][j-1] → grid[i-1][j] → grid[i][j]，即先往右再向下
    dp[j]   + grid[i][j] 表示路线为 grid[i-1][j-1] → grid[i][j-1] → grid[i][j]，即先向下再往右
    然后选择这两条路线中较大的更新 dp[j]
    ```

**初始状态**
- `dp[j] = sum(grid[0][:j])`

```python
class Solution:
    def maxValue(self, grid: List[List[int]]) -> int:
        if not grid or not grid[0]: return 0

        m, n = len(grid), len(grid[0])

        # 初始化第一行的结果
        dp = [grid[0][0]] + [0] * (n - 1)
        for i in range(1, n):
            dp[i] = dp[i - 1] + grid[0][i]

        for i in range(1, m):
            dp[0] = dp[0] + grid[i][0]
            for j in range(1, n):
                # dp[j-1] + grid[i][j] 表示 grid[i-1][j-1] → grid[i][j-1] → grid[i][j]
                # dp[j]   + grid[i][j] 表示 grid[i-1][j-1] → grid[i-1][j] → grid[i][j]
                # 然后选择这两条路线中较大的更新 dp[j]
                dp[j] = max(dp[j-1], dp[j]) + grid[i][j]
        
        return dp[n-1]
```

</details>