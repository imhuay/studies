## LeetCode_0474_一和零（中等, 2022-02）
<!--{
    "tags": ["DFS2DP"],
    "来源": "LeetCode",
    "难度": "中等",
    "编号": "0474",
    "标题": "一和零",
    "公司": []
}-->

<summary><b>问题简述</b></summary>

```txt
给你一个二进制字符串数组 strs 和两个整数 m 和 n 。
请你找出并返回 strs 的最大子集的长度，该子集中 最多 有 m 个 0 和 n 个 1 。
如果 x 的所有元素也是 y 的元素，集合 x 是集合 y 的 子集 。
```
> [474. 一和零 - 力扣（LeetCode）](https://leetcode-cn.com/problems/ones-and-zeroes/)

<!-- 
<details><summary><b>详细描述</b></summary>

```txt
```

</details>
-->


<!-- <div align="center"><img src="../../../_assets/xxx.png" height="300" /></div> -->

<summary><b>思路：自底向上递归+记忆化搜索</b></summary>

- 定义 `dfs(i, rest_z, rest_o)` 表示剩余容量为 `rest_z`, `rest_o` 情况下，前 `i` 个元素的最大子集长度（子问题）；
- 【递归基】显然 `i=0` 时，返回 `0`；
- 然后分是否加入当前元素，返回其中的最大值；
- 记得预处理所有字符串；

<details><summary><b>Python</b></summary>

```python
class Solution:
    def findMaxForm(self, strs: List[str], m: int, n: int) -> int:

        from functools import lru_cache
        
        def get_zo(s):
            z, o = 0, 0
            for c in s:
                if c == '0': z += 1
                else: o += 1
            return z, o

        # 预处理
        tb = dict()
        for s in strs:
            tb[s] = get_zo(s)

        @lru_cache(maxsize=None)
        def dfs(i, rest_z, rest_o):  # 剩余容量为 rest_z, rest_o 情况下，strs[:i] 下的最大子集长度
            if i == 0:
                return 0
            
            c1 = dfs(i - 1, rest_z, rest_o)  # 不要
            c2 = 0
            z, o = tb[strs[i - 1]]
            if rest_z >= z and rest_o >= o:  # 要
                c2 = dfs(i - 1, rest_z - z, rest_o - o) + 1
            
            return max(c1, c2)
        
        N = len(strs)
        return dfs(N, m, n)
```

</details>

**优化**：通过递归转动态规划
> 实际上，记忆化搜索的速度要更快；

<details><summary><b>Python</b></summary>

```python
class Solution:
    def findMaxForm(self, strs: List[str], m: int, n: int) -> int:

        from functools import lru_cache
        
        def get_zo(s):
            z, o = 0, 0
            for c in s:
                if c == '0': z += 1
                else: o += 1
            return z, o

        N = len(strs)
        # 预处理
        tb = dict()
        for s in strs:
            tb[s] = get_zo(s)

        # dp[N][m][n]
        dp = [[[0] * (n + 1) for _ in range(m + 1)] for _ in range(N + 1)]

        for i in range(1, N + 1):
            for rest_z in range(m + 1):
                for rest_o in range(n + 1):
                    c1 = dp[i - 1][rest_z][rest_o]
                    c2 = 0
                    z, o = tb[strs[i - 1]]
                    if rest_z >= z and rest_o >= o:
                        c2 = dp[i - 1][rest_z - z][rest_o - o] + 1
                    dp[i][rest_z][rest_o] = max(c1, c2)
        
        return dp[N][m][n]
```

</details>


**空间优化**（略）
> [【宫水三叶】详解如何转换「背包问题」，以及逐步空间优化 - 一和零 - 力扣（LeetCode）](https://leetcode-cn.com/problems/ones-and-zeroes/solution/gong-shui-san-xie-xiang-jie-ru-he-zhuan-174wv/)