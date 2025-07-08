## 全排列
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2022-10-29%2023%3A59%3A13&color=yellowgreen&style=flat-square)
[![](https://img.shields.io/static/v1?label=&message=%E4%B8%AD%E7%AD%89&color=yellow&style=flat-square)](../../../README.md#中等)
[![](https://img.shields.io/static/v1?label=&message=LeetCode&color=green&style=flat-square)](../../../README.md#leetcode)
[![](https://img.shields.io/static/v1?label=&message=%E9%80%92%E5%BD%92&color=blue&style=flat-square)](../../../README.md#递归)
[![](https://img.shields.io/static/v1?label=&message=LeetCode%20Hot%20100&color=blue&style=flat-square)](../../../README.md#leetcode-hot-100)
[![](https://img.shields.io/static/v1?label=&message=%E7%83%AD%E9%97%A8&color=blue&style=flat-square)](../../../README.md#热门)

<!--END_SECTION:badge-->
<!--info
tags: [递归+回溯, lc100, 热门]
source: LeetCode
level: 中等
number: '0046'
name: 全排列
companies: []
-->

> [46. 全排列 - 力扣（LeetCode）](https://leetcode.cn/problems/permutations/?favorite=2cktkvj)

<summary><b>问题简述</b></summary>

```txt
给定一个不含重复数字的数组 nums ，返回其 所有可能的全排列 。你可以 按任意顺序 返回答案。
```

<!-- 
<details><summary><b>详细描述</b></summary>

```txt
```

</details>
-->

<!-- <div align="center"><img src="../../../_assets/xxx.png" height="300" /></div> -->

<summary><b>思路 1</b></summary>

- 递归+回溯模板：
- 把递归过程看作一棵树的生成过程，考虑两个关键问题：
  1. 每个节点需要产生哪些分支；
  2. 何时结束一条路径上的递归（递归基）；
- 本题中，
  - 对第一个问题：每个节点产生的分支由**在这条路径上**未使用过的数字决定；因此可以使用一个全局变量记录已经用过的数字，遍历时跳过这些数字即可；
    - 路径上的每个节点代表一次递归的深入，所以需要使用全局变量来记录（或者把变量作为参数传递到下一层），这个过程可以看作是一次**纵向剪枝**；
    - 如果是**横向剪枝**，则可以使用一个局部变量来记录（相关问题：[全排列 II](https://leetcode.cn/problems/permutations-ii/)）；
  - 对第二个问题：使用一个变量记录当前的递归深度（最简单）；或者判断全局变量中每个数字都使用过；

<details><summary><b>Python</b></summary>

```python
class Solution:
    def permute(self, nums: List[int]) -> List[List[int]]:

        ret = []
        used = [0] * len(nums)  # 记录各位置的使用情况
        nums_len = len(nums)

        def dfs(deep, tmp):  # deep: 递归深度
            if deep == nums_len:  # len(tmp) == nums_len 也可以，省一个变量
                ret.append(tmp[:])
                return

            for i in range(nums_len):
                if used[i]: continue
                
                used[i] = 1
                tmp.append(nums[i])
                dfs(deep + 1, tmp)
                tmp.pop()
                used[i] = 0
            
        dfs(0, [])
        return ret
```

</details>

<summary><b>思路 2：下一个排列</b></summary>

- 先排序，然后判断是否存在下一个排列，进而得到全部排列；
- 代码略；

<summary><b>相关问题</b></summary>

- [47. 全排列 II - 力扣（LeetCode）](https://leetcode.cn/problems/permutations-ii/)
    > 存在重复数字
