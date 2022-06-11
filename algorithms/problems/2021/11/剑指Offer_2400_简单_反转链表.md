## 剑指Offer_2400_反转链表（简单, 2021-11）
<!--{
    "tags": ["链表", "递归", "迭代", "经典"],
    "来源": "剑指Offer",
    "编号": "2400",
    "难度": "简单",
    "标题": "反转链表"
}-->

<summary><b>问题简述</b></summary>

```txt
输入一个链表的头节点，反转该链表。
```

<details><summary><b>详细描述</b></summary>

```txt
定义一个函数，输入一个链表的头节点，反转该链表并输出反转后链表的头节点。

示例:
    输入: 1->2->3->4->5->NULL
    输出: 5->4->3->2->1->NULL

限制：
    0 <= 节点个数 <= 5000

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/fan-zhuan-lian-biao-lcof
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```

</details>

<!-- <div align="center"><img src="../../../_assets/xxx.png" height="300" /></div> -->

<summary><b>思路</b></summary>


<details><summary><b>Python：递归（写法1）</b></summary>

```python
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution:

    def reverseList(self, head: ListNode) -> ListNode:
        if not head:  # 单独处理空链表
            return head
        
        self.ret = None

        def dfs(cur):
            # nonlocal ret  # 如果不使用 self.ret，而是 ret，就需要加上这句
            
            if cur.next is None:
                if self.ret is None:
                    self.ret = cur  # 尾节点，即新链表的头节点
                return cur
            
            nxt = dfs(cur.next)
            nxt.next = cur
            return cur
        
        
        head = dfs(head)
        head.next = None  # 断开最后一个节点，容易忽略的一步
        return self.ret
```

</details>


<details><summary><b>Python：递归（写法2）</b></summary>

```python
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution:

    def reverseList(self, head: ListNode) -> ListNode:

        def dfs(cur, pre):  # 当前节点，上一个节点
            if cur is None:  # 达到尾结点
                return pre  # 返回尾结点的上一个节点
            
            ret = dfs(cur.next, cur)
            cur.next = pre  # 把当前节点的 next 指向上一个节点
            return ret
        
        return dfs(head, None)
```

</details>


<details><summary><b>Python：迭代</b></summary>

```python
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution:
    def reverseList(self, head: ListNode) -> ListNode:
        cur, pre = head, None
        while cur:
            # 注意顺序
            nxt = cur.next # 暂存后继节点 cur.next
            cur.next = pre # 修改 next 引用指向
            pre = cur      # pre 暂存 cur
            cur = nxt      # cur 访问下一节点
        return pre
```

</details>