## LeetCode_0033_搜索旋转排序数组（中等, 2021-10）
<!--{
    "tags": ["二分查找"],
    "来源": "LeetCode",
    "编号": "0033",
    "难度": "中等",
    "标题": "搜索旋转排序数组"
}-->

<summary><b>问题简述</b></summary>

```txt
在一个旋转过的有序数组中搜索某值，若存在返回下标，否则返回 -1。
```


<details><summary><b>详细描述</b></summary>

```txt
整数数组 nums 按升序排列，数组中的值 互不相同 。

在传递给函数之前，nums 在预先未知的某个下标 k（0 <= k < nums.length）上进行了 旋转，使数组变为 [nums[k], nums[k+1], ..., nums[n-1], nums[0], nums[1], ..., nums[k-1]]（下标 从 0 开始 计数）。例如， [0,1,2,4,5,6,7] 在下标 3 处经旋转后可能变为 [4,5,6,7,0,1,2] 。

给你 旋转后 的数组 nums 和一个整数 target ，如果 nums 中存在这个目标值 target ，则返回它的下标，否则返回 -1 。

示例 1：
    输入：nums = [4,5,6,7,0,1,2], target = 0
    输出：4
示例 2：
    输入：nums = [4,5,6,7,0,1,2], target = 3
    输出：-1
示例 3：
    输入：nums = [1], target = 0
    输出：-1
 

提示：
    1 <= nums.length <= 5000
    -10^4 <= nums[i] <= 10^4
    nums 中的每个值都 独一无二
    题目数据保证 nums 在预先未知的某个下标上进行了旋转
    -10^4 <= target <= 10^4
 
进阶：你可以设计一个时间复杂度为 O(log n) 的解决方案吗？

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/search-in-rotated-sorted-array
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```

</details>


<summary><b>思路</b></summary>

- “二分”的本质是两段性，而不是单调性；即只要二分后，左边满足某个性质，右边不满足某个性质，即可使用二分；
- 比如本题二分后，有前半段满足 >= nums[0]，而后半段不满足；

    > [LogicStack-LeetCode/33.搜索旋转排序数组（中等）](https://github.com/SharingSource/LogicStack-LeetCode/blob/main/LeetCode/31-40/33.%20搜索旋转排序数组（中等）.md#二分解法)


<details><summary><b>Python：二分查找</b></summary>

- 将数组从中间分开成左右两部分时，一定有一部分的数组是有序的。

```python
class Solution:
    def search(self, nums: List[int], target: int) -> int:
        if not nums:
            return -1

        L = len(nums) - 1
        l, r = 0, L
        while l <= r:
            mid = l + (r - l) // 2  # 中点下标

            if nums[mid] == target:
                return mid

            if nums[0] <= nums[mid]:  # [0, mid) 是有序的
                # 如果目标在[0, mid)，则将搜索范围缩小到 [0,mid-1]，反之 [mid+1,L]
                if nums[0] <= target < nums[mid]:
                    r = mid - 1
                else:
                    l = mid + 1
            else:  # (mid, L] 是有序的
                # 同理，如果目标在(mid, L]，则将搜索范围缩小到 [mid+1,L]，反之 [0,mid-1]
                if nums[mid] < target <= nums[L]:
                    l = mid + 1
                else:
                    r = mid - 1

        return -1

```

</details>

