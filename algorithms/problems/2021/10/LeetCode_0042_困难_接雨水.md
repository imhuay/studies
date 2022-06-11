## LeetCode_0042_接雨水（困难, 2021-10）
<!--{
    "tags": ["双指针"],
    "来源": "LeetCode",
    "编号": "0042",
    "难度": "困难",
    "标题": "接雨水"
}-->

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


<summary><b>思路</b></summary>

<details><summary><b>法1）Python：双指针</b></summary>

```Python
class Solution:
    def trap(self, height: List[int]) -> int:
        """"""
        l, r = 0, len(height) - 1
        
        ans = 0
        max_l = max_r = 0  # 保存当前位置时，左右最高的柱子
        
        while l <= r:
            if height[l] <= height[r]:
                if height[l] > max_l:
                    max_l = height[l]
                else:
                    ans += max_l - height[l]
                l += 1
            else:
                if height[r] > max_r:
                    max_r = height[r]
                else:
                    ans += max_r - height[r]
                r -= 1
                
        return ans
``` 

</details>


<details><summary><b>法2）C++：左右遍历两次</b></summary>

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
