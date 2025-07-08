## 数组中出现次数超过一半的数字（摩尔投票）
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2022-10-14%2014%3A59%3A33&color=yellowgreen&style=flat-square)
[![](https://img.shields.io/static/v1?label=&message=%E7%AE%80%E5%8D%95&color=yellow&style=flat-square)](../../../README.md#简单)
[![](https://img.shields.io/static/v1?label=&message=%E5%89%91%E6%8C%87Offer&color=green&style=flat-square)](../../../README.md#剑指offer)
[![](https://img.shields.io/static/v1?label=&message=%E6%8E%92%E5%BA%8F&color=blue&style=flat-square)](../../../README.md#排序)
[![](https://img.shields.io/static/v1?label=&message=%E6%A8%A1%E6%8B%9F&color=blue&style=flat-square)](../../../README.md#模拟)
[![](https://img.shields.io/static/v1?label=&message=%E5%88%86%E6%B2%BB&color=blue&style=flat-square)](../../../README.md#分治)
[![](https://img.shields.io/static/v1?label=&message=%E7%BB%8F%E5%85%B8&color=blue&style=flat-square)](../../../README.md#经典)

<!--END_SECTION:badge-->
<!--info
tags: [排序, 模拟, 分治, 经典]
source: 剑指Offer
level: 简单
number: '3900'
name: 数组中出现次数超过一半的数字（摩尔投票）
companies: []
-->

<summary><b>问题简述</b></summary>

```txt
数组中有一个数字出现的次数超过数组长度的一半，请找出这个数字。
```

<details><summary><b>详细描述</b></summary>

```txt
数组中有一个数字出现的次数超过数组长度的一半，请找出这个数字。

你可以假设数组是非空的，并且给定的数组总是存在多数元素。

示例 1:
    输入: [1, 2, 3, 2, 2, 2, 5, 4, 2]
    输出: 2
限制：
    1 <= 数组长度 <= 50000

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/shu-zu-zhong-chu-xian-ci-shu-chao-guo-yi-ban-de-shu-zi-lcof
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```

</details>

<!-- <div align="center"><img src="../../../_assets/xxx.png" height="300" /></div> -->

<summary><b>思路1：排序</b></summary>

- 排序后，数组中间位置的数一定满足题意；
- 时间复杂度 `O(NlogN)`；

<details><summary><b>Python</b></summary>

```python
class Solution:
    def majorityElement(self, nums: List[int]) -> int:
        return sorted(nums)[len(nums) // 2]
```

</details>


<summary><b>思路2：计数</b></summary>

- 一次遍历，记录每个数出现的次数；
- 空间复杂度 `O(N)`；

<details><summary><b>Python</b></summary>

```python
class Solution:
    def majorityElement(self, nums: List[int]) -> int:
        from collections import defaultdict

        cnt = defaultdict(int)

        for x in nums:
            cnt[x] += 1
            if cnt[x] > len(nums) // 2:
                return x
        
        # return -1
```

</details>


<summary><b>思路3：“摩尔投票法”</b></summary>

> [数组中出现次数超过一半的数字（摩尔投票法，清晰图解）](https://leetcode-cn.com/problems/shu-zu-zhong-chu-xian-ci-shu-chao-guo-yi-ban-de-shu-zi-lcof/solution/mian-shi-ti-39-shu-zu-zhong-chu-xian-ci-shu-chao-3/)

- “摩尔投票法”的核心思想是**一一抵消**；
- 假设已知目标数为 x，遍历时若出现一次 x 记 `+1` 票，否则为 `-1` 票；
    - 推论1：最终票数和必大于 0；
    - 推论2：若前 n 个数的票数和为 0，那么剩余部分依然满足推论1，即目标数字依然为 x；

<details><summary><b>Python</b></summary>

```python
class Solution:
    def majorityElement(self, nums: List[int]) -> int:

        cnt = 0
        for x in nums:
            if cnt == 0:  # 当票数和为 0 时，假设当前值为目标值
                ret = x   # 如果这个数不是目标值，那么它迟早会因为不断 -1，被替换掉
                
            if x == ret:
                cnt += 1
            else:
                cnt -= 1
        
        return ret
```

</details>


<summary><b>思路4：分治</b></summary>

> [数组中出现次数超过一半的数字](https://leetcode-cn.com/problems/shu-zu-zhong-chu-xian-ci-shu-chao-guo-yi-ban-de-shu-zi-lcof/solution/shu-zu-zhong-chu-xian-ci-shu-chao-guo-yi-pvh8/)

- 本题使用分治在时间和空间上都不是最优，仅用于理解分治的思想；

<details><summary><b>Python</b></summary>

```python
class Solution:
    def majorityElement(self, nums: List[int]) -> int:

        def recur(lo, hi):  # [lo, hi] 闭区间
            if lo == hi:  # 当数组中只有一个元素时，这个数就是目标值
                return nums[lo]

            # 分治
            mid = (hi - lo) // 2 + lo
            l = recur(lo, mid)
            r = recur(mid + 1, hi)

            # 如果左右返回值相同时，显然这个值就是目标值
            if l == r:
                return l

            # 否则需要判断哪个出现的次数更多
            lc = sum(1 for i in range(lo, hi + 1) if nums[i] == l)
            rc = sum(1 for i in range(lo, hi + 1) if nums[i] == r)
            return l if lc > rc else r

        return recur(0, len(nums) - 1)
```

</details>
