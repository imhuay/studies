## LeetCode_0025_K个一组翻转链表（困难, 2022-02）
<!--{
    "tags": ["链表"],
    "来源": "LeetCode",
    "难度": "困难",
    "编号": "0025",
    "标题": "K个一组翻转链表",
    "公司": []
}-->

<summary><b>问题简述</b></summary>

```txt
给你一个链表，每 k 个节点一组进行翻转，请你返回翻转后的链表。
k 是一个正整数，它的值小于或等于链表的长度。
如果节点总数不是 k 的整数倍，那么请将最后剩余的节点保持原有顺序。

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

- 每次用 l, r 两个指针框定需要翻转的范围，完成翻转后继续下一组，直到最后一组不足 k 个节点结束；
- 注意节点的拼接；

<details><summary><b>Python</b></summary>

```python
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def reverseKGroup(self, head: Optional[ListNode], k: int) -> Optional[ListNode]:
        
        # 翻转一个子链表
        def reverse(l, r):
            pre, cur = None, l
            while cur:
                nxt = cur.next
                cur.next = pre
                pre = cur
                cur = nxt

            return r, l  # 翻转后，头尾交换

        dummy = ListNode(0)  # 因为头结点可能会变，设置一个伪头结点
        dummy.next = head

        pre = dummy  # pre 定位在 l 的前面
        l = head
        while l:
            r = pre  # r 初始化为上一个节点，这样走 k 步后正好划定一个 [l, r] 的闭区间
            for _ in range(k):
                r = r.next
                if not r:
                    return dummy.next
            
            nxt = r.next
            r.next = None  # 切断，这里是否切断要看具体的 reverse 是怎么实现的，这里的实现需要切断
            l, r = reverse(l, r)
            pre.next = l  # 重新接入链表
            r.next = nxt
            
            # [l, r] 翻转完成后，继续下一组 [l, r]
            pre = r  # pre 初始化为上一组的 r
            l = r.next  # l 初始化为上一组 r 的下一个节点
        
        return dummy.next
```

</details>

