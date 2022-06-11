## LeetCode_0001_两数之和（简单, 2021-10）
<!--{
    "tags": ["哈希表"],
    "来源": "LeetCode",
    "编号": "0001",
    "难度": "简单",
    "标题": "两数之和"
}-->

<summary><b>问题简述</b></summary>

```txt
给定一个整数数组 nums 和一个整数目标值 target，请你在该数组中找出 和为目标值 target  的那 两个 整数，并返回它们的数组下标。
```


<details><summary><b>详细描述</b></summary>

```txt
给定一个整数数组 nums 和一个整数目标值 target，请你在该数组中找出 和为目标值 target  的那 两个 整数，并返回它们的数组下标。

你可以假设每种输入只会对应一个答案。但是，数组中同一个元素在答案里不能重复出现。

你可以按任意顺序返回答案。

示例 1：
    输入：nums = [2,7,11,15], target = 9
    输出：[0,1]
    解释：因为 nums[0] + nums[1] == 9 ，返回 [0, 1] 。
示例 2：
    输入：nums = [3,2,4], target = 6
    输出：[1,2]
示例 3：
    输入：nums = [3,3], target = 6
    输出：[0,1]
 

提示：
    2 <= nums.length <= 10^4
    -10^9 <= nums[i] <= 10^9
    -10^9 <= target <= 10^9
    只会存在一个有效答案

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/two-sum
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```

</details>

<summary><b>思路</b></summary>

<details><summary><b>Python3</b></summary>

```python
class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:  # noqa
        """"""
        tmp = dict()

        for i in range(len(nums)):
            left = target - nums[i]  # 减去当前值
            if left in tmp:  # 如果差值在哈希表中，说明找到了答案
                return [tmp[left], i]

            tmp[nums[i]] = i  # 保存当前值的位置

        return []

```

</details>
