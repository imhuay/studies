## 复杂链表的复制（深拷贝）
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2022-10-14%2014%3A59%3A33&color=yellowgreen&style=flat-square)
[![](https://img.shields.io/static/v1?label=&message=%E4%B8%AD%E7%AD%89&color=yellow&style=flat-square)](../../../README.md#中等)
[![](https://img.shields.io/static/v1?label=&message=%E5%89%91%E6%8C%87Offer&color=green&style=flat-square)](../../../README.md#剑指offer)
[![](https://img.shields.io/static/v1?label=&message=%E9%93%BE%E8%A1%A8&color=blue&style=flat-square)](../../../README.md#链表)
[![](https://img.shields.io/static/v1?label=&message=%E5%93%88%E5%B8%8C%E8%A1%A8%28Hash%29&color=blue&style=flat-square)](../../../README.md#哈希表hash)
[![](https://img.shields.io/static/v1?label=&message=%E7%BB%8F%E5%85%B8&color=blue&style=flat-square)](../../../README.md#经典)

<!--END_SECTION:badge-->
<!--info
tags: [链表, 哈希表, 经典]
source: 剑指Offer
level: 中等
number: '3500'
name: 复杂链表的复制（深拷贝）
companies: []
-->

<summary><b>问题简述</b></summary>

```txt
复制带随机指针的链表，返回复制后链表的头结点；
```

<details><summary><b>详细描述</b></summary>

**注意**：本题的输入输出带有迷惑性，它们并不是实际的输入和输出，而是链表的数组展现；

```txt
给你一个长度为 n 的链表，每个节点包含一个额外增加的随机指针 random ，该指针可以指向链表中的任何节点或空节点。

构造这个链表的 深拷贝。深拷贝应该正好由 n 个 全新 节点组成，其中每个新节点的值都设为其对应的原节点的值。新节点的 next 指针和 random 指针也都应指向复制链表中的新节点，并使原链表和复制链表中的这些指针能够表示相同的链表状态。复制链表中的指针都不应指向原链表中的节点 。

例如，如果原链表中有 X 和 Y 两个节点，其中 X.random --> Y 。那么在复制链表中对应的两个节点 x 和 y ，同样有 x.random --> y 。

返回复制链表的头节点。

用一个由 n 个节点组成的链表来表示输入/输出中的链表。每个节点用一个 [val, random_index] 表示：

val：一个表示 Node.val 的整数。
random_index：随机指针指向的节点索引（范围从 0 到 n-1）；如果不指向任何节点，则为  null 。
你的代码 只 接受原链表的头节点 head 作为传入参数。

示例 1：
    输入：head = [[7,null],[13,0],[11,4],[10,2],[1,0]]
    输出：[[7,null],[13,0],[11,4],[10,2],[1,0]]
示例 2：
    输入：head = [[1,1],[2,1]]
    输出：[[1,1],[2,1]]
示例 3：
    输入：head = [[3,null],[3,0],[3,null]]
    输出：[[3,null],[3,0],[3,null]]
示例 4：
    输入：head = []
    输出：[]
    解释：给定的链表为空（空指针），因此返回 null。

提示：
    -10000 <= Node.val <= 10000
    Node.random 为空（null）或指向链表中的节点。
    节点数目不超过 1000 。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/fu-za-lian-biao-de-fu-zhi-lcof
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```

</details>

<!-- <div align="center"><img src="../../../_assets/xxx.png" height="300" /></div> -->

<summary><b>思路1：哈希表</b></summary>

- 先看下普通链表的复制：

    <details><summary><b>普通链表的复制</b></summary>

    ```python
        class Solution:
            def copyList(self, head: 'Node') -> 'Node':
                cur = head
                ret = pre = Node(0)  # 伪头结点
                while cur:
                    node = Node(cur.val) # 复制节点 cur
                    pre.next = node      # 新链表的 前驱节点 -> 当前节点
                    # pre.random = '???' # 新链表的 「 前驱节点 -> 当前节点 」 无法确定
                    cur = cur.next       # 遍历下一节点
                    pre = node           # 保存当前新节点
                return ret.next
    ```

    </details>

- 首先要理解本题的难点：
    - 复制当前节点的时候，随机指针指向的节点可能还没有创建；
    - 即使你先按普通链表先把节点都创建出来，由于链表无法随机访问的性质，你也不知道随机节点在哪个位置；
- 解决方法是利用哈希表（写法1）：
    - 第一次遍历时，记录每个节点对应的复制节点；
    - 第二次遍历时，根据原链表的指向从哈希表中提取对应的节点，建立指向关系；
- 本题还有一种递归的写法（写法2）：
    - 同样用一个哈希表保存

<details><summary><b>Python：迭代（写法1）</b></summary>

```python
"""
# Definition for a Node.
class Node:
    def __init__(self, x: int, next: 'Node' = None, random: 'Node' = None):
        self.val = int(x)
        self.next = next
        self.random = random
"""

class Solution:
    def copyRandomList(self, head: 'Node') -> 'Node':
        if not head: return None  # 使用伪头结点，可以省去这行

        dp = dict()

        # 第一次遍历，生成复制节点，并记录到哈希表
        p = head
        while p:
            dp[p] = Node(p.val)
            p = p.next
        
        # 写法1：使用伪头结点，可以省去对 head 为 None 的判断
        cur = head
        ret = pre = Node(0)  # 伪头结点
        while cur:
            pre.next = dp[cur]  # 这里可以不用 get，因为一定存在
            pre.next.random = dp.get(cur.random)  # get 方法在 key 不存在时，默认返回 None
            cur = cur.next
            pre = pre.next

        return ret.next

        # 写法2：相比使用伪头结点
        # cur = head
        # while cur:
        #     dp[cur].next = dp.get(cur.next)
        #     dp[cur].random = dp.get(cur.random)
        #     cur = cur.next
        
        # return dp[head]
```

</details>


<details><summary><b>Python：递归（写法2）</b></summary>

- 【不推荐】虽然代码量会少一点，但是不好理解；

```python
"""
# Definition for a Node.
class Node:
    def __init__(self, x: int, next: 'Node' = None, random: 'Node' = None):
        self.val = int(x)
        self.next = next
        self.random = random
"""

class Solution:
    def copyRandomList(self, head: 'Node') -> 'Node':
        if not head: return None

        dp = dict()
        
        def dfs(p):
            if not p: return None

            if p not in dp:
                dp[p] = Node(p.val)
                dp[p].next = dfs(p.next)
                dp[p].random = dfs(p.random)
        
            return dp[p]
        
        return dfs(head)
```

</details>


<summary><b>思路2：复制+拆分</b></summary>

<div align="center"><img src="../../../_assets/剑指Offer_0035_中等_复杂链表的复制.png" height="300" /></div>

> 详见：[复杂链表的复制（哈希表 / 拼接与拆分，清晰图解）](https://leetcode-cn.com/problems/fu-za-lian-biao-de-fu-zhi-lcof/solution/jian-zhi-offer-35-fu-za-lian-biao-de-fu-zhi-ha-xi-/)

- 注意这个方法需要遍历三次：
    - 第一次复制节点
    - 第二次设置随机节点
    - 第三次拆分
- 因为随机节点指向任意，所以必须先设置完所有随机节点后才能拆分；

<details><summary><b>Python</b></summary>

```python
"""
# Definition for a Node.
class Node:
    def __init__(self, x: int, next: 'Node' = None, random: 'Node' = None):
        self.val = int(x)
        self.next = next
        self.random = random
"""

"""
# Definition for a Node.
class Node:
    def __init__(self, x: int, next: 'Node' = None, random: 'Node' = None):
        self.val = int(x)
        self.next = next
        self.random = random
"""

class Solution:
    def copyRandomList(self, head: 'Node') -> 'Node':
        if not head: return None

        # 复制节点
        cur = head
        while cur:
            nod = Node(cur.val)  # 创建节点
            cur.next, nod.next = nod, cur.next  # 接入新节点
            cur = nod.next  # 遍历下一个节点

        # 设置随机节点，因为随机节点指向任意，所以必须先设置随机节点后才能断开
        cur = head
        while cur:
            if cur.random:
                cur.next.random = cur.random.next
            cur = cur.next.next

        # 拆分节点
        cur = head
        ret = nxt = head.next
        while nxt.next:
            # 开始拆分
            cur.next = cur.next.next
            nxt.next = nxt.next.next

            # 下一组
            cur = cur.next
            nxt = nxt.next
        
        return ret
```

</details>
