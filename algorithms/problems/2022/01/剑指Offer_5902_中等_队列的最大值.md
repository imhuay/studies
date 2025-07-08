## 队列的最大值
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2022-10-14%2014%3A59%3A33&color=yellowgreen&style=flat-square)
[![](https://img.shields.io/static/v1?label=&message=%E4%B8%AD%E7%AD%89&color=yellow&style=flat-square)](../../../README.md#中等)
[![](https://img.shields.io/static/v1?label=&message=%E5%89%91%E6%8C%87Offer&color=green&style=flat-square)](../../../README.md#剑指offer)
[![](https://img.shields.io/static/v1?label=&message=%E6%A0%88/%E9%98%9F%E5%88%97&color=blue&style=flat-square)](../../../README.md#栈队列)
[![](https://img.shields.io/static/v1?label=&message=%E8%AE%BE%E8%AE%A1&color=blue&style=flat-square)](../../../README.md#设计)

<!--END_SECTION:badge-->
<!--info
tags: [队列, 设计]
source: 剑指Offer
level: 中等
number: '5902'
name: 队列的最大值
companies: []
-->

<summary><b>问题简述</b></summary>

```txt
设计一个队列并实现函数 max_value 得到队列里的最大值，要求函数max_value、push_back 和 pop_front 的均摊时间复杂度都是O(1)。
若队列为空，pop_front 和 max_value 返回 -1
```

<details><summary><b>详细描述</b></summary>

```txt
请定义一个队列并实现函数 max_value 得到队列里的最大值，要求函数max_value、push_back 和 pop_front 的均摊时间复杂度都是O(1)。

若队列为空，pop_front 和 max_value 需要返回 -1

示例 1：
    输入: 
    ["MaxQueue","push_back","push_back","max_value","pop_front","max_value"]
    [[],[1],[2],[],[],[]]
    输出: [null,null,null,2,1,2]
示例 2：
    输入: 
    ["MaxQueue","pop_front","max_value"]
    [[],[],[]]
    输出: [null,-1,-1]

限制：
    1 <= push_back,pop_front,max_value的总操作数 <= 10000
    1 <= value <= 10^5

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/dui-lie-de-zui-da-zhi-lcof
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```

</details>

<!-- <div align="center"><img src="../../../_assets/xxx.png" height="300" /></div> -->

<summary><b>思路</b></summary>

- 使用单调队列维护一个最大值序列，每次入队或出队时维护，详见代码；

<details><summary><b>Python</b></summary>

```python
class MaxQueue:

    def __init__(self):
        from collections import deque
        self.q = deque()  # 正常保存队列元素
        self.d = deque()  # 单调队列

    def max_value(self) -> int:
        if not self.d: return -1
        return self.d[0]


    def push_back(self, value: int) -> None:
        self.q.append(value)
        
        # 维护单调队列
        while self.d and self.d[-1] < value:  # 这里使用小于而不是小于等于，是因为后面出队是通过值判断，所以不能使用严格单调
            self.d.pop()
        self.d.append(value)


    def pop_front(self) -> int:
        if not self.q: return -1

        v = self.q.popleft()
        if v == self.d[0]:  # 如果出队元素等于当前最大元素，则同时对 d 执行出队
            self.d.popleft()
        return v


# Your MaxQueue object will be instantiated and called as such:
# obj = MaxQueue()
# param_1 = obj.max_value()
# obj.push_back(value)
# param_3 = obj.pop_front()
```

</details>

