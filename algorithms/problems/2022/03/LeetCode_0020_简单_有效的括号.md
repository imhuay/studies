## LeetCode_0020_有效的括号（简单, 2022-03）
<!--{
    "tags": ["栈"],
    "来源": "LeetCode",
    "难度": "简单",
    "编号": "0020",
    "标题": "有效的括号",
    "公司": []
}-->

<summary><b>问题简述</b></summary>

```txt
给定一个只包括 '('，')'，'{'，'}'，'['，']' 的字符串 s ，判断字符串是否有效。
有效字符串需满足：
    左括号必须用相同类型的右括号闭合。
    左括号必须以正确的顺序闭合。
```
> [20. 有效的括号 - 力扣（LeetCode）](https://leetcode-cn.com/problems/valid-parentheses/)

<!-- 
<details><summary><b>详细描述</b></summary>

```txt
```

</details>
-->


<!-- <div align="center"><img src="../../../_assets/xxx.png" height="300" /></div> -->

<summary><b>思路</b></summary>

- 利用栈，遇到左括号就压栈，遇到右括号就出栈；
- 无效的情况：栈顶与当前遇到的右括号不匹配，或栈为空；
- 当遍历完所有字符，且栈为空时，即有效；

<details><summary><b>Python</b></summary>

```python
class Solution:
    def isValid(self, s: str) -> bool:
        """"""
        N = len(s)
        # 奇数情况一定无效
        if N % 1: return False

        # 小技巧，遇到左括号，压入对应的右扩招，这样遇到右括号对比时，直接比较即可
        book = {'(': ')', '[': ']', '{': '}'}

        stk = []
        for c in s:
            if c in book:
                stk.append(book[c])
            else:
                # 如果栈为空，或者栈顶不匹配，无效
                if not stk or stk[-1] != c: 
                    return False
                stk.pop()

        return len(stk) == 0
```

</details>

