## 剑指Offer_6400_求1~n的和（中等, 2022-01）
<!--{
    "tags": ["递归"],
    "来源": "剑指Offer",
    "编号": "6400",
    "难度": "中等",
    "标题": "求1~n的和"
}-->

<summary><b>问题简述</b></summary>

```txt
求 1+2+...+n ，要求不能使用乘除法、for、while、if、else、switch、case等关键字及三目运算符。
```

<details><summary><b>详细描述</b></summary>

```txt
求 1+2+...+n ，要求不能使用乘除法、for、while、if、else、switch、case等关键字及条件判断语句（A?B:C）。

示例 1：
    输入: n = 3
    输出: 6
示例 2：
    输入: n = 9
    输出: 45

限制：
    1 <= n <= 10000

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/qiu-12n-lcof
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```

</details>

<!-- <div align="center"><img src="../../../_assets/xxx.png" height="300" /></div> -->

<summary><b>思路</b></summary>

- 通过“短路”中止递归；
- 在 Python 中 `and` 操作如果最后结果为真，返回最后一个表达式的值，`or` 操作如果结果为真，返回第一个结果为真的表达式的值（写法2）；

<details><summary><b>Python：写法1</b></summary>

```python
class Solution:
    def __init__(self):
        self.res = 0

    def sumNums(self, n: int) -> int:
        n > 1 and self.sumNums(n - 1)  # 当 n <= 1 时，因为短路导致递归中止
        self.res += n
        return self.res
```

</details>

<details><summary><b>Python：写法2</b></summary>

```python
class Solution:
    def sumNums(self, n: int) -> int:
        return n > 0 and (n + self.sumNums(n-1))
```

</details>

