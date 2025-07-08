## 正则表达式匹配
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2022-10-14%2014%3A59%3A33&color=yellowgreen&style=flat-square)
[![](https://img.shields.io/static/v1?label=&message=%E5%9B%B0%E9%9A%BE&color=yellow&style=flat-square)](../../../README.md#困难)
[![](https://img.shields.io/static/v1?label=&message=LeetCode&color=green&style=flat-square)](../../../README.md#leetcode)
[![](https://img.shields.io/static/v1?label=&message=%E5%8A%A8%E6%80%81%E8%A7%84%E5%88%92&color=blue&style=flat-square)](../../../README.md#动态规划)
[![](https://img.shields.io/static/v1?label=&message=LeetCode%20Hot%20100&color=blue&style=flat-square)](../../../README.md#leetcode-hot-100)

<!--END_SECTION:badge-->
<!--info
tags: [动态规划, lc100]
source: LeetCode
level: 困难
number: '0010'
name: 正则表达式匹配
companies: []
-->

<summary><b>问题简述</b></summary>

```txt
请实现一个函数用来匹配包含'.'和'*'的正则表达式。
```
> [10. 正则表达式匹配 - 力扣（LeetCode）](https://leetcode-cn.com/problems/regular-expression-matching/)

</details>

<!-- <div align="center"><img src="../../../_assets/xxx.png" height="300" /></div> -->

<summary><b>思路：动态规划</b></summary>

- 定义 `dp(i, j)` 表示 `s[:i]` 与 `p[:j]` 是否匹配；
- 难点是要把所有情况考虑全面，尤其是初始化，以及 `p[j-1] == '*'` 的情况；

<details><summary><b>Python（递归写法）</b></summary>

```python
class Solution:
    def isMatch(self, s: str, p: str) -> bool:

        from functools import lru_cache

        @lru_cache(maxsize=None)
        def dp(i, j):  # s[:i] 和 p[:j] 是否匹配
            if i == 0 and j == 0: return True  # 空串和空串
            if j == 0: return False
            # s='' 时，p='a*' 或 'a*b*' 等
            if i == 0: return p[j - 1] == '*' and dp(i, j - 2)

            # s='abc' 时，p='abc' 或 'ab.'
            r1 = (s[i - 1] == p[j - 1] or p[j - 1] == '.') and dp(i - 1, j - 1)
            # '*'匹配了 0 个字符的情况，比如 s='ab', p='abc*'
            r2 = p[j - 1] == '*' and dp(i, j - 2)
            # '*'匹配了 1 个以上的字符，比如 s='abc', p='abc*' 或 'ab.*'
            r3 = p[j - 1] == '*' and (s[i - 1] == p[j - 2] or p[j - 2] == '.') and dp(i - 1, j)
            
            return r1 or r2 or r3

        m, n = len(s), len(p)
        return dp(m, n)
```

</details>


<details><summary><b>Python（迭代写法）</b></summary>

```python
class Solution:
    def isMatch(self, s: str, p: str) -> bool:

        m, n = len(s), len(p)
        dp = [[False] * (n + 1) for _ in range(m + 1)]

        # 初始化，对应递归中的 base case
        # dp[0][0] = True
        # for j in range(2, n + 1):
        #     dp[0][j] = p[j - 1] == '*' and dp[0][j - 2]

        # 为了展示“无缝转换”，把上面的初始化代码也写到了循环里面，两种写法都可以
        for i in range(0, m + 1):
            for j in range(0, n + 1):
                if i == 0 and j == 0: dp[i][j] = True
                elif j == 0: continue
                elif i == 0: dp[i][j] = p[j - 1] == '*' and dp[0][j - 2]
                else:
                    r1 = (s[i - 1] == p[j - 1] or p[j - 1] == '.') and dp[i - 1][j - 1]
                    r2 = p[j - 1] == '*' and dp[i][j - 2]
                    r3 = p[j - 1] == '*' and (s[i - 1] == p[j - 2] or p[j - 2] == '.') and dp[i - 1][j]
                    dp[i][j] = r1 or r2 or r3

        return dp[m][n]
```

</details>
