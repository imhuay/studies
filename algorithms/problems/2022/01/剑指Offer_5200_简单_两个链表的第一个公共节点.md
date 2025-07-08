## 两个链表的第一个公共节点
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2022-10-15%2016%3A42%3A24&color=yellowgreen&style=flat-square)
[![](https://img.shields.io/static/v1?label=&message=%E7%AE%80%E5%8D%95&color=yellow&style=flat-square)](../../../README.md#简单)
[![](https://img.shields.io/static/v1?label=&message=%E5%89%91%E6%8C%87Offer&color=green&style=flat-square)](../../../README.md#剑指offer)
[![](https://img.shields.io/static/v1?label=&message=%E9%93%BE%E8%A1%A8&color=blue&style=flat-square)](../../../README.md#链表)
[![](https://img.shields.io/static/v1?label=&message=%E5%8F%8C%E6%8C%87%E9%92%88&color=blue&style=flat-square)](../../../README.md#双指针)

<!--END_SECTION:badge-->
<!--info
tags: [链表, 快慢指针]
source: 剑指Offer
level: 简单
number: '5200'
name: 两个链表的第一个公共节点
companies: []
-->

<summary><b>问题描述</b></summary>

```txt
输入两个链表，找出它们的第一个公共节点。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/liang-ge-lian-biao-de-di-yi-ge-gong-gong-jie-dian-lcof
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```

<!-- <div align="center"><img src="../../../_assets/xxx.png" height="300" /></div> -->

<summary><b>思路1</b></summary>

> [两个链表的第一个公共节点（差值法） - 宫水三叶](https://leetcode-cn.com/problems/liang-ge-lian-biao-de-di-yi-ge-gong-gong-jie-dian-lcof/solution/gong-shui-san-xie-zhao-liang-tiao-lian-b-ifqw/)

- 分别遍历两个链表，得到两个链表的长度，记为 `l1` 和 `l2`；
- 让较长的先走 `|l1 - l2|` 步，然后一起走，第一个相同节点即为公共节点；

<details><summary><b>Python</b></summary>

```python
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution:
    def getIntersectionNode(self, headA: ListNode, headB: ListNode) -> ListNode:

        def get_list_len(p):
            cnt = 0
            while p:
                p = p.next
                cnt += 1
            
            return cnt

        la = get_list_len(headA)
        lb = get_list_len(headB)

        if la > lb:
            p1, p2 = headA, headB
        else:
            p1, p2 = headB, headA

        c = abs(la - lb)
        while c:
            p1 = p1.next
            c -= 1

        while p1 != p2:
            p1 = p1.next
            p2 = p2.next

        return p1
```

</details>

<summary><b>思路2</b></summary>

> [两个链表的第一个公共节点 - Krahets](https://leetcode-cn.com/problems/liang-ge-lian-biao-de-di-yi-ge-gong-gong-jie-dian-lcof/solution/jian-zhi-offer-52-liang-ge-lian-biao-de-gcruu/)

- 本质上跟思路1 是类似的，但是更巧妙，写法也更简洁；
- 把 headA 和 headB 都分为两段，记 `headA = la + lc`，`headB = lb + lc`，其中 `lc` 为公共部分；
- 对指针 pa，当遍历完 headA 后紧接着遍历 headB；指针 pb 和 headB 同理，那么遍历过程如下：

    ```
    headA -> headB = la -> lc -> lb -> lc
    headB -> headA = lb -> lc -> la -> lc
    ```

- 因为 `la + lc + lb == lb + lc + la`，当 pa 和 pb 遍历完这三段时，接下去的第一个节点就是公共节点；
- 如果 lc 部分的长度为 0，那么公共节点就是 NULL；

<details><summary><b>Python</b></summary>

```python
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution:
    def getIntersectionNode(self, headA: ListNode, headB: ListNode) -> ListNode:
        
        pa, pb = headA, headB
        while pa != pb:
            # 如果两个链表没有公共节点，循环结束时，pa == pa == None
            pa = pa.next if pa else headB
            pb = pb.next if pb else headA
        
        return pa
```

</details>
