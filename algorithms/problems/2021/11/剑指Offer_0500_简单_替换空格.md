## 剑指Offer_0500_替换空格（简单, 2021-11）
<!--{
    "tags": ["字符串"],
    "来源": "剑指Offer",
    "编号": "0500",
    "难度": "简单",
    "标题": "替换空格"
}-->

<summary><b>问题简述</b></summary>

```txt
实现一个函数，把字符串 s 中的每个空格替换成"%20"。
```

<details><summary><b>详细描述</b></summary>

```txt
请实现一个函数，把字符串 s 中的每个空格替换成"%20"。

示例 1：
    输入：s = "We are happy."
    输出："We%20are%20happy."

限制：
    0 <= s 的长度 <= 10000

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/ti-huan-kong-ge-lcof
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```

<!-- <div align="center"><img src="../../../_assets/xxx.png" height="300" /></div> -->

</details>


<summary><b>思路</b></summary>

- Python、Java 中的字符串都是不可变类型，所以始终要申请新的容器；那么问题就很简单，替换拼接即可；
- C++ 中 string 是可变类型，因此可以尝试原地替换；


<details><summary><b>Python</b></summary>

```python
class Solution:
    def replaceSpace(self, s: str) -> str:
        buf = []
        for c in s:
            if c == ' ':
                buf.append('%20')
            else:
                buf.append(c)
        
        return ''.join(buf)
```

</details>

<details><summary><b>C++：原地替换</b></summary>

```cpp
class Solution {
public:
    string replaceSpace(string s) {
        // 统计空格数量
        int space_cnt = 0;
        for (char c : s) {
            if (c == ' ') space_cnt++;
        }
        // 修改 s 长度
        int i = s.size() - 1;  // 原来的长度
        s.resize(s.size() + 2 * space_cnt);        
        int j = s.size() - 1;  // 新的长度
        // 倒序遍历修改
        while (i < j) {
            if (s[i] != ' ')
                s[j] = s[i];
            else {
                s[j - 2] = '%';
                s[j - 1] = '2';
                s[j] = '0';
                j -= 2;
            }
            i--;
            j--;
        }
        return s;
    }
};
```

</details>

