## LeetCode_0859_亲密字符串（简单, 2021-11）
<!--{
    "tags": ["模拟", "字符串"],
    "来源": "LeetCode",
    "编号": "0859",
    "难度": "简单",
    "标题": "亲密字符串"
}-->

<summary><b>问题简述</b></summary>

```txt
给你两个字符串 s 和 goal ，只要我们可以通过交换 s 中的两个字母得到与 goal 相等的结果，就返回 true ；否则返回 false。

例如，在 "abcd" 中交换下标 0 和下标 2 的元素可以生成 "cbad" 。
```

<details><summary><b>详细描述</b></summary>

```txt
给你两个字符串 s 和 goal ，只要我们可以通过交换 s 中的两个字母得到与 goal 相等的结果，就返回 true ；否则返回 false 。

交换字母的定义是：取两个下标 i 和 j （下标从 0 开始）且满足 i != j ，接着交换 s[i] 和 s[j] 处的字符。

例如，在 "abcd" 中交换下标 0 和下标 2 的元素可以生成 "cbad" 。
 

示例 1：
    输入：s = "ab", goal = "ba"
    输出：true
    解释：你可以交换 s[0] = 'a' 和 s[1] = 'b' 生成 "ba"，此时 s 和 goal 相等。
示例 2：
    输入：s = "ab", goal = "ab"
    输出：false
    解释：你只能交换 s[0] = 'a' 和 s[1] = 'b' 生成 "ba"，此时 s 和 goal 不相等。
示例 3：
    输入：s = "aa", goal = "aa"
    输出：true
    解释：你可以交换 s[0] = 'a' 和 s[1] = 'a' 生成 "aa"，此时 s 和 goal 相等。
示例 4：
    输入：s = "aaaaaaabc", goal = "aaaaaaacb"
    输出：true
 

提示：
    1 <= s.length, goal.length <= 2 * 10^4
    s 和 goal 由小写英文字母组成

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/buddy-strings
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```

<!-- <div align="center"><img src="../../../_assets/xxx.png" height="300" /></div> -->

</details>



<summary><b>思路：分情况讨论</b></summary>

- 当 `len(s) != len(goal)` 时：False
- 当 `len(s) == len(goal)` 时：
    - 当 `s != goal` 时：当且仅当不同的字符数量等于 2，且交换后满足条件；
    - 当 `s == goal` 时：`s` 中存在出现至少 2 次的字符；

- `s == goal` 的情况比较容易被忽略；


<details><summary><b>Python：模拟</b></summary>

```python
class Solution:

    def buddyStrings(self, s: str, goal: str) -> bool:
        """"""
        if len(s) != len(goal):
            return False

        dif = []
        cs = set()
        for i, c in enumerate(s):
            cs.add(c)
            if s[i] != goal[i]:
                dif.append(i)

        # 存在字符出现过 2 次
        if s == goal and len(cs) < len(s):
            return True

        # 只存在两个位置字符不同，且交换后满足条件
        if len(dif) == 2 and (s[dif[0]], s[dif[1]]) == (goal[dif[1]], goal[dif[0]]):
            return True

        return False
```

</details>

