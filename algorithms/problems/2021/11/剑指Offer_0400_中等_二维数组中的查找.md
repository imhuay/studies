## 剑指Offer_0400_二维数组中的查找（中等, 2021-11）
<!--{
    "tags": ["二分查找"],
    "来源": "剑指Offer",
    "编号": "0400",
    "难度": "中等",
    "标题": "二维数组中的查找"
}-->

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

