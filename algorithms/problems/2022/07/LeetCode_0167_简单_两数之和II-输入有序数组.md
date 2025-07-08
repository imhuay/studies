## 两数之和II-输入有序数组
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2022-10-14%2014%3A59%3A33&color=yellowgreen&style=flat-square)
[![](https://img.shields.io/static/v1?label=&message=%E7%AE%80%E5%8D%95&color=yellow&style=flat-square)](../../../README.md#简单)
[![](https://img.shields.io/static/v1?label=&message=LeetCode&color=green&style=flat-square)](../../../README.md#leetcode)
[![](https://img.shields.io/static/v1?label=&message=%E5%8F%8C%E6%8C%87%E9%92%88&color=blue&style=flat-square)](../../../README.md#双指针)

<!--END_SECTION:badge-->
<!--info
tags: [双指针]
source: LeetCode
level: 简单
number: '0167'
name: 两数之和II-输入有序数组
companies: []
-->

<summary><b>问题简述</b></summary>

```txt
找出一个非递减数组中和等于 target 的两个数字，输出它们的下标。

假定题目一定有一个解。
```

<details><summary><b>详细描述</b></summary>

```txt
给定一个已按照 非递减顺序排列 的整数数组 numbers ，请你从数组中找出两个数满足相加之和等于目标数 target 。

函数应该以长度为 2 的整数数组的形式返回这两个数的下标值。numbers 的下标 从 1 开始计数 ，所以答案数组应当满足 1 <= answer[0] < answer[1] <= numbers.length 。

你可以假设每个输入 只对应唯一的答案 ，而且你 不可以 重复使用相同的元素。

 
示例 1：
    输入：numbers = [2,7,11,15], target = 9
    输出：[1,2]
    解释：2 与 7 之和等于目标数 9 。因此 index1 = 1, index2 = 2 。
示例 2：
    输入：numbers = [2,3,4], target = 6
    输出：[1,3]
示例 3：
    输入：numbers = [-1,0], target = -1
    输出：[1,2]


提示：
    2 <= numbers.length <= 3 * 10^4
    -1000 <= numbers[i] <= 1000
    numbers 按 非递减顺序 排列
    -1000 <= target <= 1000
    仅存在一个有效答案

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/two-sum-ii-input-array-is-sorted
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```

</details>

<summary><b>思路</b></summary>

<details><summary><b>Python：双指针</b></summary>

```python
class Solution:
    def twoSum(self, numbers: List[int], target: int) -> List[int]:
        """"""
        lo, hi = 0, len(numbers) - 1

        while lo < hi:
            tmp = numbers[lo] + numbers[hi]

            if tmp < target:
                lo += 1
            elif tmp > target:
                hi -= 1
            else:
                return [lo + 1, hi + 1]
```

</details>
