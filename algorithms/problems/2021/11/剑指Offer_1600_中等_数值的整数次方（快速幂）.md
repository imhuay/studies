## 剑指Offer_1600_数值的整数次方（快速幂）（中等, 2021-11）
<!--{
    "tags": ["递归", "二分法", "经典"],
    "来源": "剑指Offer",
    "编号": "1600",
    "难度": "中等",
    "标题": "数值的整数次方（快速幂）"
}-->

<summary><b>问题简述</b></summary>

```txt
实现快速幂算法，即 pow(x, n)，不使用库函数；
```

<details><summary><b>详细描述</b></summary>

```txt
实现 pow(x, n) ，即计算 x 的 n 次幂函数（即，xn）。不得使用库函数，同时不需要考虑大数问题。

示例 1：
    输入：x = 2.00000, n = 10
    输出：1024.00000
示例 2：
    输入：x = 2.10000, n = 3
    输出：9.26100
示例 3：
    输入：x = 2.00000, n = -2
    输出：0.25000
    解释：2-2 = 1/22 = 1/4 = 0.25

提示：
    -100.0 < x < 100.0
    -2^31 <= n <= 2^31-1
    -10^4 <= x^n <= 10^4

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/shu-zhi-de-zheng-shu-ci-fang-lcof
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```

</details>

<summary><b>思路</b></summary>

- 直接连乘 n 次会报超时；
- 从二分角度理解快速幂

    ```python
    3^20      
    = (3^2)^10       # 当指数为偶数时，对指数除2取整，底数平方
    = (9^2)^5   
    = (81^2)^2 * 81  # 当指数为奇数时，对指数除2取整，底数平方，同时再乘一个当前的底数（这里是 81）
    = (6561^2)^1 * 81
    = 43046721^0 * 81 * 43046721
    = 1 * 81 * 43046721
    ```

    > [数值的整数次方（快速幂，清晰图解）](https://leetcode-cn.com/problems/shu-zhi-de-zheng-shu-ci-fang-lcof/solution/mian-shi-ti-16-shu-zhi-de-zheng-shu-ci-fang-kuai-s/)

<!-- <div align="center"><img src="../../../_assets/xxx.png" height="300" /></div> -->

<details><summary><b>Python</b></summary>

```python
class Solution:
    def myPow(self, x: float, n: int) -> float:
        if x == 0: 
            return 0
        
        if n == 0:
            return 1

        if n < 0: 
            x = 1 / x
            n = -n

        ret = 1
        while n:
            if n & 1: 
                ret *= x
            x *= x
            n >>= 1
        return ret
```

</details>

