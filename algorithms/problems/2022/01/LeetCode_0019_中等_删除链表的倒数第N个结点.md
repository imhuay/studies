## LeetCode_0019_删除链表的倒数第N个结点（中等, 2022-01）
<!--{
    "tags": ["链表", "快慢指针"],
    "来源": "LeetCode",
    "难度": "中等",
    "编号": "0019",
    "标题": "删除链表的倒数第N个结点"
}-->

<summary><b>问题简述</b></summary>

```txt
给定链表，删除链表的倒数第 n 个结点，返回删除后链表的头结点。
```
> [19. 删除链表的倒数第 N 个结点 - 力扣（LeetCode）](https://leetcode-cn.com/problems/remove-nth-node-from-end-of-list/)

<details><summary><b>详细描述</b></summary>

```txt
给你一个链表，删除链表的倒数第 n 个结点，并且返回链表的头结点。

示例 1：
    输入：head = [1,2,3,4,5], n = 2
    输出：[1,2,3,5]
示例 2：
    输入：head = [1], n = 1
    输出：[]
示例 3：
    输入：head = [1,2], n = 1
    输出：[1]

提示：
    链表中结点的数目为 sz
    1 <= sz <= 30
    0 <= Node.val <= 100
    1 <= n <= sz

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/remove-nth-node-from-end-of-list
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```

</details>

<!-- <div align="center"><img src="../../../_assets/xxx.png" height="300" /></div> -->

<summary><b>思路</b></summary>

<details><summary><b>Python</b></summary>

```python
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next

class Solution:
    def removeNthFromEnd(self, head: ListNode, n: int) -> ListNode:

        dummy = ListNode(0)  # 伪头节点
        dummy.next = head

        k = n + 1  # 获取倒数第 n+1 个节点
        lp, fp = dummy, dummy
        while fp:
            if k <= 0:
                lp = lp.next
            
            fp = fp.next
            k -= 1
        
        # print(lp.val)
        lp.next = lp.next.next
        return dummy.next
```

</details>

