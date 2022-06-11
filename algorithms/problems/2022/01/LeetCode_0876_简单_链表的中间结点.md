## LeetCode_0876_链表的中间结点（简单, 2022-01）
<!--{
    "tags": ["链表", "快慢指针"],
    "来源": "LeetCode",
    "难度": "简单",
    "编号": "0876",
    "标题": "链表的中间结点"
}-->

<summary><b>问题简述</b></summary>

```txt
给定非空链表，返回链表的中间结点。如果有两个中间结点，则返回第二个中间结点。
```

<details><summary><b>详细描述</b></summary>

```txt
给定一个头结点为 head 的非空单链表，返回链表的中间结点。

如果有两个中间结点，则返回第二个中间结点。

示例 1：
    输入：[1,2,3,4,5]
    输出：此列表中的结点 3 (序列化形式：[3,4,5])
    返回的结点值为 3 。 (测评系统对该结点序列化表述是 [3,4,5])。
    注意，我们返回了一个 ListNode 类型的对象 ans，这样：
    ans.val = 3, ans.next.val = 4, ans.next.next.val = 5, 以及 ans.next.next.next = NULL.
示例 2：
    输入：[1,2,3,4,5,6]
    输出：此列表中的结点 4 (序列化形式：[4,5,6])
    由于该列表有两个中间结点，值分别为 3 和 4，我们返回第二个结点。

提示：
    给定链表的结点数介于 1 和 100 之间。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/middle-of-the-linked-list
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```

</details>

<!-- <div align="center"><img src="../../../_assets/xxx.png" height="300" /></div> -->

<summary><b>思路：快慢指针</b></summary>

<details><summary><b>Python</b></summary>

```python
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def middleNode(self, head: ListNode) -> ListNode:

        lp, fp = head, head
        while fp and fp.next:
            fp = fp.next.next
            lp = lp.next
        
        return lp
```

</details>

