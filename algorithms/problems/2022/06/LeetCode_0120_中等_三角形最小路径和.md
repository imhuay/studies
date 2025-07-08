## 三角形最小路径和
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2025-07-08%2016%3A53%3A13&color=yellowgreen&style=flat-square)
[![](https://img.shields.io/static/v1?label=&message=%E4%B8%AD%E7%AD%89&color=yellow&style=flat-square)](../../../README.md#中等)
[![](https://img.shields.io/static/v1?label=&message=LeetCode&color=green&style=flat-square)](../../../README.md#leetcode)
[![](https://img.shields.io/static/v1?label=&message=%E5%8A%A8%E6%80%81%E8%A7%84%E5%88%92&color=blue&style=flat-square)](../../../README.md#动态规划)

<!--END_SECTION:badge-->
<!--info
tags: [动态规划]
source: LeetCode
level: 中等
number: '0120'
name: 三角形最小路径和
companies: []
-->

<summary><b>问题简述</b></summary>

```txt
给定一个三角形 triangle ，找出自顶向下的最小路径和。
```

<details><summary><b>详细描述</b></summary>

```txt
给定一个三角形 triangle ，找出自顶向下的最小路径和。

每一步只能移动到下一行中相邻的结点上。相邻的结点 在这里指的是 下标 与 上一层结点下标 相同或者等于 上一层结点下标 + 1 的两个结点。也就是说，如果正位于当前行的下标 i ，那么下一步可以移动到下一行的下标 i 或 i + 1 。

示例 1：
    输入：triangle = [[2],[3,4],[6,5,7],[4,1,8,3]]
    输出：11
    解释：如下面简图所示：
    2
    3 4
    6 5 7
    4 1 8 3
    自顶向下的最小路径和为 11（即，2 + 3 + 5 + 1 = 11）。
示例 2：
    输入：triangle = [[-10]]
    输出：-10

提示：
    1 <= triangle.length <= 200
    triangle[0].length == 1
    triangle[i].length == triangle[i - 1].length + 1
    -10^4 <= triangle[i][j] <= 10^4
 

进阶：

你可以只使用 O(n) 的额外空间（n 为三角形的总行数）来解决这个问题吗？

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/triangle
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```

</details>

<!-- <div align="center"><img src="../../../_assets/xxx.png" height="300" /></div> -->

<summary><b>思路：动态规划</b></summary>

- 思路跟[网格版的最小路径和](https://leetcode-cn.com/problems/minimum-path-sum/)基本相同，就是路线方向略有不同，模拟路线即可；

<details><summary><b>Python</b></summary>

```python
class Solution:
    def minimumTotal(self, triangle: List[List[int]]) -> int:
        if not triangle: return 0

        dp = [triangle[0][0]]
        for i in range(1, len(triangle)):
            dp = [dp[0] + triangle[i][0]] + dp  # 加上最左路
            for j in range(1, len(triangle[i])):
                if j == len(triangle[i]) - 1:  # 特殊处理最右路
                    dp[j] = dp[j] + triangle[i][j]
                else:  # 因为提前改变了 dp 的长度，所以不能写成 min(dp[j], dp[j - 1])，这里踩了个小坑
                    dp[j] = min(dp[j], dp[j + 1]) + triangle[i][j]
            
            # print(dp)
        
        return min(dp)
```

</details>

