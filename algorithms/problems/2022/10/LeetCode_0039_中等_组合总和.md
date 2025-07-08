## 组合总和
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2022-10-14%2014%3A59%3A33&color=yellowgreen&style=flat-square)
[![](https://img.shields.io/static/v1?label=&message=%E4%B8%AD%E7%AD%89&color=yellow&style=flat-square)](../../../README.md#中等)
[![](https://img.shields.io/static/v1?label=&message=LeetCode&color=green&style=flat-square)](../../../README.md#leetcode)
[![](https://img.shields.io/static/v1?label=&message=%E6%B7%B1%E5%BA%A6%E4%BC%98%E5%85%88%E6%90%9C%E7%B4%A2&color=blue&style=flat-square)](../../../README.md#深度优先搜索)
[![](https://img.shields.io/static/v1?label=&message=%E9%80%92%E5%BD%92&color=blue&style=flat-square)](../../../README.md#递归)
[![](https://img.shields.io/static/v1?label=&message=LeetCode%20Hot%20100&color=blue&style=flat-square)](../../../README.md#leetcode-hot-100)

<!--END_SECTION:badge-->
<!--info
tags: [dfs, 回溯, lc100]
source: LeetCode
level: 中等
number: '0039'
name: 组合总和
companies: []
-->

> 

<summary><b>问题简述</b></summary>

```txt
给你一个 无重复元素 的整数数组 candidates 和一个目标整数 target，
找出 candidates 中可以使数字和为目标数 target 的 所有 不同组合，
并以列表形式返回。你可以按 任意顺序 返回这些组合。

candidates 中的 同一个 数字可以 无限制重复被选取。
如果至少一个数字的被选数量不同，则两种组合是不同的。
```

<!-- 
<details><summary><b>详细描述</b></summary>

```txt
```

</details>
-->

<!-- <div align="center"><img src="../../../_assets/xxx.png" height="300" /></div> -->

<summary><b>思路：递归回溯</b></summary>

<details><summary><b>Python：写法1（标准写法，推荐）</b></summary>

```python
class Solution:
    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:

        ret = []

        def dfs(s, start, tmp):
            if s >= target:
                if s == target:
                    ret.append(tmp[:])
                return

            for i in range(start, len(candidates)):
                c = candidates[i]
                tmp.append(c)
                dfs(s + c, i, tmp)  
                # 这里传入 i 表示从 candidates 第 i 个开始取，因此可以重复
                # 组合总和II 中不能重复取，相应的要传入 i+1
                tmp.pop()

        dfs(0, 0, [])
        return ret
```

</details>

<details><summary><b>Python：写法2（好记）</b></summary>

- 本写法不保证在其他相关问题上适用；

```python
class Solution:
    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:
        
        ret = []

        def dfs(s, tmp):
            if s >= target:
                if s == target:
                    ret.append(tmp[:])
                return
            
            for c in candidates:
                if tmp and c < tmp[-1]:  # 保证 tmp 内部有序来达到去重的目的
                    continue
                tmp.append(c)
                dfs(s + c, tmp)
                tmp.pop()
        
        dfs(0, [])
        return ret
```

</details>


<summary><b>相关问题</b></summary>

- [40. 组合总和 II - 力扣（LeetCode）](https://leetcode.cn/problems/combination-sum-ii/)
