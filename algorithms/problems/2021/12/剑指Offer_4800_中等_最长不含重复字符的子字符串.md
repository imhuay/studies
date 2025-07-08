## 最长不含重复字符的子字符串
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2022-10-14%2014%3A59%3A33&color=yellowgreen&style=flat-square)
[![](https://img.shields.io/static/v1?label=&message=%E4%B8%AD%E7%AD%89&color=yellow&style=flat-square)](../../../README.md#中等)
[![](https://img.shields.io/static/v1?label=&message=%E5%89%91%E6%8C%87Offer&color=green&style=flat-square)](../../../README.md#剑指offer)
[![](https://img.shields.io/static/v1?label=&message=%E5%93%88%E5%B8%8C%E8%A1%A8%28Hash%29&color=blue&style=flat-square)](../../../README.md#哈希表hash)
[![](https://img.shields.io/static/v1?label=&message=%E5%8F%8C%E6%8C%87%E9%92%88&color=blue&style=flat-square)](../../../README.md#双指针)
[![](https://img.shields.io/static/v1?label=&message=%E5%8A%A8%E6%80%81%E8%A7%84%E5%88%92&color=blue&style=flat-square)](../../../README.md#动态规划)

<!--END_SECTION:badge-->
<!--info
tags: [哈希表, 双指针, 动态规划]
source: 剑指Offer
level: 中等
number: '4800'
name: 最长不含重复字符的子字符串
companies: []
-->

<summary><b>问题简述</b></summary>

```txt
求字符串 s 中的最长不重复子串，返回其长度；
```

<details><summary><b>详细描述</b></summary>

```txt
请从字符串中找出一个最长的不包含重复字符的子字符串，计算该最长子字符串的长度。

示例 1:
    输入: "abcabcbb"
    输出: 3 
    解释: 因为无重复字符的最长子串是 "abc"，所以其长度为 3。
示例 2:
    输入: "bbbbb"
    输出: 1
    解释: 因为无重复字符的最长子串是 "b"，所以其长度为 1。
示例 3:
    输入: "pwwkew"
    输出: 3
    解释: 因为无重复字符的最长子串是 "wke"，所以其长度为 3。
        请注意，你的答案必须是 子串 的长度，"pwke" 是一个子序列，不是子串。
 
提示：
    s.length <= 40000

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/zui-chang-bu-han-zhong-fu-zi-fu-de-zi-zi-fu-chuan-lcof
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```

</details>

<!-- <div align="center"><img src="../../../_assets/xxx.png" height="300" /></div> -->

<summary><b>思路1：双指针（推荐）</b></summary>

- 双指针同向遍历每个字符；同时使用哈希表记录每个字符的最新位置；
- 如果右指针遇到已经出现过的字符，则将左指针移动到该字符的位置，更新最大长度；
- 具体细节见代码；

<details><summary><b>Python</b></summary>

```python
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        if not s: return 0
        
        c2p = dict()
        lo = -1  # 左指针
        ret = 1
        for hi, c in enumerate(s):  # 遍历右指针
            if c not in c2p or c2p[c] < lo:  # 如果当前字符还没有出现过，或者出现过但是在左指针的左侧，可以更新最大长度
                ret = max(ret, hi - lo)
            else:  # 否则更新左指针
                lo = c2p[c]

            c2p[c] = hi  # 更新字符最新位置

        return ret
```

</details>


<summary><b>思路2：动态规划</b></summary>

> [最长不含重复字符的子字符串（动态规划 / 双指针 + 哈希表，清晰图解）](https://

**状态定义**
leetcode-cn.com/problems/zui-chang-bu-han-zhong-fu-zi-fu-de-zi-zi-fu-chuan-lcof/solution/mian-shi-ti-48-zui-chang-bu-han-zhong-fu-zi-fu-d-9/)
- 记 `dp[i] := 以第 i 个字符为结尾的不含重复字符的子串的最大长度`；

**转移方程**
```
dp[i] = dp[i-1] + 1     if dp[i-1] < i-i
      = i-j             else

其中 j 表示字符 s[i] 上一次出现的位置；
```

- 使用一个 hash 表记录每个字符上一次出现的位置；
- 因为当前状态只与上一个状态有关，因此可以使用一个变量代替数组（滚动）；

**初始状态**
- `dp[0] = 1`

<!-- <div align="center"><img src="../../../_assets/剑指Offer_0048_中等_最长不含重复字符的子字符串.png" height="300" /></div> -->

<details><summary><b>Python</b></summary>

```python
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        idx = dict()
        ret = dp = 0
        for i, c in enumerate(s):
            if c not in idx:
                dp = dp + 1
            else:
                j = idx[c]  # 如果 c 已经出现过，获取其上一个出现的位置
                if dp < i - j:  # 参考双指针思路，这里相当于上一次出现的位置在左指针之前，不影响更新长度
                    dp = dp + 1
                else:  # 反之，在左指针之后
                    dp = i - j

            idx[c] = i  # 更新位置 i
            ret = max(ret, dp)  # 更新最大长度
        return ret
```

</details>

