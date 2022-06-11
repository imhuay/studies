## LeetCode_0021_合并两个有序链表（简单, 2021-10）
<!--{
    "tags": ["递归"],
    "来源": "LeetCode",
    "编号": "0021",
    "难度": "简单",
    "标题": "合并两个有序链表"
}-->

<summary><b>问题描述</b></summary>

```txt
将两个升序链表合并为一个新的 升序 链表并返回。新链表是通过拼接给定的两个链表的所有节点组成的。 

示例 1：
    输入：l1 = [1,2,4], l2 = [1,3,4]
    输出：[1,1,2,3,4,4]
示例 2：
    输入：l1 = [], l2 = []
    输出：[]
示例 3：
    输入：l1 = [], l2 = [0]
    输出：[0]

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/merge-two-sorted-lists
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```

<summary><b>思路</b></summary>

<details><summary><b>Python：递归</b></summary>

```python
# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):  # noqa
        self.val = val
        self.next = next


class Solution:
    def mergeTwoLists(self, l1: ListNode, l2: ListNode) -> ListNode:  # noqa
        """ 递归 """
        if l1 is None:  # 尾递归 1
            return l2
        elif l2 is None:  # 尾递归 2
            return l1
        elif l1.val < l2.val:  # 选出头结点较小的一个，余下部分递归
            l1.next = self.mergeTwoLists(l1.next, l2)
            return l1
        else:
            l2.next = self.mergeTwoLists(l1, l2.next)
            return l2


```

</details>


<details><summary><b>Python：迭代</b></summary>

```python
# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):  # noqa
        self.val = val
        self.next = next


class Solution:
    def mergeTwoLists(self, l1: ListNode, l2: ListNode) -> ListNode:  # noqa
        """ 迭代 """
        head = ListNode(-1)  # 初始化

        pre = head
        while l1 and l2:
            if l1.val < l2.val:
                pre.next = l1
                l1 = l1.next
            else:
                pre.next = l2
                l2 = l2.next
            pre = pre.next

        # 合并后 l1 和 l2 最多只有一个还未被合并完，我们直接将链表末尾指向未合并完的链表即可
        pre.next = l1 if l1 is not None else l2

        return head.next

```

</details>