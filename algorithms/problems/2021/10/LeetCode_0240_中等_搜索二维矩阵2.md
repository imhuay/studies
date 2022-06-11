## LeetCode_0240_搜索二维矩阵2（中等, 2021-10）
<!--{
    "tags": ["二分查找"],
    "来源": "LeetCode",
    "编号": "0240",
    "难度": "中等",
    "标题": "搜索二维矩阵2"
}-->

<summary><b>问题简述</b></summary>

```txt
编写一个高效的算法来搜索 m x n 矩阵 matrix 中的一个目标值 target。
该矩阵具有以下特性：
    每行的元素从左到右升序排列。
    每列的元素从上到下升序排列。
```

<details><summary><b>详细描述</b></summary>

```txt
编写一个高效的算法来搜索 m x n 矩阵 matrix 中的一个目标值 target 。该矩阵具有以下特性：

    每行的元素从左到右升序排列。
    每列的元素从上到下升序排列。

示例 1：
    输入：matrix = [[1,4,7,11,15],[2,5,8,12,19],[3,6,9,16,22],[10,13,14,17,24],[18,21,23,26,30]], target = 5
    输出：true
示例 2：
    输入：matrix = [[1,4,7,11,15],[2,5,8,12,19],[3,6,9,16,22],[10,13,14,17,24],[18,21,23,26,30]], target = 20
    输出：false

提示：
    m == matrix.length
    n == matrix[i].length
    1 <= n, m <= 300
    -10^9 <= matrix[i][j] <= 10^9
    每行的所有元素从左到右升序排列
    每列的所有元素从上到下升序排列
    -10^9 <= target <= 10^9

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/search-a-2d-matrix-ii
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```

<div align="center"><img src="../../../_assets/searchgrid2.jpeg" height="300" /></div> 

</details>


<summary><b>思路</b></summary>

<details><summary><b>法1）Python：二分查找</b></summary>

- 时间复杂度：`O(MlogN)`

```python
from bisect import bisect_left

# 直接层序二分搜索
class Solution:
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        for row in matrix:
            idx = bisect_left(row, target)  # 注意这里要用 bisect_left
            if idx < len(row) and row[idx] == target:
                return True
        return False


# 稍微做一些优化
class Solution:
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        m, n = len(matrix), len(matrix[0])
        if target < matrix[0][0] or target > matrix[m - 1][n - 1]:
            return False

        lo, hi = 0, n
        for row in matrix:
            idx = bisect_left(row, target, lo, hi)

            # 逐步缩小每层遍历的范围
            if idx < len(row):
                if row[idx] == target:
                    return True
                elif row[idx] < target:
                    lo = idx
                elif row[idx] > target:
                    hi = idx

        return False
```

</details>


<details><summary><b>法2）Python：模拟二分</b></summary>

- **二分搜索的核心**是将搜索区域分成两个部分，且这两个部分具有相反的性质，每次可以排除一半左右搜索区域；
- 对本题来说，如果从**右上角**开始遍历，则有：所有左边的值都比当前值小，所有下方的值都比当前值大；
- 时间复杂度：`O(M+N)`

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