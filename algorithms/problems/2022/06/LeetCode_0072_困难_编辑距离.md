## 编辑距离
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2022-10-29%2023%3A59%3A13&color=yellowgreen&style=flat-square)
[![](https://img.shields.io/static/v1?label=&message=%E5%9B%B0%E9%9A%BE&color=yellow&style=flat-square)](../../../README.md#困难)
[![](https://img.shields.io/static/v1?label=&message=LeetCode&color=green&style=flat-square)](../../../README.md#leetcode)
[![](https://img.shields.io/static/v1?label=&message=%E5%8A%A8%E6%80%81%E8%A7%84%E5%88%92&color=blue&style=flat-square)](../../../README.md#动态规划)
[![](https://img.shields.io/static/v1?label=&message=%E7%BB%8F%E5%85%B8&color=blue&style=flat-square)](../../../README.md#经典)
[![](https://img.shields.io/static/v1?label=&message=%E7%83%AD%E9%97%A8&color=blue&style=flat-square)](../../../README.md#热门)

<!--END_SECTION:badge-->
<!--info
tags: [动态规划, 经典, 热门]
source: LeetCode
level: 困难
number: '0072'
name: 编辑距离
companies: []
-->

<summary><b>问题简述</b></summary>

```txt
给你两个单词 word1 和 word2，请你计算出将 word1 转换成 word2 所使用的最少操作数。
```

<details><summary><b>详细描述</b></summary>

```txt
给你两个单词 word1 和 word2，请你计算出将 word1 转换成 word2 所使用的最少操作数。

你可以对一个单词进行如下三种操作：
    插入一个字符
    删除一个字符
    替换一个字符

示例 1：
    输入：word1 = "horse", word2 = "ros"
    输出：3
    解释：
    horse -> rorse (将 'h' 替换为 'r')
    rorse -> rose (删除 'r')
    rose -> ros (删除 'e')
示例 2：
    输入：word1 = "intention", word2 = "execution"
    输出：5
    解释：
    intention -> inention (删除 't')
    inention -> enention (将 'i' 替换为 'e')
    enention -> exention (将 'n' 替换为 'x')
    exention -> exection (将 'n' 替换为 'c')
    exection -> execution (插入 'u')

提示：
    0 <= word1.length, word2.length <= 500
    word1 和 word2 由小写英文字母组成

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/edit-distance
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```

</details>

<!-- <div align="center"><img src="../../../_assets/xxx.png" height="300" /></div> -->

<summary><b>思路</b></summary>

- 动态规划经典问题 > [编辑距离 - 力扣官方题解](https://leetcode-cn.com/problems/edit-distance/solution/bian-ji-ju-chi-by-leetcode-solution/)

- Tips：“插入”和“删除”操作可以认为是同一种操作，因为编辑距离具有对称性，在一方中插入，等价于在另一方删除，这有助于理解代码；

<details><summary><b>Python</b></summary>

```python
class Solution:
    def minDistance(self, word1: str, word2: str) -> int:

        m = len(word1)
        n = len(word2)

        if m * n == 0:  # 其中一个是空串
            return m + n
        
        dp = [[0] * (n + 1) for _ in range(m + 1)]  # m * n
        
        for i in range(1, m + 1):
            dp[i][0] = i
        for i in range(1, n + 1):
            dp[0][i] = i
        
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                r1 = dp[i - 1][j] + 1
                r2 = dp[i][j - 1] + 1
                r3 = dp[i - 1][j - 1]
                if word1[i - 1] != word2[j - 1]:
                    r3 += 1
                dp[i][j] = min(r1, r2, r3)
        
        return dp[m][n]
```

</details>

**优化**：利用**滚动数组**将空间复杂度从 `O(MN)` 优化到 `min(O(N), O(M))`

<details><summary><b>Python</b></summary>

```python
class Solution:
    def minDistance(self, word1: str, word2: str) -> int:

        m = len(word1)
        n = len(word2)

        if m * n == 0:  # 其中一个是空串
            return m + n

        if m < n:
            m, n = n, m
            word1, word2 = word2, word1
        
        dp_pre = [0] * (n + 1)
        for i in range(1, n + 1):
            dp_pre[i] = i
        
        for i in range(1, m + 1):
            dp_cur = [i] + [0] * n
            for j in range(1, n + 1):
                r1 = dp_cur[j - 1] + 1
                r2 = dp_pre[j] + 1
                r3 = dp_pre[j - 1]
                if word1[i - 1] != word2[j - 1]:
                    r3 += 1
                dp_cur[j] = min(r1, r2, r3)
            dp_pre = dp_cur
        
        return dp_cur[n]
```

</details>