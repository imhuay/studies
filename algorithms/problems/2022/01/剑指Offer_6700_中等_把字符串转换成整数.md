## 把字符串转换成整数
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2025-07-08%2016%3A53%3A13&color=yellowgreen&style=flat-square)
[![](https://img.shields.io/static/v1?label=&message=%E4%B8%AD%E7%AD%89&color=yellow&style=flat-square)](../../../README.md#中等)
[![](https://img.shields.io/static/v1?label=&message=%E5%89%91%E6%8C%87Offer&color=green&style=flat-square)](../../../README.md#剑指offer)
[![](https://img.shields.io/static/v1?label=&message=%E5%AD%97%E7%AC%A6%E4%B8%B2&color=blue&style=flat-square)](../../../README.md#字符串)
[![](https://img.shields.io/static/v1?label=&message=%E7%BB%8F%E5%85%B8&color=blue&style=flat-square)](../../../README.md#经典)
[![](https://img.shields.io/static/v1?label=&message=%E7%83%AD%E9%97%A8&color=blue&style=flat-square)](../../../README.md#热门)

<!--END_SECTION:badge-->
<!--info
tags: [字符串, 经典, 热门]
source: 剑指Offer
level: 中等
number: '6700'
name: 把字符串转换成整数
companies: []
-->

<summary><b>问题简述</b></summary>

```txt
写一个函数 strToInt(string s)，实现把字符串转换成整数这个功能。不能使用 atoi 或者其他类似的库函数。
```

<details><summary><b>详细描述</b></summary>

```txt
写一个函数 strToInt(string s)，实现把字符串转换成整数这个功能。不能使用 atoi 或者其他类似的库函数。

首先，该函数会根据需要丢弃无用的开头空格字符，直到寻找到第一个非空格的字符为止。

当我们寻找到的第一个非空字符为正或者负号时，则将该符号与之后面尽可能多的连续数字组合起来，作为该整数的正负号；假如第一个非空字符是数字，则直接将其与之后连续的数字字符组合起来，形成整数。

该字符串除了有效的整数部分之后也可能会存在多余的字符，这些字符可以被忽略，它们对于函数不应该造成影响。

注意：假如该字符串中的第一个非空格字符不是一个有效整数字符、字符串为空或字符串仅包含空白字符时，则你的函数不需要进行转换。

在任何情况下，若函数不能进行有效的转换时，请返回 0。

说明：
    假设我们的环境只能存储 32 位大小的有符号整数，那么其数值范围为 [−231,  231 − 1]。如果数值超过这个范围，请返回  INT_MAX (231 − 1) 或 INT_MIN (−231) 。

示例 1:
    输入: "42"
    输出: 42
示例 2:
    输入: "   -42"
    输出: -42
    解释: 第一个非空白字符为 '-', 它是一个负号。
         我们尽可能将负号与后面所有连续出现的数字组合起来，最后得到 -42 。
示例 3:
    输入: "4193 with words"
    输出: 4193
    解释: 转换截止于数字 '3' ，因为它的下一个字符不为数字。
示例 4:
    输入: "words and 987"
    输出: 0
    解释: 第一个非空字符是 'w', 但它不是数字或正、负号。
        因此无法执行有效的转换。
示例 5:
    输入: "-91283472332"
    输出: -2147483648
    解释: 数字 "-91283472332" 超过 32 位有符号整数范围。 
         因此返回 INT_MIN (−231) 。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/ba-zi-fu-chuan-zhuan-huan-cheng-zheng-shu-lcof
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```

<!-- <div align="center"><img src="./_assets/xxx.png" height="300" /></div> -->

</details>


<summary><b>思路</b></summary>

- 把字符串当做数组，依次遍历每个字符，根据题目要求执行每一步操作；
- 注意一些细节：如正负号、char 与 int 的互转、越界判断等，详见下方代码；
- PS：不同编程语言中字符串的实现细节；


<details><summary><b>C++</b></summary>

```cpp
class Solution {
public:
    int strToInt(string str) {
        int n = str.length();
        if (n < 1) return 0;
        
        int ret = 0;
        int p = 0;      // 模拟指针
        int sign = 1;   // 正负
        int s_max = INT_MAX / 10;
        
        while (isspace(str[p])) 
            p++;  // 跳过前置空格

        // c++ 的字符串末尾有一个特殊字符，因此不需要做越界判断
        // if (p == n) return 0;
        
        if (str[p] == '-') sign = -1;
        if (str[p] == '-' || str[p] == '+') p++;
        
        while (str[p] >= '0' && str[p] <= '9') {
            if (ret > s_max || (ret == s_max && str[p] > '7')) {  // 越界判断
                return sign > 0 ? INT_MAX : INT_MIN;
            }
            ret = ret * 10 + (str[p] - '0');  // str[p] - '0' 必须括起来，否则顺序计算时会溢出
            p++;
        }
        
        return sign * ret;
    }
};

```

</details>


<details><summary><b>Python</b></summary>

```python
class Solution:
    def strToInt(self, str: str) -> int:

        n = len(str)
        if n < 1: return 0

        INT_MAX = 2 ** 31 - 1
        INT_MIN = -2 ** 31

        ret = 0  # 保存结果
        sign = 1  # 记录符号
        p = 0  # 模拟指针

        # Python 字符串与 C++ 不同，时刻需要进行越界判断
        while p < n and str[p] == ' ':
            p += 1
        
        if p == n:  # 越界判断
            return ret
        
        if str[p] == '-':
            sign = -1
        if str[p] in ('-', '+'):
            p += 1
        
        while p < n and '0' <= str[p] <= '9':  # 注意越界判断
            ret = ret * 10 + int(str[p])
            p += 1
            if ret > INT_MAX:  # python 中不存在越界，因此直接跟 INT_MAX 比较即可
                return INT_MAX if sign == 1 else INT_MIN
        
        return ret * sign
```

</details>


<details><summary><b>Java</b></summary>

> [把字符串转换成整数（数字越界处理，清晰图解）](https://leetcode-cn.com/problems/ba-zi-fu-chuan-zhuan-huan-cheng-zheng-shu-lcof/solution/mian-shi-ti-67-ba-zi-fu-chuan-zhuan-huan-cheng-z-4/)

```java
class Solution {
    public int strToInt(String str) {
        int res = 0, bndry = Integer.MAX_VALUE / 10;
        int i = 0, sign = 1, length = str.length();
        if(length == 0) return 0;
        while(str.charAt(i) == ' ')
            if(++i == length) return 0;
        if(str.charAt(i) == '-') sign = -1;
        if(str.charAt(i) == '-' || str.charAt(i) == '+') i++;
        for(int j = i; j < length; j++) {
            if(str.charAt(j) < '0' || str.charAt(j) > '9') break;
            if(res > bndry || res == bndry && str.charAt(j) > '7')
                return sign == 1 ? Integer.MAX_VALUE : Integer.MIN_VALUE;
            res = res * 10 + (str.charAt(j) - '0');
        }
        return sign * res;
    }
}

```

</details>
