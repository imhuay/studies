## 剑指Offer_6500_不用加减乘除做加法（简单, 2022-01）
<!--{
    "tags": ["位运算"],
    "来源": "剑指Offer",
    "编号": "6500",
    "难度": "简单",
    "标题": "不用加减乘除做加法"
}-->

<summary><b>问题简述</b></summary>

```txt
求两个整数之和，要求不能使用 “+”、“-”、“*”、“/” 运算符号。
```

<details><summary><b>详细描述</b></summary>

```txt
写一个函数，求两个整数之和，要求在函数体内不得使用 “+”、“-”、“*”、“/” 四则运算符号。

示例:
    输入: a = 1, b = 1
    输出: 2

提示：
    a, b 均可能是负数或 0
    结果不会溢出 32 位整数

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/bu-yong-jia-jian-cheng-chu-zuo-jia-fa-lcof
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```

</details>

<!-- <div align="center"><img src="../../../_assets/xxx.png" height="300" /></div> -->

<summary><b>思路</b></summary>

<div align="center"><img src="../../../_assets/剑指Offer_065_简单_不用加减乘除做加法.png" height="300" /></div>

> [不用加减乘除做加法（位运算，清晰图解）](https://leetcode-cn.com/problems/bu-yong-jia-jian-cheng-chu-zuo-jia-fa-lcof/solution/mian-shi-ti-65-bu-yong-jia-jian-cheng-chu-zuo-ji-7/)

- 不用编程语言之间略有区别；

<details><summary><b>Java（推荐）</b></summary>

```java
class Solution {
    public int add(int a, int b) {
        while(b != 0) { // 当进位为 0 时跳出
            int c = (a & b) << 1;  // c = 进位
            a ^= b; // a = 非进位和
            b = c; // b = 进位
        }
        return a;
    }
}
```

</details>

<details><summary><b>Python</b></summary>

- Python 中

```python
class Solution:
    def add(self, a: int, b: int) -> int:
        x = 0xffffffff
        a, b = a & x, b & x  # 转为补码形式
        while b != 0:
            a, b = (a ^ b), (a & b) << 1 & x
        return a if a <= 0x7fffffff else ~(a ^ x)  # 还原
```

</details>

<details><summary><b>C++</b></summary>

> [不用加减乘除做加法](https://leetcode-cn.com/problems/bu-yong-jia-jian-cheng-chu-zuo-jia-fa-lcof/solution/dian-zan-yao-wo-zhi-dao-ni-xiang-kan-dia-ovxy/)

```cpp
class Solution {
public:
    int add(int a, int b) {
        while (b) {
            int carry = a & b; // 计算 进位
            a = a ^ b; // 计算 本位
            b = (unsigned)carry << 1;  // C++中负数不支持左位移
        }
        return a;
    }
};
```

</details>

