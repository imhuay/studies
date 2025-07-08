## 最长回文子串
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2022-10-16%2016%3A24%3A13&color=yellowgreen&style=flat-square)
[![](https://img.shields.io/static/v1?label=&message=%E4%B8%AD%E7%AD%89&color=yellow&style=flat-square)](../../../README.md#中等)
[![](https://img.shields.io/static/v1?label=&message=LeetCode&color=green&style=flat-square)](../../../README.md#leetcode)
[![](https://img.shields.io/static/v1?label=&message=%E5%8A%A8%E6%80%81%E8%A7%84%E5%88%92&color=blue&style=flat-square)](../../../README.md#动态规划)
[![](https://img.shields.io/static/v1?label=&message=%E5%8F%8C%E6%8C%87%E9%92%88&color=blue&style=flat-square)](../../../README.md#双指针)
[![](https://img.shields.io/static/v1?label=&message=LeetCode%20Hot%20100&color=blue&style=flat-square)](../../../README.md#leetcode-hot-100)

<!--END_SECTION:badge-->
<!--info
tags: [dp, 双指针, lc100]
source: LeetCode
level: 中等
number: '0005'
name: 最长回文子串
companies: []
-->

<summary><b>问题简述</b></summary>

```txt
给你一个字符串 s，找到 s 中最长的回文子串。
```
> [5. 最长回文子串 - 力扣（LeetCode）](https://leetcode-cn.com/problems/longest-palindromic-substring/)

<details><summary><b>详细描述</b></summary>

```txt
给你一个字符串 s，找到 s 中最长的回文子串。

示例 1：
    输入：s = "babad"
    输出："bab"
    解释："aba" 同样是符合题意的答案。
示例 2：
    输入：s = "cbbd"
    输出："bb"
示例 3：
    输入：s = "a"
    输出："a"
示例 4：
    输入：s = "ac"
    输出："a"

提示：
    1 <= s.length <= 1000
    s 仅由数字和英文字母（大写和/或小写）组成

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/longest-palindromic-substring
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```

</details>

<summary><b>思路1：动态规划</b></summary>

- 状态定义：`dp[i][j] := 子串 s[i:j] 是否为回文串`；
- 状态转移方程：`dp[i][j] := dp[i+1][j-1] == True 且 s[i] == s[j]`；
- 初始状态
    - 单个字符：`dp[i][j] := True` 当 `i == j` 
    - 两个连续相同字符：`dp[i][j] := True` 当 `j == i + 1 && s[i] == s[j]`
- 动态规划并不是最适合的解，这里仅提供一个思路；
- 如果要使用动态规划解本题，如何循环是关键，因为回文串的特点，从“双指针”的角度来看，需要从中心往两侧遍历，这跟大多数的 dp 问题略有不同；

<details><summary><b>C++</b></summary>

```cpp
class Solution {
public:
    string longestPalindrome(string s) {
        int n = s.length();

        vector<vector<int>> dp(n, vector<int>(n, 0));
        int max_len = 1;    // 保存最长回文子串长度
        int start = 0;      // 保存最长回文子串起点

        // 初始状态1：子串长度为 1 时，显然是回文子串
        for (int i = 0; i < n; i++)
            dp[i][i] = 1;

        //for (int j = 1; j < n; j++)         // 子串结束位置
        //    for (int i = 0; i < j; i++) {   // 子串起始位置
        // 上述循环方式也是可以的，但在 “最长回文子序列” 一题中会有问题
        // 下面的循环方式在两个问题中都正确，这个遍历思路比较像“中心扩散法”
        for (int j = 1; j < n; j++)             // 子串结束位置
            for (int i = j - 1; i >= 0; i--) {  // 子串开始位置
                if (j == i + 1)  // 初始状态2：子串长度为 2 时，只有当两个字母相同时才是回文子串
                    dp[i][j] = (s[i] == s[j]);
                else  // 状态转移方程：当上一个状态是回文串，且此时两个位置的字母也相同时，当前状态才是回文串
                    dp[i][j] = (dp[i + 1][j - 1] && s[i] == s[j]);

                // 保存最长回文子串
                if (dp[i][j] && max_len < (j - i + 1)) {
                    max_len = j - i + 1;
                    start = i;
                }
            }

        return s.substr(start, max_len);
    }
};
```

</details>

<details><summary><b>Python</b></summary>

```python
class Solution:
    def longestPalindrome(self, s: str) -> str:
        
        n = len(s)
        dp = [[0] * n for _ in range(n)]

        for i in range(n):
            dp[i][i] = 1
        
        start = 0
        length = 1
        for j in range(1, n):  # 子串的结束位置
            for i in range(j - 1, -1, -1):  # 子串的开始位置
                if i == j - 1:
                    dp[i][j] = 1 if s[i] == s[j] else 0
                else:
                    dp[i][j] = 1 if dp[i + 1][j - 1] and s[i] == s[j] else 0

                if dp[i][j]:
                    if j - i + 1 > length:
                        length = j - i + 1
                        start = i

        return s[start: start + length]
```

</details>

<summary><b>思路2：模拟-中心扩散（推荐）</b></summary>

- 按照回文的定义，遍历每个字符作为中点，向两边扩散；
- 注意奇数和偶数两种情况；

<details><summary><b>Python: 写法 1 (推荐, 不容易写错)</b></summary>

```python
class Solution:
    def longestPalindrome(self, s: str) -> str:

        self.ret = ''
        n = len(s)

        def process(l, r):
            tmp = ''
            # 从 s[l:r] 开始向两侧扩散
            while l >= 0 and r < n and s[l] == s[r]:
                tmp = s[l: r + 1]
                l, r = l - 1, r + 1
            
            if len(tmp) > len(self.ret):
                self.ret = tmp
        
        for i in range(n):  # 注意 i 的范围
            process(i, i)  # 奇数情况
            process(i, i + 1)  # 偶数情况
        
        return self.ret
```

</details>

<details><summary><b>Python: 写法 2</b></summary>

- 相比写法 1, 写法 2 少用了一个变量, 但是很容易写错;

```python
class Solution:
    def longestPalindrome(self, s: str) -> str:
        
        self.ret = s[0]
        n = len(s)

        def process(l, r):
            # 注意这里比较的时 s[l - 1] 和 s[r + 1]
            while l - 1 >= 0 and r + 1 < n and s[l - 1] == s[r + 1]:
                l, r = l - 1, r + 1
            
            if r - l + 1 > len(self.ret):
                self.ret = s[l: r + 1]
            
        for i in range(n - 1):
            process(i, i)  # 奇数情况
            if s[i] == s[i + 1]:  # 偶数情况,
                # 因为 process 中比较的是 s[l - 1] 和 s[r + 1], 所以要额外加一个判断条件
                process(i, i + 1)
        
        return self.ret
```

</details>
