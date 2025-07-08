## 搜索二维矩阵 II
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2023-07-17%2004%3A19%3A17&color=yellowgreen&style=flat-square)
[![](https://img.shields.io/static/v1?label=&message=%E4%B8%AD%E7%AD%89&color=yellow&style=flat-square)](../../../README.md#中等)
[![](https://img.shields.io/static/v1?label=&message=LeetCode&color=green&style=flat-square)](../../../README.md#leetcode)
[![](https://img.shields.io/static/v1?label=&message=%E4%BA%8C%E5%88%86%E6%9F%A5%E6%89%BE&color=blue&style=flat-square)](../../../README.md#二分查找)
[![](https://img.shields.io/static/v1?label=&message=%E7%83%AD%E9%97%A8&color=blue&style=flat-square)](../../../README.md#热门)

<!--END_SECTION:badge-->
<!--info
tags: [二分查找, 热门]
source: LeetCode
level: 中等
number: '0240'
name: 搜索二维矩阵 II
companies: [Shopee]
-->

> [240. 搜索二维矩阵 II - 力扣（LeetCode）](https://leetcode.cn/problems/search-a-2d-matrix-ii/)

<summary><b>问题简述</b></summary>

```txt
编写一个高效的算法来搜索 m x n 矩阵 matrix 中的一个目标值 target。
该矩阵具有以下特性：
    每行的元素从左到右升序排列。
    每列的元素从上到下升序排列。
```

<div align="center"><img src="../../../_assets/searchgrid2.jpeg" height="200" /></div> 


<summary><b>思路</b></summary>

- **二分查找的核心**是将搜索区域分成两个部分，且这两个部分具有相反的性质，每次可以排除一半左右搜索区域；
- 对本题来说，从**右上角**开始遍历，则所有左边的值都比当前值小，所有下方的值都比当前值大；每次可以排除一半区域;
- 时间复杂度：`O(M+N)`

<details><summary><b>Python</b></summary>

```python
class Solution:
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        m, n = len(matrix), len(matrix[0])
        i, j = 0, n - 1
        while i < m and j >= 0:
            if matrix[i][j] == target:
                return True
            elif matrix[i][j] > target:  # 比当前值大，横向往左进一格
                j -= 1
            else:  # matrix[i][j] < target 比当前值小，纵向往下进一格
                i += 1
        return False
```

</details>