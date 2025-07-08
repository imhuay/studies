## 左旋转字符串
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2022-10-14%2014%3A59%3A33&color=yellowgreen&style=flat-square)
[![](https://img.shields.io/static/v1?label=&message=%E7%AE%80%E5%8D%95&color=yellow&style=flat-square)](../../../README.md#简单)
[![](https://img.shields.io/static/v1?label=&message=%E5%89%91%E6%8C%87Offer&color=green&style=flat-square)](../../../README.md#剑指offer)
[![](https://img.shields.io/static/v1?label=&message=%E5%AD%97%E7%AC%A6%E4%B8%B2&color=blue&style=flat-square)](../../../README.md#字符串)

<!--END_SECTION:badge-->
<!--info
tags: [字符串]
source: 剑指Offer
level: 简单
number: '5802'
name: 左旋转字符串
companies: []
-->

<summary><b>问题简述</b></summary>

```txt
把字符串前面的 n 个字符转移到字符串的尾部。
```

<details><summary><b>详细描述</b></summary>

```txt
字符串的左旋转操作是把字符串前面的若干个字符转移到字符串的尾部。请定义一个函数实现字符串左旋转操作的功能。比如，输入字符串"abcdefg"和数字2，该函数将返回左旋转两位得到的结果"cdefgab"。

示例 1：
    输入: s = "abcdefg", k = 2
    输出: "cdefgab"
示例 2：
    输入: s = "lrloseumgh", k = 6
    输出: "umghlrlose"

限制：
    1 <= k < s.length <= 10000

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/zuo-xuan-zhuan-zi-fu-chuan-lcof
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```

</details>

<!-- <div align="center"><img src="../../../_assets/xxx.png" height="300" /></div> -->

<summary><b>思路</b></summary>

> [左旋转字符串（切片 / 列表 / 字符串，清晰图解）](https://leetcode-cn.com/problems/zuo-xuan-zhuan-zi-fu-chuan-lcof/solution/mian-shi-ti-58-ii-zuo-xuan-zhuan-zi-fu-chuan-qie-p/)

<details><summary><b>Python</b></summary>

```python
class Solution:
    def reverseLeftWords(self, s: str, n: int) -> str:

        # 法1：切片（速度最快）
        def f1():
            return s[n:] + s[:n]
        
        # 法2：列表（面试推荐写法）
        def f2():
            ret = []
            # for i in range(n, len(s)):
            #     ret.append(s[i])
            # for i in range(n):
            #     ret.append(s[i])

            # 使用求余操作简化上述循环
            for i in range(len(s)):
                ret.append(s[(n + i) % len(s)])

            return ''.join(ret)
        
        return f2()

```

</details>

