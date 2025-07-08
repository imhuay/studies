## 括号生成
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2022-10-14%2014%3A59%3A33&color=yellowgreen&style=flat-square)
[![](https://img.shields.io/static/v1?label=&message=%E4%B8%AD%E7%AD%89&color=yellow&style=flat-square)](../../../README.md#中等)
[![](https://img.shields.io/static/v1?label=&message=LeetCode&color=green&style=flat-square)](../../../README.md#leetcode)
[![](https://img.shields.io/static/v1?label=&message=%E6%B7%B1%E5%BA%A6%E4%BC%98%E5%85%88%E6%90%9C%E7%B4%A2&color=blue&style=flat-square)](../../../README.md#深度优先搜索)
[![](https://img.shields.io/static/v1?label=&message=LeetCode%20Hot%20100&color=blue&style=flat-square)](../../../README.md#leetcode-hot-100)

<!--END_SECTION:badge-->
<!--info
tags: [dfs+回溯, lc100]
source: LeetCode
level: 中等
number: '0022'
name: 括号生成
companies: []
-->

> [22. 括号生成 - 力扣（LeetCode）](https://leetcode.cn/problems/generate-parentheses)

<summary><b>问题简述</b></summary>

```txt
数字 n 代表生成括号的对数，请你设计一个函数，用于能够生成所有可能的并且 有效的 括号组合。
```

<!-- 
<details><summary><b>详细描述</b></summary>

```txt
```

</details>
-->

<!-- <div align="center"><img src="../../../_assets/xxx.png" height="300" /></div> -->

<summary><b>思路</b></summary>

- 相当于对 `['(', ')']` 进行深度优先遍历；
- 通过剪枝排除无效情况；

    <div align="center"><img src="../../../_assets/LeetCode_0022_括号生成.png" height="300" /></div>

    > [回溯算法（深度优先遍历）+ 广度优先遍历（Java） - liweiwei1419](https://leetcode.cn/problems/generate-parentheses/solution/hui-su-suan-fa-by-liweiwei1419/)


<details><summary><b>Python（写法 1）</b></summary>

```python
class Solution:
    def generateParenthesis(self, n: int) -> List[str]:

        ret = []

        def dfs(l, r, tmp):
            # 非法情况（剪枝）
            if l < r or l > n:  # 已经包括 r > n
                return

            if l == r == n:
                ret.append(''.join(tmp))
                return
            
            # 先添加左括号
            tmp.append('(')
            dfs(l + 1, r, tmp)
            tmp.pop()

            # 再添加右括号
            tmp.append(')')
            dfs(l, r + 1, tmp)
            tmp.pop()

        dfs(0, 0, [])
        return ret
```

</details>

<details><summary><b>Python（写法 2，写法 1 的等价写法）</b></summary>

```python
class Solution:
    def generateParenthesis(self, n: int) -> List[str]:

        ret = []

        def dfs(l, r, tmp):
            # 非法情况
            if l < r or l > n:  # 已经包括 r > n
                return

            if l == r == n:
                ret.append(''.join(tmp))
                return
            
            for c in '()':
                # 注意 l 和 r 也要回溯，这里直接传表达式可以省略这一步；
                # 同样，如果不用 tmp 数组，而是传字符串表达式，那么 tmp 的回溯也可以省略（写法3）
                # if c == '(': l += 1
                # else: r += 1
                tmp.append(c)
                dfs(l + 1 if c == '(' else l, 
                    r + 1 if c == ')' else r, 
                    tmp)
                tmp.pop()
                # if c == '(': l -= 1
                # else: r -= 1

        dfs(0, 0, [])
        return ret
```

</details>

<details><summary><b>Python（写法 3，不回溯）</b></summary>

```python
class Solution:
    def generateParenthesis(self, n: int) -> List[str]:

        ret = []

        def dfs(l, r, tmp):
            # 非法情况
            if l < r or l > n:  # 已经包括 r > n
                return

            if l == r == n:
                ret.append(tmp)
                return

            for c in '()':
                # 不回溯的写法
                dfs(l + 1 if c == '(' else l, 
                    r + 1 if c == ')' else r, 
                    tmp + c)

        dfs(0, 0, '')
        return ret
```

</details>