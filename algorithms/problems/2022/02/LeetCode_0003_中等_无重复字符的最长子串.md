## 无重复字符的最长子串
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2022-10-14%2014%3A59%3A33&color=yellowgreen&style=flat-square)
[![](https://img.shields.io/static/v1?label=&message=%E4%B8%AD%E7%AD%89&color=yellow&style=flat-square)](../../../README.md#中等)
[![](https://img.shields.io/static/v1?label=&message=LeetCode&color=green&style=flat-square)](../../../README.md#leetcode)
[![](https://img.shields.io/static/v1?label=&message=%E6%BB%91%E5%8A%A8%E7%AA%97%E5%8F%A3&color=blue&style=flat-square)](../../../README.md#滑动窗口)
[![](https://img.shields.io/static/v1?label=&message=LeetCode%20Hot%20100&color=blue&style=flat-square)](../../../README.md#leetcode-hot-100)

<!--END_SECTION:badge-->
<!--info
tags: [滑动窗口, lc100]
source: LeetCode
level: 中等
number: '0003'
name: 无重复字符的最长子串
companies: []
-->

<summary><b>问题简述</b></summary>

```txt
给定一个字符串 s ，请你找出其中不含有重复字符的 最长子串 的长度。
```
> [3. 无重复字符的最长子串 - 力扣（LeetCode）](https://leetcode-cn.com/problems/longest-substring-without-repeating-characters/)

<!-- 
<details><summary><b>详细描述</b></summary>

```txt
```

</details>
-->


<!-- <div align="center"><img src="../../../_assets/xxx.png" height="300" /></div> -->

<summary><b>思路：滑动窗口</b></summary>

- 维护一个已经出现过的字符集合；

<details><summary><b>Python 写法1 （滑动窗口模板，推荐写法）</b></summary>

```python
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        
        used = set()
        l = r = 0  # 窗口边界
        ret = 0
        while r < len(s):
            while s[r] in used:  # 滑动左边界
                # 判断的是右边界，移动的是左边界
                used.remove(s[l])
                l += 1
            ret = max(ret, r - l + 1)
            used.add(s[r])
            r += 1
        return ret
```

</details>


<details><summary><b>Python 写法2 （优化）</b></summary>

- **优化**：直接移动 l 指针到重复字符的下一个位置，减少 l 指针移动；
```python
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        used = dict()
        l = r = 0  # [l, r] 闭区间
        ret = 0
        while r < len(s):
            if s[r] in used and l <= used[s[r]]:  # l <= used[s[r]] 的意思是重复字符出现在窗口内；
                l = used[s[r]] + 1
            ret = max(ret, r - l + 1)
            used[s[r]] = r
            r += 1
        return ret
```

</details>