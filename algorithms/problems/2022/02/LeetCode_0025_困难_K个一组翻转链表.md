## K个一组翻转链表
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2022-10-29%2023%3A59%3A13&color=yellowgreen&style=flat-square)
[![](https://img.shields.io/static/v1?label=&message=%E5%9B%B0%E9%9A%BE&color=yellow&style=flat-square)](../../../README.md#困难)
[![](https://img.shields.io/static/v1?label=&message=LeetCode&color=green&style=flat-square)](../../../README.md#leetcode)
[![](https://img.shields.io/static/v1?label=&message=%E9%93%BE%E8%A1%A8&color=blue&style=flat-square)](../../../README.md#链表)
[![](https://img.shields.io/static/v1?label=&message=LeetCode%20Hot%20100&color=blue&style=flat-square)](../../../README.md#leetcode-hot-100)
[![](https://img.shields.io/static/v1?label=&message=%E7%83%AD%E9%97%A8&color=blue&style=flat-square)](../../../README.md#热门)

<!--END_SECTION:badge-->
<!--info
tags: [链表, lc100, 热门]
source: LeetCode
level: 困难
number: '0025'
name: K个一组翻转链表
companies: []
-->

<summary><b>问题简述</b></summary>

```txt
给你链表的头节点 head ，每 k 个节点一组进行翻转，请你返回修改后的链表。
k 是一个正整数，它的值小于或等于链表的长度。如果节点总数不是 k 的整数倍，那么请将最后剩余的节点保持原有顺序。

进阶：
    你可以设计一个只使用常数额外空间的算法来解决此问题吗？
    你不能只是单纯的改变节点内部的值，而是需要实际进行节点交换。
```
> [25. K 个一组翻转链表 - 力扣（LeetCode）](https://leetcode-cn.com/problems/reverse-nodes-in-k-group/)

<!-- 
<details><summary><b>详细描述</b></summary>

```txt
```

</details>
-->


<!-- <div align="center"><img src="../../../_assets/xxx.png" height="300" /></div> -->

<summary><b>思路</b></summary>

- 关键是确定 4 个位置, 即待反转子链表的头节点 `sub_head`, 及其前一个节点 `pre`, 尾节点 `sub_tail`, 及其下一个节点 `nxt`;
- 细节:
  - 设置伪头节点, 遍历时先找到 `pre`, 在确定 `h`, `t`, `nxt`;
  - 不足 k 个长度时提前退出;
  - 反转子链表时提前断开 ``

<details><summary><b>Python</b></summary>

```python
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next

class Solution:

    def reverse(self, head):
        pre, cur = None, head
        while cur:
            nxt = cur.next
            cur.next = pre
            pre = cur
            cur = nxt
        return pre, head

    def reverseKGroup(self, head: Optional[ListNode], k: int) -> Optional[ListNode]:

        dummy = cur = ListNode(next=head)  # 设置伪头节点
        while cur:
            pre = cur  # 子链表头节点的前一个节点
            for _ in range(k):
                if not cur.next:
                    return dummy.next
                cur = cur.next
            sub_head = cur.next  # 子链表尾节点的下一个节点
            cur.next = None  # 断开子链表
            pre.next, sub_tail = self.reverse(pre.next)  # 反转子链表, 返回反转后的头尾节点
            sub_tail.next = sub_head
            cur = sub_tail

        return dummy.next
```

</details>
