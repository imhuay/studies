## LeetCode_0434_字符串中的单词数（简单, 2021-10）
<!--{
    "tags": ["字符串"],
    "来源": "LeetCode",
    "编号": "0434",
    "难度": "简单",
    "标题": "字符串中的单词数"
}-->

<summary><b>问题描述</b></summary>

```txt
统计字符串中的单词个数，这里的单词指的是连续的不是空格的字符。

请注意，你可以假定字符串里不包括任何不可打印的字符。

示例:
    输入: "Hello, my name is John"
    输出: 5
    解释: 这里的单词是指连续的不是空格的字符，所以 "Hello," 算作 1 个单词。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/number-of-segments-in-a-string
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```

<summary><b>思路</b></summary>

<details><summary><b>Python3</b></summary>

```python
class Solution:
    def countSegments(self, s):
        
        # 针对第一个字符初始化，注意处理空串
        ans = 0 if s == '' or s[0] == ' ' else 1

        for i in range(1, len(s)):
            if s[i] != ' ' and s[i - 1] == ' ':
                ans += 1

        return ans

```

</details>
