## 旋转数组的最小数字
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2022-10-14%2014%3A59%3A33&color=yellowgreen&style=flat-square)
[![](https://img.shields.io/static/v1?label=&message=%E7%AE%80%E5%8D%95&color=yellow&style=flat-square)](../../../README.md#简单)
[![](https://img.shields.io/static/v1?label=&message=%E5%89%91%E6%8C%87Offer&color=green&style=flat-square)](../../../README.md#剑指offer)
[![](https://img.shields.io/static/v1?label=&message=%E4%BA%8C%E5%88%86%E6%9F%A5%E6%89%BE&color=blue&style=flat-square)](../../../README.md#二分查找)

<!--END_SECTION:badge-->
<!--info
tags: [二分查找]
source: 剑指Offer
level: 简单
number: '1100'
name: 旋转数组的最小数字
companies: []
-->

<summary><b>问题简述</b></summary>

```txt
求旋转数组中的最小元素；
旋转数组：将一个有序数组的前 N 个数组拼接到末尾；
例如，数组 [3,4,5,1,2] 为 [1,2,3,4,5] 的一个旋转；
```

<details><summary><b>详细描述</b></summary>

```txt
把一个数组最开始的若干个元素搬到数组的末尾，我们称之为数组的旋转。输入一个递增排序的数组的一个旋转，输出旋转数组的最小元素。例如，数组 [3,4,5,1,2] 为 [1,2,3,4,5] 的一个旋转，该数组的最小值为1。  

示例 1：
    输入：[3,4,5,1,2]
    输出：1
示例 2：
    输入：[2,2,2,0,1]
    输出：0

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/xuan-zhuan-shu-zu-de-zui-xiao-shu-zi-lcof
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```

<!-- <div align="center"><img src="../../../_assets/xxx.png" height="300" /></div> -->

</details>

<summary><b>思路：二分查找</b></summary>

- 本题的难点是比较基准的确定（详见代码）
- 本题虽然是简单题，但有很多需要注意的点；
  > [旋转数组的最小数字（二分法，清晰图解）](https://leetcode-cn.com/problems/xuan-zhuan-shu-zu-de-zui-xiao-shu-zi-lcof/solution/mian-shi-ti-11-xuan-zhuan-shu-zu-de-zui-xiao-shu-3/)


<details><summary><b>Python</b></summary>

```python
class Solution:
    def minArray(self, numbers: List[int]) -> int:
        """"""
        if numbers[0] < numbers[-1]:  # 只有严格小于，才说明没有发生旋转
            return numbers[0]

        l, r = -1, len(numbers) - 1  # 本题设置为左开右闭较合适，即 (l, r]
        while l + 1 < r:
            mid = l + (r - l) // 2  # l <= mid < r
            if numbers[mid] > numbers[r]:  # 中值大于右边界，说明最小值在右侧
                l = mid  # 因为设置 l 为开区间，故不需要 l = mid + 1
            elif numbers[mid] < numbers[r]:  # 中值小于右边界，说明最小值在左侧
                r = mid  # mid 本身就可能是最小值，且 r 为闭区间，故不需要 r = mid - 1
            else:
                r -= 1  # 关键步骤，当 numbers[mid] == numbers[r] 时，无法判断旋转点 x 是在 (l, m] 还是 (m, r] 区间中，通过 r-=1 来缩小范围

        return numbers[r]  # 循环结束时，应有 l+1 == r
```

</details>

