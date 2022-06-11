## LeetCode_0003_无重复字符的最长子串（中等, 2022-02）
<!--{
    "tags": ["滑动窗口"],
    "来源": "LeetCode",
    "难度": "中等",
    "编号": "0003",
    "标题": "无重复字符的最长子串",
    "公司": []
}-->

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

- 维护一个已经出现过的字符集合，详见代码；

<details><summary><b>Python</b></summary>

```python
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        
        used = set()
        l = r = 0  # 窗口边界
        ret = 0
        while r < len(s):
            while s[r] in used:  # 如果已经出现过则移出
                # 注意这里要 while 判断，因为 l 指针不一定刚好指向这个重复的字符，要一直移动直到把 r 指向的字符移出
                used.remove(s[l])
                l += 1
            ret = max(ret, r - l + 1)
            used.add(s[r])
            r += 1
        return ret
```

</details>


**优化**：直接移动 l 指针到重复字符的下一个位置，减少 l 指针移动；

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