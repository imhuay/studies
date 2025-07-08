## 划分2N个点
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2025-07-08%2016%3A53%3A13&color=yellowgreen&style=flat-square)
[![](https://img.shields.io/static/v1?label=&message=%E4%B8%AD%E7%AD%89&color=yellow&style=flat-square)](../../../README.md#中等)
[![](https://img.shields.io/static/v1?label=&message=Collection&color=green&style=flat-square)](../../../README.md#collection)
[![](https://img.shields.io/static/v1?label=&message=%E6%95%B0%E5%AD%A6&color=blue&style=flat-square)](../../../README.md#数学)

<!--END_SECTION:badge-->
<!--info
tags: [数学]
source: Collection
level: 中等
number: '20220126'
name: 划分2N个点
companies: []
-->

<summary><b>问题简述</b></summary>

```txt
平面上有 2N 个点，是否存在一条直线将这 2N 个点一分为二（各 N 个点）
```

<!-- 
<details><summary><b>详细描述</b></summary>

```txt
```

</details>
-->


<!-- <div align="center"><img src="../../../_assets/xxx.png" height="300" /></div> -->

<details><summary><b>思路</b></summary>

> [是否一点存在直线能把平面上给定的2n个点分成两部分，每部分n个点？ - 知乎](https://www.zhihu.com/question/25071189)

```txt
- 考虑将这 2N 个点两两相连得到 m 条直线（可能存在重叠），其斜率分别为 k_1, .., k_m；
- 因为 m 是有限的，则必然存在与这 m 条直线斜率不同的直线，
- 取这条直线的垂线，则这条垂线与这 m 条直线都不垂直；
- 把这条直线从这 2N 个点的一侧平移到另一侧，得到 2N 个交点，
- 则显然存在一条平行于平移方向的直线将这 2N 个交点分成两部分，而这条直线也将这 2N 个点划分成了数量相等的两部分。
```

</details>
