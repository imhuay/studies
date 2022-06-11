## 剑指Offer_5901_滑动窗口的最大值（困难, 2022-01）
<!--{
    "tags": ["滑动窗口", "单调队列"],
    "来源": "剑指Offer",
    "编号": "5901",
    "难度": "困难",
    "标题": "滑动窗口的最大值"
}-->

<summary><b>问题简述</b></summary>

```txt
给定一个数组 nums 和滑动窗口的大小 k，请找出所有滑动窗口里的最大值。
```

<details><summary><b>详细描述</b></summary>

```txt
给定一个数组 nums 和滑动窗口的大小 k，请找出所有滑动窗口里的最大值。

示例:
    输入: nums = [1,3,-1,-3,5,3,6,7], 和 k = 3
    输出: [3,3,5,5,6,7] 
    解释: 
      滑动窗口的位置                最大值
    ---------------               -----
    [1  3  -1] -3  5  3  6  7       3
     1 [3  -1  -3] 5  3  6  7       3
     1  3 [-1  -3  5] 3  6  7       5
     1  3  -1 [-3  5  3] 6  7       5
     1  3  -1  -3 [5  3  6] 7       6
     1  3  -1  -3  5 [3  6  7]      7

提示：
    你可以假设 k 总是有效的，在输入数组不为空的情况下，1 ≤ k ≤ 输入数组的大小。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/hua-dong-chuang-kou-de-zui-da-zhi-lcof
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```

</details>

<!-- <div align="center"><img src="../../../_assets/xxx.png" height="300" /></div> -->

<summary><b>思路</b></summary>

- 使用单调队列维护一个最大值序列，每次滑动窗口前，更新单调队列，使队首元素为下一个窗口中的最大值，详见参考链接或具体代码；
    > [滑动窗口的最大值（单调队列，清晰图解）](https://leetcode-cn.com/problems/hua-dong-chuang-kou-de-zui-da-zhi-lcof/solution/mian-shi-ti-59-i-hua-dong-chuang-kou-de-zui-da-1-6/)

<details><summary><b>Python</b></summary>

- 跟[官方写法](https://leetcode-cn.com/problems/hua-dong-chuang-kou-de-zui-da-zhi-lcof/solution/hua-dong-chuang-kou-de-zui-da-zhi-by-lee-ymyo/)的区别：
    - 官方的单调队列维护的是数组下标，通过判断下标位置来确定是否移除队首元素；因此可以使用**严格单调队列**；而下面的写法中使用值来判断是否移除队首，因此使用的是非严格单调队列（相关代码段：`if q[0] == nums[i - k]: q.popleft()`）

```python
class Solution:
    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
        from collections import deque

        if not nums: return []

        # 初始化单调队列，对任意 i > j，有 q[i] >= q[j]
        q = deque()
        for x in nums[:k]:
            while q and q[-1] < x:  # 注意这里是非严格单调的
                q.pop()
            q.append(x)
        # print(q)

        ret = [q[0]]  # 
        for i in range(k, len(nums)):
            if q[0] == nums[i - k]:  # 因为是通过值判断，所以需要保留所有相同的最大值，所以队列是非严格单调的
                q.popleft()
            while q and q[-1] < nums[i]:
                q.pop()
            q.append(nums[i])
            ret.append(q[0])
            # print(q)
        
        return ret
```

</details>

