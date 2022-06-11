## 剑指Offer_5000_第一个只出现一次的字符（简单, 2021-12）
<!--{
    "tags": ["哈希表"],
    "来源": "剑指Offer",
    "编号": "5000",
    "难度": "简单",
    "标题": "第一个只出现一次的字符"
}-->

<summary><b>问题简述</b></summary>

```txt
在字符串 s 中找出第一个只出现一次的字符。如果没有，返回一个单空格。
```

<details><summary><b>详细描述</b></summary>

```txt
在字符串 s 中找出第一个只出现一次的字符。如果没有，返回一个单空格。 s 只包含小写字母。

示例 1:
    输入：s = "abaccdeff"
    输出：'b'
示例 2:
    输入：s = "" 
    输出：' '

限制：
    0 <= s 的长度 <= 50000

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/di-yi-ge-zhi-chu-xian-yi-ci-de-zi-fu-lcof
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```

</details>

<!-- <div align="center"><img src="../../../_assets/xxx.png" height="300" /></div> -->


<summary><b>思路1：哈希表</b></summary>

<details><summary><b>Python</b></summary>

```python
class Solution:
    def firstUniqChar(self, s: str) -> str:
        dic = defaultdict(int)  # python 3.6 之后 dict 默认就是有序的

        for c in s:
            dic[c] += 1

        for c in s:
            if dic[c] == 1: 
                return c

        return ' '
```

</details>


<summary><b>思路1：有序哈希表</b></summary>

<details><summary><b>Python</b></summary>

- python 3.6 之后 dict 默认就是有序的；
    > [为什么 Python 3.6 以后字典有序并且效率更高？](https://www.cnblogs.com/xieqiankun/p/python_dict.html)

```python
from collections import defaultdict

class Solution:
    def firstUniqChar(self, s: str) -> str:
        dic = defaultdict(int)  # python 3.6 之后 dict 默认就是有序的

        for c in s:
            dic[c] += 1

        for c, v in dic.items():
            if v == 1: 
                return c

        return ' '
```

</details>