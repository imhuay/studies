## 下一个更大元素
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2022-10-14%2014%3A59%3A33&color=yellowgreen&style=flat-square)
[![](https://img.shields.io/static/v1?label=&message=%E7%AE%80%E5%8D%95&color=yellow&style=flat-square)](../../../README.md#简单)
[![](https://img.shields.io/static/v1?label=&message=LeetCode&color=green&style=flat-square)](../../../README.md#leetcode)
[![](https://img.shields.io/static/v1?label=&message=%E5%8D%95%E8%B0%83%E6%A0%88/%E5%8D%95%E8%B0%83%E9%98%9F%E5%88%97&color=blue&style=flat-square)](../../../README.md#单调栈单调队列)

<!--END_SECTION:badge-->
<!--info
tags: [单调栈]
source: LeetCode
level: 简单
number: '0496'
name: 下一个更大元素
companies: []
-->

<summary><b>问题简述</b></summary>

```txt
找出 nums1 中每个元素在 nums2 中的下一个比其大的值，不存在输出 -1；
其中 nums1 是 nums2 的子集。

本题实际上就是模拟了**单调栈**最常见的使用场景；
```

<details><summary><b>详细描述</b></summary>

```txt

给你两个 没有重复元素 的数组 nums1 和 nums2 ，其中 nums1 是 nums2 的子集。

请你找出 nums1 中每个元素在 nums2 中的下一个比其大的值。

nums1 中数字 x 的下一个更大元素是指 x 在 nums2 中对应位置的右边的第一个比 x 大的元素。如果不存在，对应位置输出 -1 。

示例 1:
    输入: nums1 = [4,1,2], nums2 = [1,3,4,2].
    输出: [-1,3,-1]
    解释:
        对于 num1 中的数字 4 ，你无法在第二个数组中找到下一个更大的数字，因此输出 -1 。
        对于 num1 中的数字 1 ，第二个数组中数字1右边的下一个较大数字是 3 。
        对于 num1 中的数字 2 ，第二个数组中没有下一个更大的数字，因此输出 -1 。
示例 2:
    输入: nums1 = [2,4], nums2 = [1,2,3,4].
    输出: [3,-1]
    解释:
        对于 num1 中的数字 2 ，第二个数组中的下一个较大数字是 3 。
        对于 num1 中的数字 4 ，第二个数组中没有下一个更大的数字，因此输出 -1 。
 
提示：
    1 <= nums1.length <= nums2.length <= 1000
    0 <= nums1[i], nums2[i] <= 10^4
    nums1和nums2中所有整数 互不相同
    nums1 中的所有整数同样出现在 nums2 中
 

进阶：你可以设计一个时间复杂度为 O(nums1.length + nums2.length) 的解决方案吗？

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/next-greater-element-i
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

```

<!-- <div align="center"><img src="./_assets/xxx.png" height="300" /></div> -->

</details>


<summary><b>思路</b></summary>

<details><summary><b>Python：单调栈</b></summary>

```python
class Solution:
    def nextGreaterElement(self, nums1: List[int], nums2: List[int]) -> List[int]:
        res = {}  # 保存结果
        stack = []  # 模拟单调栈
        for num in reversed(nums2):  # 逆序遍历
            while stack and num >= stack[-1]:  # 当栈不为空，且当前值大于栈顶值时
                stack.pop()  # 弹出栈顶值（list.pop 默认弹出最后一个值）
            res[num] = stack[-1] if stack else -1  # 如果此时栈不为空，那么栈顶值就是下一个比当前大的值
            stack.append(num)  # 把当前值入栈
        return [res[num] for num in nums1]  # 遍历完 nums2 中的所有元素后，就得到了 nums1 中每个元素下一个比它大的值，因为 num1 是 nums2 的子集
```

</details>



