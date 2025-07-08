## 解码方法
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2025-07-08%2016%3A53%3A13&color=yellowgreen&style=flat-square)
[![](https://img.shields.io/static/v1?label=&message=%E4%B8%AD%E7%AD%89&color=yellow&style=flat-square)](../../../README.md#中等)
[![](https://img.shields.io/static/v1?label=&message=LeetCode&color=green&style=flat-square)](../../../README.md#leetcode)
[![](https://img.shields.io/static/v1?label=&message=%E5%8A%A8%E6%80%81%E8%A7%84%E5%88%92&color=blue&style=flat-square)](../../../README.md#动态规划)
[![](https://img.shields.io/static/v1?label=&message=%E6%9A%B4%E5%8A%9B%E9%80%92%E5%BD%92%E4%B8%8E%E5%8A%A8%E6%80%81%E8%A7%84%E5%88%92&color=blue&style=flat-square)](../../../README.md#暴力递归与动态规划)

<!--END_SECTION:badge-->
<!--info
tags: [dp, dfs2dp]
source: LeetCode
level: 中等
number: '0091'
name: 解码方法
companies: []
-->

<summary><b>问题简述</b></summary>

```txt
将数字解码成字母，返回可能的解码方法数；
例如，"11106" 可以映射为：
    "AAJF" ，将消息分组为 (1 1 10 6)
    "KJF" ，将消息分组为 (11 10 6)
```
> [91. 解码方法 - 力扣（LeetCode）](https://leetcode-cn.com/problems/decode-ways/)

<!-- 
<details><summary><b>详细描述</b></summary>

```txt
```

</details>
-->


<!-- <div align="center"><img src="../../../_assets/xxx.png" height="300" /></div> -->

<summary><b>思路</b></summary>

- 有限制的  "跳台阶" 问题: `dp[i] = dp[i-1] + dp[i-2]`;
    - 只有当 `s[i]` 和 `s[i-1]` 满足某些条件时, 才能从 `dp[i-1]` 或 `dp[i-2]` "跳上来";

<details><summary><b>Python: 递归写法</b></summary>

```python
class Solution:
    def numDecodings(self, s: str) -> int:

        from functools import lru_cache

        @lru_cache
        def dfs(i):  # 前 i 个字符的解码方法数
            # 最容易出错的点, 以 0 开头的字符串不存在相应的编码
            if i <= 1: return int(s[0] != '0')

            ret = 0
            if '1' <= s[i - 1] <= '9':  # 如果 s[i] 在 0~9, 存在相应的编码
                ret += dfs(i - 1)  # s[i-1] == 1 和 s[i-2] 的特殊讨论
            if s[i - 2] == '1' or s[i - 2] == '2' and '0' <= s[i - 1] <= '6':
                ret += dfs(i - 2)
            
            return ret
        
        return dfs(len(s))
```

</details>

<details><summary><b>Python: 迭代写法 (与递归版一一对应)</b></summary>

```python
class Solution:
    def numDecodings(self, s: str) -> int:
        
        # if s[0] == '0': return 0

        dp = [0] * (len(s) + 1)
        # dp[0] = dp[1] = int(s[0] != '0')
        
        # 注意 i 的范围与递归中一致
        for i in range(len(s) + 1):
            # 下面就是把递归中的代码搬过来
            if i <= 1:  # 如果把这一段拿到循环外, 需要调整 i 的遍历范围
                dp[i] = int(s[0] != '0')
                continue
            dp[i] = 0
            if '1' <= s[i - 1] <= '9':
                dp[i] += dp[i - 1]
            if s[i - 2] == '1' or s[i - 2] == '2' and '0' <= s[i - 1] <= '6':
                dp[i] += dp[i - 2]
        
        return dp[-1]
```

</details>
