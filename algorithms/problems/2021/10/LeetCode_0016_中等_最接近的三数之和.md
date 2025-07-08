## 最接近的三数之和
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2022-10-14%2014%3A59%3A33&color=yellowgreen&style=flat-square)
[![](https://img.shields.io/static/v1?label=&message=%E4%B8%AD%E7%AD%89&color=yellow&style=flat-square)](../../../README.md#中等)
[![](https://img.shields.io/static/v1?label=&message=LeetCode&color=green&style=flat-square)](../../../README.md#leetcode)
[![](https://img.shields.io/static/v1?label=&message=%E5%8F%8C%E6%8C%87%E9%92%88&color=blue&style=flat-square)](../../../README.md#双指针)

<!--END_SECTION:badge-->
<!--info
tags: [双指针]
source: LeetCode
level: 中等
number: '0016'
name: 最接近的三数之和
companies: []
-->

<summary><b>问题简述</b></summary> 

```text
给定一个数组，找出该数组中和最接近指定值的三元组。
```


<details><summary><b>详细描述</b></summary> 

```text
给定一个包括 n 个整数的数组 nums 和 一个目标值 target。找出 nums 中的三个整数，使得它们的和与 target 最接近。返回这三个数的和。假定每组输入只存在唯一答案。

示例：
    输入：nums = [-1,2,1,-4], target = 1
    输出：2
    解释：与 target 最接近的和是 2 (-1 + 2 + 1 = 2) 。

提示：
    3 <= nums.length <= 10^3
    -10^3 <= nums[i] <= 10^3
    -10^4 <= target <= 10^4

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/3sum-closest
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```

</details>


<summary><b>思路</b></summary> 

- 思路跟三数之和基本一致；
- 当找到比当前更接近的结果时更新；


<details><summary><b>Python</b></summary> 

```python
from typing import List

class Solution:
    def threeSumClosest(self, nums: List[int], target: int) -> int:
        """"""
        nums = sorted(nums)

        L = len(nums)
        ret = nums[0] + nums[1] + nums[2]  # 初始化，len(nums) >= 3
        for i in range(L - 2):

            # 跳过重复元素
            if i > 0 and nums[i] == nums[i - 1]:
                continue

            # 利用单调性剪纸
            min_s = nums[i] + nums[i + 1] + nums[i + 2]  # 最小和
            if min_s > target:
                if abs(min_s - target) < abs(ret - target):
                    ret = min_s
                break

            max_s = nums[i] + nums[L - 2] + nums[L - 1]  # 最大和
            if max_s < target:
                ret = max_s
                continue

            # 初始化双指针
            l, r = i + 1, L - 1
            while l < r:
                s = nums[i] + nums[l] + nums[r]
                if abs(s - target) < abs(ret - target):
                    ret = s

                if s < target:
                    l += 1
                    while l < r and nums[l] == nums[l - 1]: l += 1
                elif s > target:
                    r -= 1
                    while l < r and nums[r] == nums[r + 1]: r -= 1
                else:  # ret == target
                    return ret
        return ret

```

</details>

<details><summary><b>利用单调性剪枝</b></summary> 

- 在经过排序后，每轮迭代时，三数之和的最大值和最小值是确定的；
- 所以如果最小值比目标值大，那么后面无论怎么移动双指针，差值都只会越来越大；最大值比目标值小时同理；
- 代码细节：

    ```python
    # 剪枝：利用单调性
    min_s = nums[i] + nums[i + 1] + nums[i + 2]  # 最小和
    if min_s > target:  # 如果最小和也大于 target，则剩余部分的差值肯定越来越大
        # 容易忽略的一步，注意此时也是有可能出现答案的，比如 ret < 0 < min_s 时
        if abs(min_s - target) < abs(ret - target):
            ret = min_s
        break

    max_s = nums[i] + nums[L - 2] + nums[L - 1]  # 最大和
    if max_s < target:  # 如果最大和也小于 target，则剩余部分的差值肯定越来越大
        ret = max_s  # 此时 ret < max_s < target，所以 max_s 必然比当前 ret 更接近目标值
        continue
    ```

</details>