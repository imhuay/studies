## 和为s的连续正数序列
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2022-10-14%2014%3A59%3A33&color=yellowgreen&style=flat-square)
[![](https://img.shields.io/static/v1?label=&message=%E7%AE%80%E5%8D%95&color=yellow&style=flat-square)](../../../README.md#简单)
[![](https://img.shields.io/static/v1?label=&message=%E5%89%91%E6%8C%87Offer&color=green&style=flat-square)](../../../README.md#剑指offer)
[![](https://img.shields.io/static/v1?label=&message=%E5%8F%8C%E6%8C%87%E9%92%88&color=blue&style=flat-square)](../../../README.md#双指针)

<!--END_SECTION:badge-->
<!--info
tags: [双指针]
source: 剑指Offer
level: 简单
number: '5702'
name: 和为s的连续正数序列
companies: []
-->

<summary><b>问题简述</b></summary>

```txt
输入一个正整数 target ，输出所有和为 target 的连续正整数序列（至少含有两个数）。
```

<details><summary><b>详细描述</b></summary>

```txt
输入一个正整数 target ，输出所有和为 target 的连续正整数序列（至少含有两个数）。

序列内的数字由小到大排列，不同序列按照首个数字从小到大排列。

示例 1：
    输入：target = 9
    输出：[[2,3,4],[4,5]]
示例 2：
    输入：target = 15
    输出：[[1,2,3,4,5],[4,5,6],[7,8]]

限制：
    1 <= target <= 10^5

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/he-wei-sde-lian-xu-zheng-shu-xu-lie-lcof
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```

</details>

<!-- <div align="center"><img src="../../../_assets/xxx.png" height="300" /></div> -->

<summary><b>思路1：双指针</b></summary>

```
1 初始化 左边界 l = 1 ，右边界 r = 2，结果列表 ret = []；
2 循环 当 l + r <= target 时：
    记 l 到 r 的连续和为 s
    当 s > target 时： 向右移动左边界 l += 1；
    当 s < target 时： 向右移动右边界 r += 1；
    当 s = target 时： 记录连续整数序列，左右边界同时右移，l += 1, r += 1；
3 返回结果列表 ret；

```

- **Tips**: 求连续和可以在移动双指针的过程中同步加减，并不需要每次用求和公式计算；

<details><summary><b>Python</b></summary>

```python
class Solution:
    def findContinuousSequence(self, target: int) -> List[List[int]]:

        l, r = 1, 2
        s = l + r

        ret = []
        while l + r <= target:
            if s > target:
                s -= l  # 先减
                l += 1
            elif s < target:
                r += 1
                s += r  # 后加
            else:
                ret.append(list(range(l, r + 1)))
                s -= l  # 先减
                l += 1
                r += 1
                s += r  # 后加

        return ret

```

</details>


<summary><b>思路2：数学</b></summary>

> [和为 s 的连续正数序列（求和公式 / 滑动窗口，清晰图解）](https://leetcode-cn.com/problems/he-wei-sde-lian-xu-zheng-shu-xu-lie-lcof/solution/jian-zhi-offer-57-ii-he-wei-s-de-lian-xu-t85z/)

- 当确定左边界和 target 时，可以通过求根公式得到右边界（去掉负根）；
- 当右边界为整数时得到一组解；

<details><summary><b>Python</b></summary>

```python
class Solution:
    def findContinuousSequence(self, target: int):
        i, j, res = 1, 2, []
        while i < j:
            # 当确定左边界和 target 时，可以通过求根公式得到右边界（去掉负根）
            j = (-1 + (1 + 4 * (2 * target + i * i - i)) ** 0.5) / 2
            # 当 j 为整数时得到一组解
            if i < j and j == int(j):
                res.append(list(range(i, int(j) + 1)))
            i += 1
        return res
```

</details>
