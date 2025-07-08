## 栈的压入、弹出序列
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2025-07-08%2016%3A53%3A13&color=yellowgreen&style=flat-square)
[![](https://img.shields.io/static/v1?label=&message=%E4%B8%AD%E7%AD%89&color=yellow&style=flat-square)](../../../README.md#中等)
[![](https://img.shields.io/static/v1?label=&message=%E5%89%91%E6%8C%87Offer&color=green&style=flat-square)](../../../README.md#剑指offer)
[![](https://img.shields.io/static/v1?label=&message=%E6%A0%88/%E9%98%9F%E5%88%97&color=blue&style=flat-square)](../../../README.md#栈队列)
[![](https://img.shields.io/static/v1?label=&message=%E6%95%B0%E7%BB%84/%E7%9F%A9%E9%98%B5&color=blue&style=flat-square)](../../../README.md#数组矩阵)
[![](https://img.shields.io/static/v1?label=&message=%E7%BB%8F%E5%85%B8&color=blue&style=flat-square)](../../../README.md#经典)

<!--END_SECTION:badge-->
<!--info
tags: [栈, 数组, 经典]
source: 剑指Offer
level: 中等
number: '3100'
name: 栈的压入、弹出序列
companies: []
-->

<summary><b>问题简述</b></summary>

```txt
输入两个整数序列，第一个序列表示栈的压入顺序，请判断第二个序列是否为该栈的弹出顺序。
假设压入栈的所有数字均不相等。
```

<details><summary><b>详细描述</b></summary>

```txt
输入两个整数序列，第一个序列表示栈的压入顺序，请判断第二个序列是否为该栈的弹出顺序。假设压入栈的所有数字均不相等。
例如，序列 {1,2,3,4,5} 是某栈的压栈序列，序列 {4,5,3,2,1} 是该压栈序列对应的一个弹出序列，但 {4,3,5,1,2} 就不可能是该压栈序列的弹出序列。

示例 1：
    输入：pushed = [1,2,3,4,5], popped = [4,5,3,2,1]
    输出：true
    解释：我们可以按以下顺序执行：
    push(1), push(2), push(3), push(4), pop() -> 4,
    push(5), pop() -> 5, pop() -> 3, pop() -> 2, pop() -> 1
示例 2：
    输入：pushed = [1,2,3,4,5], popped = [4,3,5,1,2]
    输出：false
    解释：1 不能在 2 之前弹出。

提示：
    0 <= pushed.length == popped.length <= 1000
    0 <= pushed[i], popped[i] < 1000
    pushed 是 popped 的排列。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/zhan-de-ya-ru-dan-chu-xu-lie-lcof
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```

</details>

<!-- <div align="center"><img src="../../../_assets/xxx.png" height="300" /></div> -->

<summary><b>思路</b></summary>

- 设置一个模拟栈 s，将 pushed 中的元素顺序入栈；
- 期间，如果 popped 中的元素与 s 栈顶元素相同，则弹出栈顶元素，**直到不再相同或 s 为空**；
- 当结束循环时，如果 s 不为空，则返回 False，反之 True；

<details><summary><b>Python</b></summary>

```python
class Solution:
    def validateStackSequences(self, pushed: List[int], popped: List[int]) -> bool:

        s = []  # 模拟栈

        # pop(0) 的操作很浪费时间，其实是不需要修改 pushed 和 popped 的，详见优化后的代码
        while pushed:
            s.append(pushed.pop(0))

            while s and s[-1] == popped[0]:
                s.pop()
                popped.pop(0)
        
        return True if not popped else False
```

</details>

<details><summary><b>Python：优化后</b></summary>

```python
class Solution:
    def validateStackSequences(self, pushed: List[int], popped: List[int]) -> bool:

        s = []  # 模拟栈

        idx = 0  # popped 索引
        for x in pushed:
            s.append(x)

            while s and s[-1] == popped[idx]:
                s.pop()
                idx += 1
        
        return True if not s else False
```

</details>

