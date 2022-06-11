## LeetCode_0011_盛最多水的容器（中等, 2021-10）
<!--{
    "tags": ["双指针"],
    "来源": "LeetCode",
    "编号": "0011",
    "难度": "中等",
    "标题": "盛最多水的容器"
}-->

<summary><b>问题描述</b></summary>

```txt
给你 n 个非负整数 a1，a2，...，an，每个数代表坐标中的一个点 (i, ai) 。在坐标内画 n 条垂直线，垂直线 i 的两个端点分别为 (i, ai) 和 (i, 0) 。找出其中的两条线，使得它们与 x 轴共同构成的容器可以容纳最多的水。

说明：不能倾斜容器。

示例 1：
    输入：[1,8,6,2,5,4,8,3,7]
    输出：49 
    解释：图中垂直线代表输入数组 [1,8,6,2,5,4,8,3,7]。在此情况下，容器能够容纳水（表示为蓝色部分）的最大值为 49。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/container-with-most-water
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```

<div align="center"><img src="../../../_assets/question_11.jpeg" height="150" /></div>


<summary><b>思路</b></summary>

- 首尾双指针遍历


<details><summary><b>Python</b></summary>

```python
class Solution:
    def maxArea(self, height: List[int]) -> int:
        """"""
        l, r = 0, len(height) - 1
        ret = (r - l) * min(height[l], height[r])  # 初始化

        while l < r:
            if height[l] < height[r]:
                l += 1
            else:
                r -= 1
            
            tmp = (r - l) * min(height[l], height[r])
            ret = max(ret, tmp)
            
        return ret
```

</details>

