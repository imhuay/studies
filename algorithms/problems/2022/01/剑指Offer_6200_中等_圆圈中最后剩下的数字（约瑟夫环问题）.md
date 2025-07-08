## 圆圈中最后剩下的数字（约瑟夫环问题）
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2022-10-14%2014%3A59%3A33&color=yellowgreen&style=flat-square)
[![](https://img.shields.io/static/v1?label=&message=%E4%B8%AD%E7%AD%89&color=yellow&style=flat-square)](../../../README.md#中等)
[![](https://img.shields.io/static/v1?label=&message=%E5%89%91%E6%8C%87Offer&color=green&style=flat-square)](../../../README.md#剑指offer)
[![](https://img.shields.io/static/v1?label=&message=%E6%A8%A1%E6%8B%9F&color=blue&style=flat-square)](../../../README.md#模拟)
[![](https://img.shields.io/static/v1?label=&message=%E5%8A%A8%E6%80%81%E8%A7%84%E5%88%92&color=blue&style=flat-square)](../../../README.md#动态规划)
[![](https://img.shields.io/static/v1?label=&message=%E7%BB%8F%E5%85%B8&color=blue&style=flat-square)](../../../README.md#经典)

<!--END_SECTION:badge-->
<!--info
tags: [模拟, 递推, 经典]
source: 剑指Offer
level: 中等
number: '6200'
name: 圆圈中最后剩下的数字（约瑟夫环问题）
companies: []
-->

<summary><b>问题简述</b></summary>

```txt
0 ~ n-1 这 n 个数字围成一个圆圈，从数字0开始，每次从这个圆圈里删除第 m 个数字（删除后从下一个数字开始计数）。求出这个圆圈里剩下的最后一个数字。
```

<details><summary><b>详细描述</b></summary>

```txt
0,1,···,n-1这n个数字排成一个圆圈，从数字0开始，每次从这个圆圈里删除第m个数字（删除后从下一个数字开始计数）。求出这个圆圈里剩下的最后一个数字。

例如，0、1、2、3、4这5个数字组成一个圆圈，从数字0开始每次删除第3个数字，则删除的前4个数字依次是2、0、4、1，因此最后剩下的数字是3。

示例 1：
    输入: n = 5, m = 3
    输出: 3
示例 2：
    输入: n = 10, m = 17
    输出: 2

限制：
    1 <= n <= 10^5
    1 <= m <= 10^6

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/yuan-quan-zhong-zui-hou-sheng-xia-de-shu-zi-lcof
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```

</details>

<!-- <div align="center"><img src="../../../_assets/xxx.png" height="300" /></div> -->

<summary><b>思路1：暴力解（超时）</b></summary>

<details><summary><b>Python</b></summary>

```python
class Solution:
    def lastRemaining(self, n: int, m: int) -> int:

        nums = list(range(n))
        idx = 0
        while len(nums) > 1:
            idx = (idx + m - 1) % len(nums)
            nums.pop(idx)
        
        return nums[0]
```

</details>


<summary><b>思路2：递推</b></summary>

- 虽然我们不知道这个最终的值是哪个，但是可以确定的是在最后一轮删除后，这个值在数组中的索引一定是 0（此时数组中只有一个值了）；
- 递推的目的就是每次还原这个值在上一轮所在的索引，直到第一轮，此时索引值就是目标值（因为 `nums = [0..n-1]`）；
- 记 `f(i)` 表示倒数第 `i` 轮时目标值所在的索引（`i>=1`），显然有 `f(1) = 0`；
- 递推公式：`f(i) = (f(i-1) + m) % i`（倒数第 `i` 轮，数组的长度也为 `i`，所以是对 `i` 取余）
    - `(f(i-1) + m) % i` 
- 关于递推公式的具体解析可以参`考「[换个角度举例解决约瑟夫环](https://leetcode-cn.com/problems/yuan-quan-zhong-zui-hou-sheng-xia-de-shu-zi-lcof/solution/huan-ge-jiao-du-ju-li-jie-jue-yue-se-fu-huan-by-as/)」


<details><summary><b>Python 递归</b></summary>

```python
class Solution:
    def lastRemaining(self, n: int, m: int) -> int:

        def f(i):
            if i == 1: return 0
            return (f(i - 1) + m) % i
        
        return f(n)
```

</details>

<details><summary><b>Python 迭代</b></summary>

```python
class Solution:
    def lastRemaining(self, n: int, m: int) -> int:

        idx = 0  # 因为最后一轮数组中只有一个值了，所以此时目标的索引一定是 0
        for i in range(2, n + 1):
            idx = (idx + m) % i  # 倒数第 i 轮时目标的索引
        
        # return nums[idx]
        return idx  # 因为 nums = [0..n-1]，所以 nums[idx] == idx
```

</details>
