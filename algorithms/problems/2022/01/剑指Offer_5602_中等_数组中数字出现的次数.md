## 数组中数字出现的次数
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2022-10-14%2014%3A59%3A33&color=yellowgreen&style=flat-square)
[![](https://img.shields.io/static/v1?label=&message=%E4%B8%AD%E7%AD%89&color=yellow&style=flat-square)](../../../README.md#中等)
[![](https://img.shields.io/static/v1?label=&message=%E5%89%91%E6%8C%87Offer&color=green&style=flat-square)](../../../README.md#剑指offer)
[![](https://img.shields.io/static/v1?label=&message=%E4%BD%8D%E8%BF%90%E7%AE%97&color=blue&style=flat-square)](../../../README.md#位运算)

<!--END_SECTION:badge-->
<!--info
tags: [位运算]
source: 剑指Offer
level: 中等
number: '5602'
name: 数组中数字出现的次数
companies: []
-->

<summary><b>问题简述</b></summary>

```txt
数组 nums 中除一个数字只出现一次外，其他数字都出现了三次。找出那个只出现一次的数字。
要求：时间复杂度 O(N)，空间复杂度 O(1)
```

<details><summary><b>详细描述</b></summary>

```txt
在一个数组 nums 中除一个数字只出现一次之外，其他数字都出现了三次。请找出那个只出现一次的数字。

示例 1：
    输入：nums = [3,4,3,3]
    输出：4
示例 2：
    输入：nums = [9,1,7,9,7,9,7]
    输出：1

限制：
    1 <= nums.length <= 10000
    1 <= nums[i] < 2^31


来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/shu-zu-zhong-shu-zi-chu-xian-de-ci-shu-ii-lcof
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```

</details>

<!-- <div align="center"><img src="../../../_assets/xxx.png" height="300" /></div> -->

<summary><b>思路1</b></summary>

- 统计每个数字二进制各位出现的次数，然后对各位出现的次数对 3 求余，即可得到目标值的二进制各位的值；
- 因为每个数的二进制位数是固定的，所以空间复杂度依然是 `O(1)`；

<details><summary><b>Python</b></summary>

```python
class Solution:
    def singleNumber(self, nums: List[int]) -> int:
        
        cnt = [0] * 32

        for i in range(32):
            for x in nums:
                if x & (1 << i):
                    cnt[i] += 1
        
        ret = 0
        for i, n in enumerate(cnt):
            if n % 3:
                ret += 2 ** i
        
        return ret
```

</details>


**优化**：上述Python代码只能处理正数，如果是负数还要一步操作
> [数组中数字出现的次数 II（位运算 + 有限状态自动机，清晰图解） - Krahets](https://leetcode-cn.com/problems/shu-zu-zhong-shu-zi-chu-xian-de-ci-shu-ii-lcof/solution/mian-shi-ti-56-ii-shu-zu-zhong-shu-zi-chu-xian-d-4/)

<details><summary><b>Python</b></summary>

```python
class Solution:
    def singleNumber(self, nums: List[int]) -> int:
        
        cnt = [0] * 32

        for i in range(32):
            for x in nums:
                if x & (1 << i):
                    cnt[i] += 1
        
        ret = 0
        for i, n in enumerate(cnt):
            if n % 3:
                ret += 2 ** i
        
        if cnt[31] % 3 == 0:  # 最高位是 0 为正数
            return ret
        else:
            return ~(ret ^ 0xffffffff)  # 这一步的操作实际上就是讲 ret 二进制表示中 32位以上的部分都置为 0
```

</details>


<summary><b>思路2：有限状态自动机</b></summary>

> [数组中数字出现的次数 II（位运算 + 有限状态自动机，清晰图解） - Krahets](https://leetcode-cn.com/problems/shu-zu-zhong-shu-zi-chu-xian-de-ci-shu-ii-lcof/solution/mian-shi-ti-56-ii-shu-zu-zhong-shu-zi-chu-xian-d-4/)

<details><summary><b>Python</b></summary>

```python
class Solution:
    def singleNumber(self, nums: List[int]) -> int:
        ones, twos = 0, 0
        for num in nums:
            ones = ones ^ num & ~twos
            twos = twos ^ num & ~ones
        return ones
```

</details>
