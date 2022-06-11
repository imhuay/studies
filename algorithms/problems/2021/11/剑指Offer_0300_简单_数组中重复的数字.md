## 剑指Offer_0300_数组中重复的数字（简单, 2021-11）
<!--{
    "tags": ["哈希表"],
    "来源": "剑指Offer",
    "编号": "0300",
    "难度": "简单",
    "标题": "数组中重复的数字"
}-->

<summary><b>问题简述</b></summary>

```txt
找出数组中任意一个重复的数字。
```

<details><summary><b>详细描述</b></summary>

```txt
找出数组中重复的数字。

在一个长度为 n 的数组 nums 里的所有数字都在 0～n-1 的范围内。数组中某些数字是重复的，但不知道有几个数字重复了，也不知道每个数字重复了几次。请找出数组中任意一个重复的数字。

示例 1：
    输入：
    [2, 3, 1, 0, 2, 5, 3]
    输出：2 或 3 

限制：
    2 <= n <= 100000

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/shu-zu-zhong-zhong-fu-de-shu-zi-lcof
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```

<!-- <div align="center"><img src="../../../_assets/xxx.png" height="300" /></div> -->

</details>

<summary><b>思路</b></summary>

- 遍历数组，保存见过的数字，当遇到出现过的数字即返回


<details><summary><b>Python</b></summary>

```python
class Solution:
    def findRepeatNumber(self, nums: List[int]) -> int:
        tb = set()
        for i in nums:
            if i in tb:
                return i
            tb.add(i)
```

</details>

