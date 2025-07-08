## 删除链表的节点
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2025-07-08%2016%3A53%3A13&color=yellowgreen&style=flat-square)
[![](https://img.shields.io/static/v1?label=&message=%E7%AE%80%E5%8D%95&color=yellow&style=flat-square)](../../../README.md#简单)
[![](https://img.shields.io/static/v1?label=&message=%E5%89%91%E6%8C%87Offer&color=green&style=flat-square)](../../../README.md#剑指offer)
[![](https://img.shields.io/static/v1?label=&message=%E9%93%BE%E8%A1%A8&color=blue&style=flat-square)](../../../README.md#链表)

<!--END_SECTION:badge-->
<!--info
tags: [链表]
source: 剑指Offer
level: 简单
number: '1800'
name: 删除链表的节点
companies: []
-->

<summary><b>问题简述</b></summary>

```txt
给定单向链表的头节点和要删除的节点的值（链表中的值都不相同），返回删除后链表的头节点。
```

<details><summary><b>详细描述</b></summary>

```txt
给定单向链表的头指针和一个要删除的节点的值，定义一个函数删除该节点。
返回删除后的链表的头节点。

注意：此题对比原题有改动

示例 1:
    输入: head = [4,5,1,9], val = 5
    输出: [4,1,9]
    解释: 给定你链表中值为 5 的第二个节点，那么在调用了你的函数之后，该链表应变为 4 -> 1 -> 9.
示例 2:
    输入: head = [4,5,1,9], val = 1
    输出: [4,5,9]
    解释: 给定你链表中值为 1 的第三个节点，那么在调用了你的函数之后，该链表应变为 4 -> 5 -> 9.

说明：
    题目保证链表中节点的值互不相同
    若使用 C 或 C++ 语言，你不需要 free 或 delete 被删除的节点

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/shan-chu-lian-biao-de-jie-dian-lcof
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```

</details>

<!-- <div align="center"><img src="../../../_assets/xxx.png" height="300" /></div> -->

<summary><b>思路</b></summary>

- 一般有两种写法：
    1. 单独处理头结点；
    2. 建立伪头结点，原头结点跟普通节点一样处理（推荐）

<details><summary><b>Python：写法1</b></summary>

```python
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution:
    def deleteNode(self, head: ListNode, val: int) -> ListNode:
        if head.val == val:  # 头结点单独处理
            return head.next

        cur = head  # 记录当前遍历的节点
        while cur:
            pre = cur  # 记录 cur 的前一个节点
            cur = cur.next
            if cur.val == val:  # 移除匹配的节点
                pre.next = cur.next
                break
        
        return head
```

</details>


<details><summary><b>Python：写法2</b></summary>

```python
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution:
    def deleteNode(self, head: ListNode, val: int) -> ListNode:
        dummy = ListNode(0)
        dummy.next = head

        pre = dummy  # 记录 cur 的前一个节点
        cur = dummy.next  # 记录当前遍历的节点
        while cur:
            if cur.val == val:  # 移除匹配的节点
                pre.next = cur.next
                break
            pre = cur  
            cur = cur.next
        
        return dummy.next
```

</details>

