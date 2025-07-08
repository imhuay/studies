## 打印从1到最大的n位数（N叉树的遍历）
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2022-10-14%2014%3A59%3A33&color=yellowgreen&style=flat-square)
[![](https://img.shields.io/static/v1?label=&message=%E4%B8%AD%E7%AD%89&color=yellow&style=flat-square)](../../../README.md#中等)
[![](https://img.shields.io/static/v1?label=&message=%E5%89%91%E6%8C%87Offer&color=green&style=flat-square)](../../../README.md#剑指offer)
[![](https://img.shields.io/static/v1?label=&message=%E6%B7%B1%E5%BA%A6%E4%BC%98%E5%85%88%E6%90%9C%E7%B4%A2&color=blue&style=flat-square)](../../../README.md#深度优先搜索)

<!--END_SECTION:badge-->
<!--info
tags: [DFS]
source: 剑指Offer
level: 中等
number: '1700'
name: 打印从1到最大的n位数（N叉树的遍历）
companies: []
-->

<summary><b>问题简述</b></summary>

```txt
输入数字 n，按顺序打印出从 1 到最大的 n 位十进制数（考虑大数情况）；
比如输入 3，则打印出 1~999
```

<details><summary><b>详细描述</b></summary>

```txt
输入数字 n，按顺序打印出从 1 到最大的 n 位十进制数。比如输入 3，则打印出 1、2、3 一直到最大的 3 位数 999。

示例 1:
    输入: n = 1
    输出: [1,2,3,4,5,6,7,8,9]

说明：
    用返回一个整数列表来代替打印
    n 为正整数

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/da-yin-cong-1dao-zui-da-de-nwei-shu-lcof
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```

</details>

<summary><b>思路</b></summary>

- 考虑大数情况下，直接遍历会存在越界问题；
- 本题实际上是一个 N 叉树（N=9）的遍历问题；

<!-- <div align="center"><img src="../../../_assets/xxx.png" height="300" /></div> -->

<details><summary><b>Python：不考虑大数</b></summary>

```python
class Solution:
    def printNumbers(self, n: int) -> List[int]:
        res = []
        for i in range(1, 10 ** n):
            res.append(i)
        return res
```

</details>

<details><summary><b>Python：考虑大数</b></summary>

```python
class Solution:
    def printNumbers(self, n: int) -> List[int]:

        ret = []
        dig = '0123456789'
        buf = [''] * n

        def process(buf):
            """去除前置0"""
            start = 0
            while start < n - 1 and buf[start] == '0':  # 保留至少一个 0
                start += 1
            return int(''.join(buf[start:]))  # LeetCode要求返回 int

        def dfs(k):
            """DFS全排列"""
            if k == n:
                ret.append(process(buf))
                return

            for i in dig:  # 每一位都有 0-9 10种取法
                buf[k] = i
                dfs(k+1)

        dfs(0)
        return ret[1:]  # 要求从 1 开始，故移除第一位
```

</details>

