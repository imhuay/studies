## 重排链表
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2022-10-26%2012%3A48%3A18&color=yellowgreen&style=flat-square)
[![](https://img.shields.io/static/v1?label=&message=%E4%B8%AD%E7%AD%89&color=yellow&style=flat-square)](../../../README.md#中等)
[![](https://img.shields.io/static/v1?label=&message=LeetCode&color=green&style=flat-square)](../../../README.md#leetcode)
[![](https://img.shields.io/static/v1?label=&message=%E9%93%BE%E8%A1%A8&color=blue&style=flat-square)](../../../README.md#链表)
[![](https://img.shields.io/static/v1?label=&message=%E7%83%AD%E9%97%A8&color=blue&style=flat-square)](../../../README.md#热门)

<!--END_SECTION:badge-->
<!--info
tags: [链表, 热门]
source: LeetCode
level: 中等
number: '0143'
name: 重排链表
companies: [字节, 度小满, 拼多多]
-->

> [143. 重排链表 - 力扣（LeetCode）](https://leetcode.cn/problems/reorder-list/)

<summary><b>问题简述</b></summary>

```txt
给定一个单链表 L 的头节点 head ，单链表 L 表示为：
    L0 → L1 → … → Ln - 1 → Ln
请将其重新排列后变为：
    L0 → Ln → L1 → Ln-1 → L2 → Ln-2 → …
不能只是单纯的改变节点内部的值，而是需要实际的进行节点交换。
```

<!-- 
<details><summary><b>详细描述</b></summary>

```txt
```

</details>
-->

<!-- <div align="center"><img src="../../../_assets/xxx.png" height="300" /></div> -->

<summary><b>思路1</b></summary>

1. 找中间节点；
2. 将第二段链表反转；
3. 然后合并两段链表；
- 细节:
    - 因为需要截断, 所以实际上找的是中间节点的前一个节点(偶数情况下)

<details><summary><b>Python</b></summary>

```python
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def reorderList(self, head: Optional[ListNode]) -> None:
        """
        Do not return anything, modify head in-place instead.
        """

        def reverse(h):
            pre, cur = None, h
            while cur:
                nxt = cur.next
                cur.next = pre
                pre = cur
                cur = nxt
            return pre
        
        def get_mid(h):
            slow, fast = h, h.next  # 找中间节点的前一个节点
            while fast and fast.next:
                slow = slow.next
                fast = fast.next.next
            return slow
        
        mid = get_mid(head)
        tmp = mid.next
        mid.next = None  # 截断
        mid = reverse(tmp)

        l, r = head, mid
        while r:  # len(l) >= len(r)
            l_nxt, r_nxt = l.next, r.next
            l.next, r.next = r, l_nxt  # 关键步骤: 将 r 接入 l
            l, r = l_nxt, r_nxt
```

</details>


<summary><b>思路2</b></summary>

1. 把节点存入列表;
2. 通过索引拼接节点;
- 细节:
    - 把节点存入数组后, 可以使用下标访问节点, 形如 `arr[i].next = ...`
    - 拼接节点时注意边界位置的操作;
    - 尾节点的截断;

<details><summary><b>Python</b></summary>

```python
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def reorderList(self, head: Optional[ListNode]) -> None:
        """
        Do not return anything, modify head in-place instead.
        """
        tmp = []
        cur = head
        while cur:
            tmp.append(cur)
            cur = cur.next
        
        l, r = 0, len(tmp) - 1
        while l < r:  # 退出循环时 l == r
            tmp[l].next = tmp[r]
            l += 1
            if l == r: break  # 易错点
            tmp[r].next = tmp[l]
            r -= 1

        # 退出循环时 l 刚好指在中间节点(奇数时), 或中间位置的下一个节点(偶数时)
        tmp[l].next = None  # 易错点
```

</details>