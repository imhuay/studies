## 正则表达式匹配
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2022-10-14%2014%3A59%3A33&color=yellowgreen&style=flat-square)
[![](https://img.shields.io/static/v1?label=&message=%E5%9B%B0%E9%9A%BE&color=yellow&style=flat-square)](../../../README.md#困难)
[![](https://img.shields.io/static/v1?label=&message=%E5%89%91%E6%8C%87Offer&color=green&style=flat-square)](../../../README.md#剑指offer)
[![](https://img.shields.io/static/v1?label=&message=%E5%AD%97%E7%AC%A6%E4%B8%B2&color=blue&style=flat-square)](../../../README.md#字符串)
[![](https://img.shields.io/static/v1?label=&message=%E5%8A%A8%E6%80%81%E8%A7%84%E5%88%92&color=blue&style=flat-square)](../../../README.md#动态规划)
[![](https://img.shields.io/static/v1?label=&message=%E9%80%92%E5%BD%92&color=blue&style=flat-square)](../../../README.md#递归)

<!--END_SECTION:badge-->
<!--info
tags: [字符串, 动态规划, 递归]
source: 剑指Offer
level: 困难
number: '1900'
name: 正则表达式匹配
companies: []
-->

<summary><b>问题简述</b></summary>

```txt
请实现一个函数用来匹配包含'.'和'*'的正则表达式。
```

<details><summary><b>详细描述</b></summary>

```txt
请实现一个函数用来匹配包含'.'和'*'的正则表达式。模式中的字符'.'表示任意一个字符，而'*'表示它前面的字符可以出现任意次（含0次）。在本题中，匹配是指字符串的所有字符匹配整个模式。例如，字符串"aaa"与模式"a.a"和"ab*ac*a"匹配，但与"aa.a"和"ab*a"均不匹配。

示例 1:
    输入:
    s = "aa"
    p = "a"
    输出: false
    解释: "a" 无法匹配 "aa" 整个字符串。
示例 2:
    输入:
    s = "aa"
    p = "a*"
    输出: true
    解释: 因为 '*' 代表可以匹配零个或多个前面的那一个元素, 在这里前面的元素就是 'a'。因此，字符串 "aa" 可被视为 'a' 重复了一次。
示例 3:
    输入:
    s = "ab"
    p = ".*"
    输出: true
    解释: ".*" 表示可匹配零个或多个（'*'）任意字符（'.'）。
示例 4:
    输入:
    s = "aab"
    p = "c*a*b"
    输出: true
    解释: 因为 '*' 表示零个或多个，这里 'c' 为 0 个, 'a' 被重复一次。因此可以匹配字符串 "aab"。
示例 5:
    输入:
    s = "mississippi"
    p = "mis*is*p*."
    输出: false
    s 可能为空，且只包含从 a-z 的小写字母。
    p 可能为空，且只包含从 a-z 的小写字母以及字符 . 和 *，无连续的 '*'。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/zheng-ze-biao-da-shi-pi-pei-lcof
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```

</details>

<!-- <div align="center"><img src="../../../_assets/xxx.png" height="300" /></div> -->

<summary><b>思路：动态规划</b></summary>

> [正则表达式匹配（动态规划，清晰图解） - Krahets](https://leetcode-cn.com/problems/zheng-ze-biao-da-shi-pi-pei-lcof/solution/jian-zhi-offer-19-zheng-ze-biao-da-shi-pi-pei-dong/)

- 记主串为 `s`，模式串为 `p`；
- 将 `s` 的前 i 个 字符记为 `s[:i]`，p 的前 j 个字符记为 `p[:j]`；
- 整体思路是从 `s[:1]` 和 `p[:1]` 开始，判断 `s[:i]` 和 `p[:j]` 能否匹配；


<details><summary><b>Python</b></summary>

```python
class Solution:
    def isMatch(self, s: str, p: str) -> bool:
        m, n = len(s), len(p)

        # dp[i][j] := 代表字符串 s 的前 i 个字符和 p 的前 j 个字符能否匹配
        dp = [[False] * (n + 1) for _ in range(m + 1)]

        dp[0][0] = True  # ‘空主串’与‘空模式串’匹配

        # 初始化首行：‘空主串’与‘特殊模式串’匹配（如 a*、a*b* 等）
        for j in range(2, n + 1, 2):
            dp[0][j] = dp[0][j - 2] and p[j - 1] == '*'

        # 状态转移
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                # 便于理解，记 s[I] == s[i - 1] 表示 s 的第 i 个字符，p[J] 同理
                I, J = i - 1, j - 1
                # 根据 p 的 第 j 个字符是否为 *，分两种情况讨论
                if p[J] != '*':
                    # s[:i-1] 与 p[:j-1] 匹配的前提下，‘s 的第 i 个字符 == p 的第 j 个字符’ 或 ‘p 的第 j 个字符是 .’
                    #   这里 s[i-1] 和 p[j-1] 分别表示的是 s 和 p 的第 i 个和第 j 个字符
                    if dp[i - 1][j - 1] and (s[I] == p[J] or p[J] == '.'):
                        dp[i][j] = True
                else:  # 当 p[J] == '*' 时
                    # 情况1：* 匹配了 0 个字符，如 'a' 和 'ab*'
                    if dp[i][j - 2]:
                        dp[i][j] = True
                    # 情况2：* 匹配了至少一个字符，如 'ab' 和 'ab*'
                    #   dp[i - 1][j] == True 表示在 '[a]b' 和 '[ab*]' 中括号部分匹配的前提下，
                    #   再看 s[I] 与 p[J-1] 是否相同，或者 p[J-1] 是否为 .
                    elif dp[i - 1][j] and (s[I] == p[J - 1] or p[J - 1] == '.'):
                        dp[i][j] = True

        return dp[m][n]
```

</details>

<summary><b>思路2：递归</b></summary>

- 看到一份非常简洁的递归代码；
    > 见[正则表达式匹配（动态规划，清晰图解） - 评论区](https://leetcode-cn.com/problems/zheng-ze-biao-da-shi-pi-pei-lcof/solution/jian-zhi-offer-19-zheng-ze-biao-da-shi-pi-pei-dong/)

<details><summary><b>C++</b></summary>

```cpp
class Solution {
public:
    bool isMatch(string s, string p) 
    {
        if (p.empty()) 
            return s.empty();
        
        bool first_match = !s.empty() && (s[0] == p[0] || p[0] == '.');
        
        // *前字符重复>=1次 || *前字符重复0次（不出现）
        if (p.size() >= 2 && p[1] == '*')  
            return (first_match && isMatch(s.substr(1), p)) || isMatch(s, p.substr(2));
        else  // 不是*，减去已经匹配成功的头部，继续比较
            return first_match && isMatch(s.substr(1), p.substr(1));    
    }
};
```

</details>
