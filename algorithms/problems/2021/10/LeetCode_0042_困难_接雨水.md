## 接雨水
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2025-07-08%2016%3A53%3A13&color=yellowgreen&style=flat-square)
[![](https://img.shields.io/static/v1?label=&message=%E5%9B%B0%E9%9A%BE&color=yellow&style=flat-square)](../../../README.md#困难)
[![](https://img.shields.io/static/v1?label=&message=LeetCode&color=green&style=flat-square)](../../../README.md#leetcode)
[![](https://img.shields.io/static/v1?label=&message=%E5%8F%8C%E6%8C%87%E9%92%88&color=blue&style=flat-square)](../../../README.md#双指针)
[![](https://img.shields.io/static/v1?label=&message=LeetCode%20Hot%20100&color=blue&style=flat-square)](../../../README.md#leetcode-hot-100)
[![](https://img.shields.io/static/v1?label=&message=%E7%83%AD%E9%97%A8&color=blue&style=flat-square)](../../../README.md#热门)

<!--END_SECTION:badge-->
<!--info
tags: [双指针, lc100, 热门]
source: LeetCode
level: 困难
number: '0042'
name: 接雨水
companies: []
-->

<summary><b>问题描述</b></summary>

```txt
给定 n 个非负整数表示每个宽度为 1 的柱子的高度图，计算按此排列的柱子，下雨之后能接多少雨水。

示例 1（如图）：
    输入：height = [0,1,0,2,1,0,1,3,2,1,2,1]
    输出：6
    解释：上面是由数组 [0,1,0,2,1,0,1,3,2,1,2,1] 表示的高度图，在这种情况下，可以接 6 个单位的雨水（蓝色部分表示雨水）。 

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/trapping-rain-water
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```

<div align="center"><img src="../../../_assets/rainwatertrap.png" height="150" /></div>


<summary><b>思路 1：双指针</b></summary>

- 设置两个变量分别记录左右最高高度；
- 双指针移动时优先移动较矮的位置，并更新能带来的增量；
- 画图理解这个过程；

<details><summary><b>Python</b></summary>

```Python
class Solution:
    def trap(self, height: List[int]) -> int:

        l, r = 0, len(height) - 1  # 首尾双指针
        l_max, r_max = 0, 0  # 记录当前位置，左右的最高高度
        ret = 0
        while l < r:
            # 更新左右最高高度
            l_max = max(l_max, height[l])
            r_max = max(r_max, height[r])

            # 取左右较矮的作为当前位置
            if height[l] < height[r]:  # <= 也可以
                cur = height[l]
                l += 1
            else:
                cur = height[r]
                r -= 1
            
            ret += min(l_max, r_max) - cur  # 更新当前位置能带来的增量
        
        return ret
``` 

</details>


<summary><b>思路 2：遍历两次</b></summary>

- 分别从左向右和从右向左遍历两次，记录每个位置左右两侧的最高高度；

<details><summary><b>C++</b></summary>

```C++
class Solution {
public:
    int trap(vector<int>& H) {
        int n = H.size();
        
        vector<int> l_max(H);
        vector<int> r_max(H);
        
        for(int i=1; i<n; i++)
            l_max[i] = max(l_max[i-1], l_max[i]);
        
        for(int i=n-2; i>=0; i--)
            r_max[i] = max(r_max[i+1], r_max[i]);
        
        int ret = 0;
        for (int i=1; i<n-1; i++)
            ret += min(l_max[i], r_max[i]) - H[i];
        
        return ret;
    }
};
``` 

</details>
