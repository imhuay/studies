## 构建乘积数组
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2022-10-14%2014%3A59%3A33&color=yellowgreen&style=flat-square)
[![](https://img.shields.io/static/v1?label=&message=%E4%B8%AD%E7%AD%89&color=yellow&style=flat-square)](../../../README.md#中等)
[![](https://img.shields.io/static/v1?label=&message=%E5%89%91%E6%8C%87Offer&color=green&style=flat-square)](../../../README.md#剑指offer)
[![](https://img.shields.io/static/v1?label=&message=%E5%89%8D%E7%BC%80%E5%92%8C&color=blue&style=flat-square)](../../../README.md#前缀和)

<!--END_SECTION:badge-->
<!--info
tags: [前缀和]
source: 剑指Offer
level: 中等
number: '6600'
name: 构建乘积数组
companies: []
-->

<summary><b>问题简述</b></summary>

```txt
给定一个数组 A，试返回数组 B，其中 B[i] 的值是数组 A 中除了下标 i 以外的元素的积, 即 B[i]=A[0]×A[1]×…×A[i-1]×A[i+1]×…×A[n-1]。

不能使用除法。
```

<details><summary><b>详细描述</b></summary>

```txt
给定一个数组 A[0,1,…,n-1]，请构建一个数组 B[0,1,…,n-1]，其中 B[i] 的值是数组 A 中除了下标 i 以外的元素的积, 即 B[i]=A[0]×A[1]×…×A[i-1]×A[i+1]×…×A[n-1]。不能使用除法。

示例:
    输入: [1,2,3,4,5]
    输出: [120,60,40,30,24]

提示：
    所有元素乘积之和不会溢出 32 位整数
    a.length <= 100000

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/gou-jian-cheng-ji-shu-zu-lcof
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```

</details>

<!-- <div align="center"><img src="../../../_assets/xxx.png" height="300" /></div> -->

<summary><b>思路</b></summary>

- 双向构建前缀积（左→右、右→左），示例：

    ```
    l = [1, a1, a1a2, a1a2a3]
    r = [a2a3a4, a3a4, a4, 1]
    s = [l[0] * r[0] for i in range(len(a))]
    ```

<details><summary><b>Python</b></summary>

```python
class Solution:
    def constructArr(self, a: List[int]) -> List[int]:

        l = [1]
        for x in a[:-1]:
            l.append(l[-1] * x)
        # print(l)

        r = [1]
        for x in a[::-1][:-1]:
            r.append(r[-1]*x)
        r = r[::-1]
        # print(r)

        return [l[i] * r[i] for i in range(len(a))]
```

</details>


<details><summary><b>Python：空间优化</b></summary>

- 实际上在求 s 的时候可以同步求前缀积，换言之，可以节省一组前缀积（这里优化掉 `l`）；

```python
class Solution:
    def constructArr(self, a: List[int]) -> List[int]:

        r = [1] * len(a)
        for i in range(len(a) - 1, 0, -1):
            r[i - 1] = r[i] * a[i]
        # print(r)

        pre = 1
        for i, x in enumerate(a):
            r[i] *= pre
            pre *= x

        return r
```

</details>
