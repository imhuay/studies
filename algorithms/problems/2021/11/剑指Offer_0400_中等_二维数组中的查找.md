## 二维数组中的查找
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2025-07-08%2016%3A53%3A13&color=yellowgreen&style=flat-square)
[![](https://img.shields.io/static/v1?label=&message=%E4%B8%AD%E7%AD%89&color=yellow&style=flat-square)](../../../README.md#中等)
[![](https://img.shields.io/static/v1?label=&message=%E5%89%91%E6%8C%87Offer&color=green&style=flat-square)](../../../README.md#剑指offer)
[![](https://img.shields.io/static/v1?label=&message=%E4%BA%8C%E5%88%86%E6%9F%A5%E6%89%BE&color=blue&style=flat-square)](../../../README.md#二分查找)

<!--END_SECTION:badge-->
<!--info
tags: [二分查找]
source: 剑指Offer
level: 中等
number: '0400'
name: 二维数组中的查找
companies: []
-->

<summary><b>问题简述</b></summary>

```txt
一个 n * m 的二维数组，每一行从左到右递增，每一列从上到下递增。
输入一个整数，判断该数组中是否含有该整数。
```

<details><summary><b>详细描述</b></summary>

```txt
在一个 n * m 的二维数组中，每一行都按照从左到右递增的顺序排序，每一列都按照从上到下递增的顺序排序。请完成一个高效的函数，输入这样的一个二维数组和一个整数，判断数组中是否含有该整数。

示例:
    现有矩阵 matrix 如下：
    [
    [1,   4,  7, 11, 15],
    [2,   5,  8, 12, 19],
    [3,   6,  9, 16, 22],
    [10, 13, 14, 17, 24],
    [18, 21, 23, 26, 30]
    ]
    给定 target = 5，返回 true。
    给定 target = 20，返回 false。

限制：
    0 <= n <= 1000
    0 <= m <= 1000

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/er-wei-shu-zu-zhong-de-cha-zhao-lcof
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```

<!-- <div align="center"><img src="../../../_assets/xxx.png" height="300" /></div> -->

</details>


<summary><b>思路</b></summary>

- 法1）对每一行做二分查找，时间复杂度`O(N*logM)`
- 法2）模拟二分，从左下角开始查找，打标目标值往右，小于目标值往上；


<details><summary><b>Python：模拟二分</b></summary>

```python
class Solution:
    def findNumberIn2DArray(self, matrix: List[List[int]], target: int) -> bool:
        if len(matrix) < 1:
            return False

        n, m = len(matrix), len(matrix[0])
        i, j = n - 1, 0

        while i >= 0 and j <= m - 1:
            if matrix[i][j] == target:
                return True
            elif matrix[i][j] > target:
                i -= 1
            else:  # matrix[i][j] < target:
                j += 1

        return False
```

</details>

