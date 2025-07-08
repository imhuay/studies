## 重复的DNA序列
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2025-07-08%2016%3A53%3A13&color=yellowgreen&style=flat-square)
[![](https://img.shields.io/static/v1?label=&message=%E4%B8%AD%E7%AD%89&color=yellow&style=flat-square)](../../../README.md#中等)
[![](https://img.shields.io/static/v1?label=&message=LeetCode&color=green&style=flat-square)](../../../README.md#leetcode)
[![](https://img.shields.io/static/v1?label=&message=%E5%93%88%E5%B8%8C%E8%A1%A8%28Hash%29&color=blue&style=flat-square)](../../../README.md#哈希表hash)
[![](https://img.shields.io/static/v1?label=&message=%E4%BD%8D%E8%BF%90%E7%AE%97&color=blue&style=flat-square)](../../../README.md#位运算)

<!--END_SECTION:badge-->
<!--info
tags: [哈希表, 位运算]
source: LeetCode
level: 中等
number: '0187'
name: 重复的DNA序列
companies: []
-->

<summary><b>问题简述</b></summary>

```txt
找出由 ATCG 构成的字符串中所有重复且长度为 10 的子串；
```

<details><summary><b>详细描述</b></summary>

```txt
所有 DNA 都由一系列缩写为 'A'，'C'，'G' 和 'T' 的核苷酸组成，例如："ACGAATTCCG"。在研究 DNA 时，识别 DNA 中的重复序列有时会对研究非常有帮助。

编写一个函数来找出所有目标子串，目标子串的长度为 10，且在 DNA 字符串 s 中出现次数超过一次。

示例 1：
    输入：s = "AAAAACCCCCAAAAACCCCCCAAAAAGGGTTT"
    输出：["AAAAACCCCC","CCCCCAAAAA"]
示例 2：
    输入：s = "AAAAAAAAAAAAA"
    输出：["AAAAAAAAAA"]

提示：
    0 <= s.length <= 10^5
    s[i] 为 'A'、'C'、'G' 或 'T'

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/repeated-dna-sequences
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```

</details>

<summary><b>思路</b></summary>

- 基本思路：哈希表计数；
- 如果直接使用子串本身作为哈希表的 key，那么时间复杂度和空间复杂度都是 `O(NL)`；而如果使用位运算+滑动窗口手动构造 key，可以把复杂度降为 `O(N)`；


<details><summary><b>子串作为 key</b></summary>

- 时间&空间复杂度：`O(NL)`；
```python
class Solution:
    def findRepeatedDnaSequences(self, s: str) -> List[str]:
        """"""
        # from collections import defaultdict
        L = 10

        cnt = defaultdict(int)
        ans = []
        for i in range(len(s) - L + 1):
            subs = s[i: i+L]
            cnt[subs] += 1
            if cnt[subs] == 2:
                ans.append(subs)

        return ans
```

</details>

<details><summary><b>位运算+滑动窗口</b></summary>

- 时间&空间复杂度：`O(N)`；
```python
class Solution:
    def findRepeatedDnaSequences(self, s: str) -> List[str]:
        """"""
        # from collections import defaultdict
        L = 10
        B = {'A': 0, 'T': 1, 'C': 2, 'G': 3}  # 分别为 00, 01, 10, 11

        if len(s) < L + 1:  # assert，否则部分用例会无法通过
            return []

        # 先计算前 9 位的值
        x = 0
        for i in range(L - 1):
            b = B[s[i]]
            x = (x << 2) | b

        ans = []
        cnt = defaultdict(int)
        for i in range(len(s) - L + 1):
            b = B[s[i + L - 1]]
            # 注意该有的括号不要少，避免运算优先级混乱
            x = ((x << 2) | b) & ((1 << (L * 2)) - 1)  # 滑动计算子串的 hash 值
            cnt[x] += 1
            if cnt[x] == 2:
                ans.append(s[i: i + L])

        return ans
```

</details>


<details><summary><b>位运算说明</b></summary>

- `(x << 2) | b`：
    ```python
    # 以为均为二进制表示
    设 x = 0010 1011, b = 10: 
    该运算相当于把 b “拼” 到 x 末尾

    x         :   0010 1011
    x = x << 2:   1010 1100
    
    x = x | b :   1010 1100
                | 0000 0010
                -----------
                  1010 1110
    ```
- `x & ((1 << (L * 2)) - 1)`
    ```python
    # 该运算把 x 除低 10 位前的所有位置置 0
    设 L = 5，x = 1110 1010 1010: 
    
    y = 1 << (L * 2):   0100 0000 0000
    y = y - 1       :   0011 1111 1111

    x = x & y       :   1110 1010 1010
                      & 0011 1111 1111
                      ----------------
                        0010 1010 1010

    ```

</details>

