## 数字序列中某一位的数字
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2022-10-14%2014%3A59%3A33&color=yellowgreen&style=flat-square)
[![](https://img.shields.io/static/v1?label=&message=%E4%B8%AD%E7%AD%89&color=yellow&style=flat-square)](../../../README.md#中等)
[![](https://img.shields.io/static/v1?label=&message=%E5%89%91%E6%8C%87Offer&color=green&style=flat-square)](../../../README.md#剑指offer)
[![](https://img.shields.io/static/v1?label=&message=%E6%89%BE%E8%A7%84%E5%BE%8B&color=blue&style=flat-square)](../../../README.md#找规律)

<!--END_SECTION:badge-->
<!--info
tags: [找规律]
source: 剑指Offer
level: 中等
number: '4400'
name: 数字序列中某一位的数字
companies: []
-->

<summary><b>问题简述</b></summary>

> [剑指 Offer 44. 数字序列中某一位的数字 - 力扣（LeetCode）](https://leetcode-cn.com/problems/shu-zi-xu-lie-zhong-mou-yi-wei-de-shu-zi-lcof/)

```txt
数字以0123456789101112131415…的格式序列化到一个字符序列中，求任意第n位对应的数字。
```

<details><summary><b>详细描述</b></summary>

```txt
数字以0123456789101112131415…的格式序列化到一个字符序列中。在这个序列中，第5位（从下标0开始计数）是5，第13位是1，第19位是4，等等。

请写一个函数，求任意第n位对应的数字。

示例 1：
    输入：n = 3
    输出：3
示例 2：
    输入：n = 11
    输出：0
 
限制：
    0 <= n < 2^31

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/shu-zi-xu-lie-zhong-mou-yi-wei-de-shu-zi-lcof
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```

<!-- <div align="center"><img src="../../../_assets/xxx.png" height="300" /></div> -->

</details>


<summary><b>思路：找规律</b></summary>

<div align="center"><img src="../../../_assets/剑指Offer_0044_中等_数字序列中某一位的数字.png" height="300" /></div>

> [数字序列中某一位的数字（迭代 + 求整 / 求余，清晰图解）](https://leetcode-cn.com/problems/shu-zi-xu-lie-zhong-mou-yi-wei-de-shu-zi-lcof/solution/mian-shi-ti-44-shu-zi-xu-lie-zhong-mou-yi-wei-de-6/)


<details><summary><b>Python：迭代+求整/求余</b></summary>

> [数字序列中某一位的数字（迭代 + 求整 / 求余，清晰图解）](https://leetcode-cn.com/problems/shu-zi-xu-lie-zhong-mou-yi-wei-de-shu-zi-lcof/solution/mian-shi-ti-44-shu-zi-xu-lie-zhong-mou-yi-wei-de-6/)

```python
class Solution:
    def findNthDigit(self, n: int) -> int:
        digit, start, cnt = 1, 1, 9
        
        while n > cnt:  # 1. 计算所属区间，如 1~9、10~99、100~999、... 等
            n -= cnt
            start *= 10
            digit += 1
            cnt = 9 * start * digit
        
        num = start + (n - 1) // digit  # 2. 计算属于区间中的哪个数字
        idx = (n - 1) % digit  # 3. 计算在该数字的第几位
        return int(str(num)[idx])  # 4. 返回结果

```

</details>

