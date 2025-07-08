## 寻找两个正序数组的中位数
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2022-10-14%2014%3A59%3A33&color=yellowgreen&style=flat-square)
[![](https://img.shields.io/static/v1?label=&message=%E5%9B%B0%E9%9A%BE&color=yellow&style=flat-square)](../../../README.md#困难)
[![](https://img.shields.io/static/v1?label=&message=LeetCode&color=green&style=flat-square)](../../../README.md#leetcode)
[![](https://img.shields.io/static/v1?label=&message=%E4%BA%8C%E5%88%86%E6%9F%A5%E6%89%BE&color=blue&style=flat-square)](../../../README.md#二分查找)
[![](https://img.shields.io/static/v1?label=&message=LeetCode%20Hot%20100&color=blue&style=flat-square)](../../../README.md#leetcode-hot-100)

<!--END_SECTION:badge-->
<!--info
tags: [二分, lc100]
source: LeetCode
level: 困难
number: '0004'
name: 寻找两个正序数组的中位数
companies: []
-->

<summary><b>问题简述</b></summary>

```txt
给定两个大小分别为 m 和 n 的正序（从小到大）数组 A 和 B。请你找出并返回这两个正序数组的 中位数 。

算法的时间复杂度应该为 O(log (m+n)) 。
```
> [4. 寻找两个正序数组的中位数 - 力扣（LeetCode）](https://leetcode-cn.com/problems/median-of-two-sorted-arrays/)

<!-- 
<details><summary><b>详细描述</b></summary>

```txt
```

</details>
-->


<!-- <div align="center"><img src="../../../_assets/xxx.png" height="300" /></div> -->

<summary><b>思路</b></summary>

- 二分目标：找到最大的 `i`，使 `A[i - 1] <= B[j]`，其中 `j = (m + n + 1) / 2 - i`，`m, n` 分别为 `A, B` 的长度；
- 思路简述：将 `A, B` 分别分成如下两组，且保证 `max(A_i-1, B_j-1) <= min(A_i, B_j)`，根据中位数的性质，目标值即 `max(A_i-1, B_j-1)`；
    - 可证，该条件等价于找到最大的 `i`，使 `A[i - 1] <= B[j]`（证明详见参考链接）
    > [寻找两个有序数组的中位数 - 力扣官方题解](https://leetcode-cn.com/problems/median-of-two-sorted-arrays/solution/xun-zhao-liang-ge-you-xu-shu-zu-de-zhong-wei-s-114/)

    ```
        A_0, .., A_i-1 | A_i, .., A_m-1
        B_0, .., B_j-1 | B_j, .., B_n-1
    其中
        i + j == (m + n + 1) / 2
    这里使用 (m + n + 1) / 2 而不是 (m + n) / 2，
        是为了使当 m + n 为奇数时，前一半比后一半多一个，即 i + j == (m + n) - (i + j) + 1；
        偶数时不影响；
    ```

- 关于 `i == 0/m, j == 0/n` 的处理细节见代码；

<details><summary><b>Python</b></summary>

```python
class Solution:
    def findMedianSortedArrays(self, A: List[int], B: List[int]) -> float:
        if len(A) > len(B):
            return self.findMedianSortedArrays(B, A)

        inf = 1e7
        m, n = len(A), len(B)
        # half 表示一半的数量；+1 是为了使奇数情况时，左侧数量多一个，偶数不影响；
        half = (m + n + 1) // 2
        l, r = 0, m  # [l, r) 左闭右开区间，循环时要始终保持这个开闭原则

        while l < r:  # 因为是左闭右开区间，所以 l 要始终小于 r
            # 这里 i 和 j 指的是数量，而不是下标，即 A 中的前 i 个数，B 中的前 j 个数；
            # i + j 共同组成了“前一半”的数
            i = (l + r + 1) // 2
            j = half - i
            # 因为 i 和 j 都是指的数量，所以下标要 -1；具体来说，i 和 j 分别把 A 和 B 划分成了如下两个区间
            # 前一半包括 A[0 .. i-1] 和 B[0 .. j-1]
            # 后一半包括 A[i .. m-1] 和 B[j .. n-1]

            # 二分的目标是找到最大的 i 使 A[i - 1] <= B[j] 成立
            if A[i - 1] <= B[j]:
                l = i  # [l, i-1] 区间满足要求，下一轮在 [i, r) 中继续找更大的，所以使 l = i
            else:
                r = i - 1  # [i-1, r) 区间不满足要求，下一轮从 [l, i-1) 继续找符合的，所以令 r = i - 1

        # 退出循环时 l == r
        i, j = l, half - l

        # 记 m1, m2 分别表示前半部分的最大值和后半部分的最小值，根据定义
        #   m1, m2 = max(A[i-1],B[j-1]), min(A[i],B[j])
        # 这里要注意 i=0/i=m/j=0/j=n 的情况（越界）
        #   i == 0 表示前一半从 A 中取 0 个数，即前一半都从 B 中取；
        #   i == m 表示前一半取 A 中所有数，剩下的再从 B 中取；
        #   j == 0, j == n 同理
        a_im1 = -inf if i == 0 else A[i - 1]
        a_i = inf if i == m else A[i]
        b_jm1 = -inf if j == 0 else B[j - 1]
        b_j = inf if j == n else B[j]
        m1, m2 = max(a_im1, b_jm1), min(a_i, b_j)

        return (m1 + m2) / 2 if (m + n) % 2 == 0 else m1
```

</details>

