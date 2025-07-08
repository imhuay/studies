## 字符串中的单词数
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2025-07-08%2016%3A53%3A13&color=yellowgreen&style=flat-square)
[![](https://img.shields.io/static/v1?label=&message=%E7%AE%80%E5%8D%95&color=yellow&style=flat-square)](../../../README.md#简单)
[![](https://img.shields.io/static/v1?label=&message=LeetCode&color=green&style=flat-square)](../../../README.md#leetcode)
[![](https://img.shields.io/static/v1?label=&message=%E5%AD%97%E7%AC%A6%E4%B8%B2&color=blue&style=flat-square)](../../../README.md#字符串)

<!--END_SECTION:badge-->
<!--info
tags: [字符串]
source: LeetCode
level: 简单
number: '0434'
name: 字符串中的单词数
companies: []
-->

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
