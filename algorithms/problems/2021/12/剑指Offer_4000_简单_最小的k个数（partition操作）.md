## 最小的k个数（partition操作）
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2022-10-14%2014%3A59%3A33&color=yellowgreen&style=flat-square)
[![](https://img.shields.io/static/v1?label=&message=%E7%AE%80%E5%8D%95&color=yellow&style=flat-square)](../../../README.md#简单)
[![](https://img.shields.io/static/v1?label=&message=%E5%89%91%E6%8C%87Offer&color=green&style=flat-square)](../../../README.md#剑指offer)
[![](https://img.shields.io/static/v1?label=&message=%E5%A0%86/%E4%BC%98%E5%85%88%E9%98%9F%E5%88%97&color=blue&style=flat-square)](../../../README.md#堆优先队列)
[![](https://img.shields.io/static/v1?label=&message=%E6%8E%92%E5%BA%8F&color=blue&style=flat-square)](../../../README.md#排序)
[![](https://img.shields.io/static/v1?label=&message=%E7%BB%8F%E5%85%B8&color=blue&style=flat-square)](../../../README.md#经典)

<!--END_SECTION:badge-->
<!--info
tags: [优先队列, 快排, 经典]
source: 剑指Offer
level: 简单
number: '4000'
name: 最小的k个数（partition操作）
companies: []
-->

<summary><b>问题简述</b></summary>

```txt
输入整数数组 arr ，找出其中最小的 k 个数
```
> [剑指 Offer 40. 最小的k个数 - 力扣（LeetCode）](https://leetcode-cn.com/problems/zui-xiao-de-kge-shu-lcof/)

<details><summary><b>详细描述</b></summary>

```txt
输入整数数组 arr ，找出其中最小的 k 个数。例如，输入4、5、1、6、2、7、3、8这8个数字，则最小的4个数字是1、2、3、4。

示例 1：
    输入：arr = [3,2,1], k = 2
    输出：[1,2] 或者 [2,1]
示例 2：
    输入：arr = [0,1,2,1], k = 1
    输出：[0]
 
限制：
    0 <= k <= arr.length <= 10000
    0 <= arr[i] <= 10000

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/zui-xiao-de-kge-shu-lcof
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```

</details>

<!-- <div align="center"><img src="../../../_assets/xxx.png" height="300" /></div> -->

<summary><b>思路1：快排中的 partition 过程</b></summary>

- 快排的过程：
    - **partition 过程**：以数组某个元素（一般取首元素）为基准数，将所有小于基准数的元素移动至其左边，大于基准数的元素移动至其右边。
    - 递归地对左右部分执行 **partition 过程**，直至区域内的元素数量为 1；
- 基于以上思想，当某次划分后基准数正好是第 k+1 小的数字，那么此时基准数左边的所有数字便是题目要求的最小的 k 个数。

<details><summary><b>Python</b></summary>

```python
class Solution:
    def getLeastNumbers(self, arr: List[int], k: int) -> List[int]:

        def partition(lo, hi):  # [lo, hi]
            if lo >= hi: return

            p = arr[lo]  # 选取第一个位置为基准点
            l, r = lo, hi  # l 的初始位置应该在 lo，而不是 lo + 1
            # 假设初始化为 lo + 1，当 a[lo] 为最小值时，此时训处循环后 l == r == lo + 1，再交换 a[lo] 和 a[l] 就会出错

            while l < r:  # 退出循环时 l == r
                # 先移动 r，在移动 l，此时退出循环后 l 和 r 同时指向一个小于 p 的值；反之，如果用 a[hi] 初始化 p，就要先移动 l，在移动 r；

                # 从 r 开始，从右往左找到第一个 < p 的值，所以循环条件是 >=
                while l < r and arr[r] >= p: r -= 1
                # 从 l 开始，从左往右找到第一个 > p 的值，所以循环条件是 <=
                while l < r and arr[l] <= p: l += 1
                arr[l], arr[r] = arr[r], arr[l]
                
            arr[lo], arr[l] = arr[l], arr[lo]  # 将基准点移动到分界点

            if l < k: partition(l + 1, hi)
            if l > k: partition(lo, l - 1)

        partition(0, len(arr) - 1)
        return arr[:k]
```

</details>


<summary><b>思路2：堆（优先队列）</b></summary>

- **写法1）** 维护一个长度为 k 的大顶堆（第一个数最大），当下一个元素小于堆顶值，就更新堆（弹出堆顶，插入新值）；
- **写法2）** 直接对整个数组构建一个小顶堆，然后循环弹出前 k 个值；
- 注意写法1 的时间复杂度是 `O(NlogK)`，而写法2 是 `O(NlogN)`；

<details><summary><b>Python：写法1（使用库函数）</b></summary>

```python
class Solution:
    def getLeastNumbers(self, arr: List[int], k: int) -> List[int]:
        if k < 1 or not arr:  # 使用堆，要添加非空断言
            return []

        import heapq

        # python 默认是小顶堆，且不支持自定义比较函数，所以要添加负号转成取前 k 大的数
        ret = [-x for x in arr[:k]]
        heapq.heapify(ret)

        for i in range(k, len(arr)):
            if -arr[i] > ret[0]:
                heapq.heappop(ret)
                heapq.heappush(ret, -arr[i])

        return [-x for x in ret]
```

</details>

<details><summary><b>Python：写法2（使用库函数）</b></summary>

```python
class Solution:
    def getLeastNumbers(self, arr: List[int], k: int) -> List[int]:
        if k < 1 or not arr:  # 使用堆，要添加非空断言
            return []

        import heapq

        # python 默认是小顶堆
        heapq.heapify(arr)

        ret = []
        for _ in range(k):
            ret.append(heapq.heappop(arr))

        return ret
```

</details>


<summary><b>思路3：计数排序</b></summary>

- 因为题目限制了 `arr[i]` 的范围，所以还可以使用计数排序，时间复杂度 `O(N)`；

<details><summary><b>Python</b></summary>

```python
class Solution:
    def getLeastNumbers(self, arr: List[int], k: int) -> List[int]:
        if k >= len(arr):  # 使用计数排序要加长度判断
            return arr

        dp = [0] * 10001

        for x in arr:
            dp[x] += 1
        
        ret = []
        cnt = 0
        for i in range(len(dp)):
            while dp[i] and cnt < k:
                ret.append(i)
                cnt += 1
                dp[i] -= 1
            if cnt == k:
                return ret
```

</details>