## 全排列II
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2025-07-08%2016%3A53%3A13&color=yellowgreen&style=flat-square)
[![](https://img.shields.io/static/v1?label=&message=%E4%B8%AD%E7%AD%89&color=yellow&style=flat-square)](../../../README.md#中等)
[![](https://img.shields.io/static/v1?label=&message=LeetCode&color=green&style=flat-square)](../../../README.md#leetcode)
[![](https://img.shields.io/static/v1?label=&message=%E9%80%92%E5%BD%92&color=blue&style=flat-square)](../../../README.md#递归)
[![](https://img.shields.io/static/v1?label=&message=LeetCode%20Hot%20100&color=blue&style=flat-square)](../../../README.md#leetcode-hot-100)
[![](https://img.shields.io/static/v1?label=&message=%E7%83%AD%E9%97%A8&color=blue&style=flat-square)](../../../README.md#热门)

<!--END_SECTION:badge-->
<!--info
tags: [递归, 回溯, lc100, 热门]
source: LeetCode
level: 中等
number: '0047'
name: 全排列II
companies: []
-->

> [47. 全排列 II - 力扣（LeetCode）](https://leetcode.cn/problems/permutations-ii/)

<summary><b>问题简述</b></summary>

```txt
给定一个可包含重复数字的序列 nums ，按任意顺序 返回所有不重复的全排列。
```

<!-- 
<details><summary><b>详细描述</b></summary>

```txt
```

</details>
-->

<!-- <div align="center"><img src="../../../_assets/xxx.png" height="300" /></div> -->

<summary><b>思路</b></summary>

- 递归回溯的关键问题是，在生成递归树的过程中，每个节点应该生成哪些分支；
- 相比无重复的全排列，需要额外考虑一个去重的剪枝过程，这里提供了写法1 和写法2 两种剪枝方法；
  - 写法 1 是最常见的写法，解释成本低；
  - 如果画出递归树的生成过程，那么写法2 更直观的；

<details><summary><b>Python 写法1（推荐）</b></summary>

- 本写法中核心的去重剪枝有两种写法：
    ```python
    # 写法1（推荐）
    if i > 0 and nums[i] == nums[i - 1] and not used[i - i]:
        continue
  
    # 写法2，区别仅在于 used[i - i]
    if i > 0 and nums[i] == nums[i - 1] and used[i - i]:
        continue
    ```
  写法1 的效率更高，关于这两种写法的实际含义，详见：[47. 全排列 II - 「代码随想录」](https://leetcode.cn/problems/permutations-ii/solution/dai-ma-sui-xiang-lu-dai-ni-xue-tou-hui-s-ki1h/)

```python
class Solution:
    def permuteUnique(self, nums: List[int]) -> List[List[int]]:
        
        nums.sort()  # 先排序，剪枝需要
        len_nums = len(nums)
        ret = []
        used = [0] * len_nums

        def dfs(deep, tmp):
            if deep == len_nums:
                ret.append(tmp[:])
                return
            
            for i in range(len_nums):
                if used[i]: continue
                # 相比无重复的全排列，多了这一步剪枝过程，该剪枝过程依赖于 nums 有序
                if i > 0 and nums[i] == nums[i - 1] and not used[i - i]:
                    continue
                
                used[i] = 1
                tmp.append(nums[i])
                dfs(deep + 1, tmp)
                tmp.pop()
                used[i] = 0
        
        dfs(0, [])
        return ret
```

</details>

<details><summary><b>Python 写法2（直观）</b></summary>

- 在递归树的每一层中，维护一个集合，记录已经使用过的数字；
- 该方法不需要预先排序；

```python
class Solution:
    def permuteUnique(self, nums: List[int]) -> List[List[int]]:
        
        # nums.sort()  # 先排序，剪枝需要
        len_nums = len(nums)
        ret = []
        used = [0] * len_nums

        def dfs(deep, tmp):
            if deep == len_nums:
                ret.append(tmp[:])
                return
            
            book = set()  # 该变量在递归树的每一层共享，记录在这一层中已经用过了哪些数字
            for i in range(len_nums):
                if used[i] or nums[i] in book: continue
                book.add(nums[i])
                
                used[i] = 1
                tmp.append(nums[i])
                dfs(deep + 1, tmp)
                tmp.pop()
                used[i] = 0
        
        dfs(0, [])
        return ret
```

</details>

<summary><b>相关问题</b></summary>

- [46. 全排列 - 力扣（LeetCode）](https://leetcode.cn/problems/permutations/)
