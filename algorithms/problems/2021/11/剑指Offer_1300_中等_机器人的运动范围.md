## 机器人的运动范围
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2022-10-14%2014%3A59%3A33&color=yellowgreen&style=flat-square)
[![](https://img.shields.io/static/v1?label=&message=%E4%B8%AD%E7%AD%89&color=yellow&style=flat-square)](../../../README.md#中等)
[![](https://img.shields.io/static/v1?label=&message=%E5%89%91%E6%8C%87Offer&color=green&style=flat-square)](../../../README.md#剑指offer)
[![](https://img.shields.io/static/v1?label=&message=%E6%B7%B1%E5%BA%A6%E4%BC%98%E5%85%88%E6%90%9C%E7%B4%A2&color=blue&style=flat-square)](../../../README.md#深度优先搜索)

<!--END_SECTION:badge-->
<!--info
tags: [DFS]
source: 剑指Offer
level: 中等
number: '1300'
name: 机器人的运动范围
companies: []
-->

<summary><b>问题描述</b></summary>

```txt
地上有一个m行n列的方格，从坐标 [0,0] 到坐标 [m-1,n-1] 。一个机器人从坐标 [0, 0] 的格子开始移动，它每次可以向左、右、上、下移动一格（不能移动到方格外），也不能进入行坐标和列坐标的数位之和大于k的格子。例如，当k为18时，机器人能够进入方格 [35, 37] ，因为3+5+3+7=18。但它不能进入方格 [35, 38]，因为3+5+3+8=19。请问该机器人能够到达多少个格子？

示例 1：
    输入：m = 2, n = 3, k = 1
    输出：3
示例 2：
    输入：m = 3, n = 1, k = 0
    输出：1

提示：
    1 <= n,m <= 100
    0 <= k <= 20

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/ji-qi-ren-de-yun-dong-fan-wei-lcof
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```

<summary><b>思路</b></summary>

- 本题也可以使用广度优先搜索；
  > [机器人的运动范围（ 回溯算法，DFS / BFS ，清晰图解）](https://leetcode-cn.com/problems/ji-qi-ren-de-yun-dong-fan-wei-lcof/solution/mian-shi-ti-13-ji-qi-ren-de-yun-dong-fan-wei-dfs-b/)

<!-- <div align="center"><img src="../../../_assets/xxx.png" height="300" /></div> -->

<details><summary><b>Python：DFS+回溯</b></summary>

```python
class Solution:
    def movingCount(self, m: int, n: int, k: int) -> int:

        def dig_sum(x):  # 求数位之和
            s = 0
            while x != 0:
                s += x % 10
                x = x // 10
            return s

        def dfs(i, j):
            if not 0 <= i < m or not 0 <= j < n or dig_sum(i) + dig_sum(j) > k:
                return 0

            if (i, j) in visited:  # 如果已经访问过
                return 0
            else:
                visited.add((i, j))  # 访问标记
                return 1 + dfs(i + 1, j) + dfs(i, j + 1)  # 因为只能往左或往右，所以只需要搜索两个方向

        visited = set()
        return dfs(0, 0)
```

</details>

