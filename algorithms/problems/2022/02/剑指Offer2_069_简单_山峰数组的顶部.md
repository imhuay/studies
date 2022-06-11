## 剑指Offer2_069_山峰数组的顶部（简单, 2022-02）
<!--{
    "tags": ["二分查找"],
    "来源": "剑指Offer2",
    "编号": "069",
    "难度": "简单",
    "标题": "山峰数组的顶部"
}-->

<summary><b>问题简述</b></summary>

```txt
找出山脉数组中山峰的下标（保证给出的数组是一个山脉数组）
```

<details><summary><b>详细描述</b></summary>

```txt
符合下列属性的数组 arr 称为 山峰数组（山脉数组） ：

    arr.length >= 3
    存在 i（0 < i < arr.length - 1）使得：
        arr[0] < arr[1] < ... arr[i-1] < arr[i]
        arr[i] > arr[i+1] > ... > arr[arr.length - 1]
    
    给定由整数组成的山峰数组 arr ，返回任何满足 arr[0] < arr[1] < ... arr[i - 1] < arr[i] > arr[i + 1] > ... > arr[arr.length - 1] 的下标 i ，即山峰顶部。

示例 1：
    输入：arr = [0,1,0]
    输出：1
示例 2：
    输入：arr = [1,3,5,4,2]
    输出：2
示例 3：
    输入：arr = [0,10,5,2]
    输出：1
示例 4：
    输入：arr = [3,4,5,1]
    输出：2
示例 5：
    输入：arr = [24,69,100,99,79,78,67,36,26,19]
    输出：2

提示：
    3 <= arr.length <= 10^4
    0 <= arr[i] <= 10^6
    题目数据保证 arr 是一个山脉数组
 
进阶：很容易想到时间复杂度 O(n) 的解决方案，你可以设计一个 O(log(n)) 的解决方案吗？

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/B1IidL
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```

</details>


<summary><b>思路</b></summary>

- 当 `N[mid] > N[mid+1]` 时，山峰必在左侧；反之，在右侧；
- 因为从中间划分后，左右分别满足相反的性质，因此可以使用二分查找；


<details><summary><b>Python</b></summary>

```python
class Solution:
    def peakIndexInMountainArray(self, arr: List[int]) -> int:
        """"""
        left, right = 1, len(arr) - 2

        ans = 0
        while left <= right:
            mid = left + (right - left) // 2
            if arr[mid] > arr[mid + 1]:  # 山峰在左侧
                ans = mid  # 目前已知 mid 位置的值是最大的，因为保证 arr 是一个山脉数组，所以一定会来到这个分支
                right = mid - 1
            else:  # 山峰在右侧
                left = mid + 1

        return ans
```

</details>

