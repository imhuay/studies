## LeetCode_0002_两数相加（中等, 2021-10）
<!--{
    "tags": ["链表"],
    "来源": "LeetCode",
    "编号": "0002",
    "难度": "中等",
    "标题": "两数相加"
}-->

<summary><b>问题简述</b></summary>

```txt
给你两个 非空 的链表，表示两个非负的整数。它们每位数字都是按照 逆序 的方式存储的，并且每个节点只能存储 一位 数字。

请你将两个数相加，并以相同形式返回一个表示和的链表。
```

<details><summary><b>详细描述</b></summary>

```txt
给你两个 非空 的链表，表示两个非负的整数。它们每位数字都是按照 逆序 的方式存储的，并且每个节点只能存储 一位 数字。

请你将两个数相加，并以相同形式返回一个表示和的链表。

你可以假设除了数字 0 之外，这两个数都不会以 0 开头。

示例1：
    输入：l1 = [2,4,3], l2 = [5,6,4]
    输出：[7,0,8]
    解释：342 + 465 = 807.

示例2：
    输入：l1 = [9,9,9,9,9,9,9], l2 = [9,9,9,9]
    输出：[8,9,9,9,0,0,0,1]

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/add-two-numbers
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```

</details>


<summary><b>思路</b></summary>

<details><summary><b>Python</b></summary>

```python
# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):  # noqa
        self.val = val
        self.next = next


class Solution:

    def addTwoNumbers(self, l1: ListNode, l2: ListNode) -> ListNode:  # noqa
        ret = p = ListNode()

        s = 0
        # 注意遍历条件，当三个都不为真时才会结束
        while l1 or l2 or s != 0:  # s != 0 表示最后一次相加存在进位的情况
            s += (l1.val if l1 else 0) + (l2.val if l2 else 0)

            p.next = ListNode(s % 10)  # 个位
            p = p.next

            # 遍历链表
            if l1:
                l1 = l1.next
            if l2:
                l2 = l2.next

            s = s // 10  # 进位

        return ret.next
```

</details>
