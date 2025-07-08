## 组合总和II
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2022-10-14%2014%3A59%3A33&color=yellowgreen&style=flat-square)
[![](https://img.shields.io/static/v1?label=&message=%E4%B8%AD%E7%AD%89&color=yellow&style=flat-square)](../../../README.md#中等)
[![](https://img.shields.io/static/v1?label=&message=LeetCode&color=green&style=flat-square)](../../../README.md#leetcode)
[![](https://img.shields.io/static/v1?label=&message=%E9%80%92%E5%BD%92&color=blue&style=flat-square)](../../../README.md#递归)
[![](https://img.shields.io/static/v1?label=&message=LeetCode%20Hot%20100&color=blue&style=flat-square)](../../../README.md#leetcode-hot-100)

<!--END_SECTION:badge-->
<!--info
tags: [递归, 回溯, lc100]
source: LeetCode
level: 中等
number: '0040'
name: 组合总和II
companies: []
-->

> [40. 组合总和 II - 力扣（LeetCode）](https://leetcode.cn/problems/combination-sum-ii/)

<summary><b>问题简述</b></summary>

```txt
给定一个候选人编号的集合 candidates 和一个目标数 target ，
找出 candidates 中所有可以使数字和为 target 的组合。
candidates 中的每个数字在每个组合中只能使用 一次 。
注意：解集不能包含重复的组合。 
```

<!-- 
<details><summary><b>详细描述</b></summary>

```txt
```

</details>
-->

<!-- <div align="center"><img src="../../../_assets/xxx.png" height="300" /></div> -->

<summary><b>思路</b></summary>

- 递归+回溯模板；
- 代码细节：
    - 每个数字只用一次；
    - 组合去重；

<details><summary><b>Python</b></summary>

```python
class Solution:
    def combinationSum2(self, candidates: List[int], target: int) -> List[List[int]]:

        ret = []

        def dfs(s, start, tmp):

            if s >= target:
                if s == target:
                    ret.append(tmp[:])
                return
            
            for i in range(start, len(candidates)):
                # 注意这里是 i > start（每个数字取一次），而不是 i > 0（每种数字取一次）
                if i > start and candidates[i] == candidates[i - 1]:
                    continue

                tmp.append(candidates[i])
                dfs(s + candidates[i], i + 1, tmp)  # i + 1 表示下一个开始取，即每个数字只使用一次
                tmp.pop()

        candidates.sort()  # 排序
        dfs(0, 0, [])
        return ret
```

</details>


<summary><b>相关问题</b></summary>

- [39. 组合总和 - 力扣（LeetCode）](https://leetcode.cn/problems/combination-sum/)
