## 矩阵中的路径
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2025-07-08%2016%3A53%3A13&color=yellowgreen&style=flat-square)
[![](https://img.shields.io/static/v1?label=&message=%E4%B8%AD%E7%AD%89&color=yellow&style=flat-square)](../../../README.md#中等)
[![](https://img.shields.io/static/v1?label=&message=%E5%89%91%E6%8C%87Offer&color=green&style=flat-square)](../../../README.md#剑指offer)
[![](https://img.shields.io/static/v1?label=&message=%E6%B7%B1%E5%BA%A6%E4%BC%98%E5%85%88%E6%90%9C%E7%B4%A2&color=blue&style=flat-square)](../../../README.md#深度优先搜索)

<!--END_SECTION:badge-->
<!--info
tags: [DFS, DFS+回溯]
source: 剑指Offer
level: 中等
number: '1200'
name: 矩阵中的路径
companies: []
-->

<summary><b>问题简述</b></summary>

```txt
给定一个 m x n 二维字符矩阵 board 和字符串 word。如果 word 存在于网格中，返回 true ；否则，返回 false 。

其中单词必须按照字母顺序，通过相邻的单元格内的字母构成，其中“相邻”单元格是那些水平相邻或垂直相邻的单元格。同一个单元格内的字母不允许被重复使用。
```

<details><summary><b>详细描述</b></summary>

```txt
给定一个 m x n 二维字符网格 board 和一个字符串单词 word 。如果 word 存在于网格中，返回 true ；否则，返回 false 。

单词必须按照字母顺序，通过相邻的单元格内的字母构成，其中“相邻”单元格是那些水平相邻或垂直相邻的单元格。同一个单元格内的字母不允许被重复使用。

例如，在下面的 3×4 的矩阵中包含单词 "ABCCED"（单词中的字母已标出）。

示例 1：
    输入：board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], word = "ABCCED"
    输出：true
示例 2：
    输入：board = [["a","b"],["c","d"]], word = "abcd"
    输出：false
 
提示：
    1 <= board.length <= 200
    1 <= board[i].length <= 200
    board 和 word 仅由大小写英文字母组成
 

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/ju-zhen-zhong-de-lu-jing-lcof
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```

<div align="center"><img src="../../../_assets/剑指Offer_0012_中等_矩阵中的路径-示例.jpeg" height="200" /></div>

</details>

<summary><b>思路</b></summary>

- 棋盘搜索，非常典型的 DFS + 回溯问题；

<!-- <div align="center"><img src="../../../_assets/xxx.png" height="300" /></div> -->

<details><summary><b>Python：DFS + 回溯</b></summary>

```python
class Solution:
    def exist(self, board: List[List[str]], word: str) -> bool:
        if len(board) < 1:
            return False

        m, n = len(board), len(board[0])

        # 使用内部函数，可以减少一些参数的传递，同时比成员方法更简洁
        def dfs(i, j, k):  # i, j, k 分别表示 board[i][j] 和 word[k]
            if not 0 <= i < m or not 0 <= j < n:  # 先判断是否越界
                return False

            if board[i][j] != word[k]:  # 这一步可以合并到越界判断，但会损失一些可读性，故分离出来单独判断
                return False
            else:  # board[i][j] == word[k]:  # 如果当前位置字符相同，继续深度搜索
                if k == len(word) - 1:  # 如果字符已经全部匹配成功，返回 True
                    return True

                # 置空，表示该位置已访问过；一些代码中会使用一个新的矩阵记录位置是否访问，这里直接在原矩阵上标记
                board[i][j] = ''
                # 继续遍历 4 个方向
                flag = dfs(i + 1, j, k + 1) or dfs(i - 1, j, k + 1) or dfs(i, j + 1, k + 1) or dfs(i, j - 1, k + 1)
                # 这一步是容易忽略的：因为需要回溯，所以必须还原该位置的元素
                board[i][j] = word[k]

                return flag

        # board 中每一个位置都可能是起始位置，所以要循环遍历
        for i in range(m):
            for j in range(n):
                if dfs(i, j, 0):
                    return True
        return False
```

</details>

