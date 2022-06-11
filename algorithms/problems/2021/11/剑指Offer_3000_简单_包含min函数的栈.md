## 剑指Offer_3000_包含min函数的栈（简单, 2021-11）
<!--{
    "tags": ["栈", "数组", "设计"],
    "来源": "剑指Offer",
    "编号": "3000",
    "难度": "简单",
    "标题": "包含min函数的栈"
}-->

<summary><b>问题简述</b></summary>

```txt
实现栈的 pop 和 push 方法，同时实现一个 min 方法，返回栈中的最小值，min、push 及 pop 的时间复杂度都是 O(1)。
```

<details><summary><b>详细描述</b></summary>

```txt
定义栈的数据结构，请在该类型中实现一个能够得到栈的最小元素的 min 函数在该栈中，调用 min、push 及 pop 的时间复杂度都是 O(1)。

示例:
    MinStack minStack = new MinStack();
    minStack.push(-2);
    minStack.push(0);
    minStack.push(-3);
    minStack.min();     --> 返回 -3.
    minStack.pop();
    minStack.top();     --> 返回 0.
    minStack.min();     --> 返回 -2.

提示：
    - 各函数的调用总次数不超过 20000 次
    - pop、top 和 min 操作总是在 非空栈 上调用。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/bao-han-minhan-shu-de-zhan-lcof
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```

</details>

<!-- <div align="center"><img src="../../../_assets/xxx.png" height="300" /></div> -->

<summary><b>思路</b></summary>

- 使用两个 list: Buf 和 Min；其中 Buf 正常模拟栈，Min 也是一个栈，但是它只会将**小于等于栈顶**的元素入栈；
- 当 Buf 的出栈元素等于 Min 的栈顶元素时，Min 也出栈；
- Python 中 list 自带的 `append` 和 `pop` 方法默认行为就是栈的 `push` 和 `pop`，`top` 方法返回 `Buf[-1]` 即可；

<details><summary><b>Python</b></summary>

```python
class MinStack:

    def __init__(self):
        """
        initialize your data structure here.
        """
        self.Buf = []
        self.Min = []

    def push(self, x: int) -> None:
        self.Buf.append(x)
        if not self.Min or x <= self.Min[-1]:  # 注意这里是小于等于
            self.Min.append(x)

    def pop(self) -> None:
        x = self.Buf.pop()
        if x == self.Min[-1]:
            self.Min.pop()

    def top(self) -> int:
        return self.Buf[-1]

    def min(self) -> int:
        return self.Min[-1]


# Your MinStack object will be instantiated and called as such:
# obj = MinStack()
# obj.push(x)
# obj.pop()
# param_3 = obj.top()
# param_4 = obj.min()
```

</details>

