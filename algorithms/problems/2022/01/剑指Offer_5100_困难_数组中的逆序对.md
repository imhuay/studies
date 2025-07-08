## 数组中的逆序对
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2022-10-14%2014%3A59%3A33&color=yellowgreen&style=flat-square)
[![](https://img.shields.io/static/v1?label=&message=%E5%9B%B0%E9%9A%BE&color=yellow&style=flat-square)](../../../README.md#困难)
[![](https://img.shields.io/static/v1?label=&message=%E5%89%91%E6%8C%87Offer&color=green&style=flat-square)](../../../README.md#剑指offer)
[![](https://img.shields.io/static/v1?label=&message=%E5%88%86%E6%B2%BB&color=blue&style=flat-square)](../../../README.md#分治)
[![](https://img.shields.io/static/v1?label=&message=%E7%BA%BF%E6%AE%B5%E6%A0%91/%E6%A0%91%E7%8A%B6%E6%95%B0%E7%BB%84&color=blue&style=flat-square)](../../../README.md#线段树树状数组)
[![](https://img.shields.io/static/v1?label=&message=%E7%BB%8F%E5%85%B8&color=blue&style=flat-square)](../../../README.md#经典)

<!--END_SECTION:badge-->
<!--info
tags: [分治, 树状数组, 经典]
source: 剑指Offer
level: 困难
number: '5100'
name: 数组中的逆序对
companies: []
-->

<summary><b>问题简述</b></summary>

```txt
在数组中的两个数字，如果前一个数字大于后面的数字，则这两个数字组成一个逆序对。
输入一个数组，求该数组中的逆序对的总数。
```

<details><summary><b>详细描述</b></summary>

```txt
在数组中的两个数字，如果前面一个数字大于后面的数字，则这两个数字组成一个逆序对。输入一个数组，求出这个数组中的逆序对的总数。

示例 1:
    输入: [7,5,6,4]
    输出: 5

限制：
    0 <= 数组长度 <= 50000

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/shu-zu-zhong-de-ni-xu-dui-lcof
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```

</details>

<!-- <div align="center"><img src="../../../_assets/xxx.png" height="300" /></div> -->

<summary><b>思路1：利用归并排序</b></summary>

- **归并排序**

    <div align="center"><img src="../../../_assets/剑指Offer_0051_困难_数组中的逆序对.png" height="300" /></div> 

    > [数组中的逆序对（归并排序，清晰图解）](https://leetcode-cn.com/problems/shu-zu-zhong-de-ni-xu-dui-lcof/solution/jian-zhi-offer-51-shu-zu-zhong-de-ni-xu-pvn2h/)

- **在合并过程中统计逆序对的数量**
    - 归并排序的合并过程：依次比较两个子数组的首元素，将其中较小的放置到一个新的数组中；
    - 每当遇到`左子数组当前元素 > 右子数组当前元素`时，意味着「左子数组当前元素 至 末尾元素」与「右子数组当前元素」构成了若干「逆序对」

- 归并排序需要用到辅助数组，因此其空间复杂度为 `O(N)`；
    - 辅助数组一般有两种用法，分别见写法1 和 写法2；

<details><summary><b>Python：写法1</b></summary>

```python
class Solution:
    def reversePairs(self, nums: List[int]) -> int:
        
        # 临时数组 for 归并排序：空间复杂度 O(N)
        tmp = [0] * len(nums)

        def merge(lo, hi):  # 闭区间 [lo, hi]
            if lo >= hi: return 0

            m = (lo + hi) // 2
            ret = merge(lo, m) + merge(m + 1, hi)  # 分治

            # 辅助数组
            tmp[lo: hi + 1] = nums[lo: hi + 1]  # 先复制，再赋值

            l, r = lo, m + 1  # 左右指针
            for i in range(lo, hi + 1):
                # 必须先判断是否越界
                if l == m + 1:  # 左子数组遍历完毕
                    nums[i] = tmp[r]
                    r += 1
                elif r == hi + 1 or tmp[l] <= tmp[r]:  # 右子数组遍历完毕，或 tmp[l] <= tmp[r] 时，即左指针位置小于右指针位置
                    nums[i] = tmp[l]
                    l += 1
                else:  # tmp[l] > tmp[r] 时
                    nums[i] = tmp[r]
                    r += 1
                    ret += m - l + 1  # 累计逆序对数

            return ret

        return merge(0, len(nums) - 1)
```

</details>

<details><summary><b>Python：写法2</b></summary>

```python
class Solution:
    def reversePairs(self, nums: List[int]) -> int:
        
        # 临时数组 for 归并排序：空间复杂度 O(N)
        tmp = [0] * len(nums)

        def merge(lo, hi):  # 闭区间 [lo, hi]
            if lo >= hi: return 0

            m = (lo + hi) // 2
            ret = merge(lo, m) + merge(m + 1, hi)  # 分治

            l, r = lo, m + 1  # 左右指针
            for i in range(lo, hi + 1):
                # 必须先判断是否越界
                if l == m + 1:  # 左子数组遍历完毕
                    tmp[i] = nums[r]
                    r += 1
                elif r == hi + 1 or nums[l] <= nums[r]:  # 右子数组遍历完毕，或 nums[l] <= nums[r]
                    tmp[i] = nums[l]
                    l += 1
                else:  # nums[l] > nums[r]
                    tmp[i] = nums[r]
                    r += 1
                    ret += m - l + 1  # 累计逆序对数

            # 辅助数组
            nums[lo: hi + 1] = tmp[lo: hi + 1]  # 先赋值，再覆盖
            return ret

        return merge(0, len(nums) - 1)
```

</details>


<summary><b>思路2：树状数组</b></summary>

> [数组中的逆序对](https://leetcode-cn.com/problems/shu-zu-zhong-de-ni-xu-dui-lcof/solution/shu-zu-zhong-de-ni-xu-dui-by-leetcode-solution/)

<details><summary><b>Python</b></summary>

```python
class BIT:
    def __init__(self, n):
        self.n = n
        self.tree = [0] * (n + 1)

    @staticmethod
    def lowbit(x):
        return x & (-x)
    
    def query(self, x):
        ret = 0
        while x > 0:
            ret += self.tree[x]
            x -= BIT.lowbit(x)
        return ret

    def update(self, x):
        while x <= self.n:
            self.tree[x] += 1
            x += BIT.lowbit(x)

class Solution:
    def reversePairs(self, nums: List[int]) -> int:
        n = len(nums)

        # 离散化
        tmp = sorted(nums)
        for i in range(n):
            nums[i] = bisect.bisect_left(tmp, nums[i]) + 1

        # 树状数组统计逆序对
        bit = BIT(n)
        ans = 0
        for i in range(n - 1, -1, -1):
            ans += bit.query(nums[i] - 1)
            bit.update(nums[i])
        return ans

```

</details>


<summary><b>更快的代码</b></summary>

<!-- - 利用归并排序求逆序对的核心是，在合并两个有序数组时可以快速累计逆序对数，其实这个过程在快排中也存在； -->

<details><summary><b>Python：快排？</b></summary>

```python
class Solution:
    def reversePairs(self, nums: List[int]) -> int:
        if len(nums) <= 1: return 0

        more, less = [], []
        count = 0
        center_count = 0
        center = random.choice(nums)
        for i in nums:
            if i > center:
                more.append(i)
            elif i == center:
                center_count += 1
                count += len(more)
            else:
                count += center_count
                count += len(more)
                less.append(i)
        count += self.reversePairs(more) + self.reversePairs(less)
        return count
```

</details>

<details><summary><b>Python：二分？</b></summary>

```python
class Solution:
    def reversePairs(self, nums: List[int]) -> int:
        tmp = []
        ret = 0
        for num in nums[::-1]:
            cur = bisect_left(tmp, num)
            ret += cur

            tmp[cur:cur] = [num]  # 用这句是 732ms
            # tmp.insert(cur, num)  # 用这句是 1624ms

        return ret
```

</details>