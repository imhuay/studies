## LeetCode_0091_解码方法（中等, 2022-02）
<!--{
    "tags": ["DP", "DFS2DP"],
    "来源": "LeetCode",
    "难度": "中等",
    "编号": "0091",
    "标题": "解码方法",
    "公司": []
}-->

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

<summary><b>思路1：从左往右的暴力递归</b></summary>

- 定义 `dfs(i)` 表示 `s[:i]` 已经固定的情况下，`s[i:]` 的解码方法；
- 【递归基】`i=n` 时，`s[:n]` 都固定了，即表示找到了一种解法方法；
- 本题的难点是 `dfs(i)` 不光可以从 `dfs(i-1)` 递推，还可以从 `dfs(i-2)` 递推；
    > 可以看做是有限制的跳台阶问题；

<details><summary><b>Python</b></summary>

```python
class Solution:
    def numDecodings(self, s: str) -> int:

        from functools import lru_cache  # 记忆化搜索

        n = len(s)  # 字符长度

        @lru_cache(maxsize=None)
        def dfs(i):  # 表示 s[:i] 已经固定的情况下，s[i:] 的解码方法
            if i == n:  # s[:n] 都已经固定，即找到了一种有效的解码方法
                ret = 1
            elif s[i] == '0':  # 以 0 开始的字符不存在有效解码
                ret = 0
            elif s[i] == '1':  # 如果以 1 开头，可以尝试两个位置
                ret = dfs(i + 1)  # 这个 1 已经固定了
                if i + 1 < n:  # 因为 10 ~ 19 都存在有效解码，因此只要后面存在两个字符，就可以加上 dfs(i + 2)
                    ret += dfs(i + 2)
            elif s[i] == '2':  # 如果以 2 开头，可以有条件的尝试两个位置
                ret = dfs(i + 1)
                if i + 1 < n and '0' <= s[i + 1] <= '6':
                    ret += dfs(i + 2)
            else:  # 如果以 3~9 开头，只能尝试一个位置
                ret = dfs(i + 1)

            return ret

        return dfs(0)
```

</details>


<summary><b>思路2：将暴力递归转化为动态规划</b></summary>

- 有了递归过程后，就可以脱离原问题，模板化的将其转化为动态规划。

<details><summary><b>Python</b></summary>

```python
class Solution:
    def numDecodings(self, s: str) -> int:

        n = len(s)  # 字符长度
        dp = [0] * (n + 1)

        # 初始化（对应递归中的 base case）
        #   i == n 时 ret = 1，即
        dp[n] = 1

        # 递推过程：对应递归过程填空
        #   下面的写法略有冗余，可以做一些合并，但是为了做到跟递归一一对应，就没有修改
        for i in range(n - 1, -1, -1):
            # 为什么是倒序遍历，一方面可以从问题理解；
            #   另一方面可以从递归过程看，因为最后返回的是 dp[0]，同时 dp[i] 需要从  dp[i + 1] 递推，所以显然需要逆序遍历
            if s[i] == '0':
                dp[i] = 0  # ret = 0
            elif s[i] == '1':
                dp[i] = dp[i + 1]  # ret = rec(i + 1)
                if i + 1 < n:
                    dp[i] += dp[i + 2]  # ret += rec(i + 2)
            elif s[i] == '2':
                dp[i] = dp[i + 1]  # ret = rec(i + 1)
                if i + 1 < n and '0' <= s[i + 1] <= '6':
                    dp[i] += dp[i + 2]  # ret += rec(i + 2)
            else:
                dp[i] = dp[i + 1]  # ret = rec(i + 1)

        return dp[0]  # return rec(0)
```

</details>

