CNN
===
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2022-10-13%2001%3A56%3A19&color=yellowgreen&style=flat-square)

<!--END_SECTION:badge-->

- [CNN 基础](#cnn-基础)
    - [权值共享](#权值共享)
- [常见问题](#常见问题)
    - [`1*1` 卷积的作用](#11-卷积的作用)

## CNN 基础

### 权值共享
- 原理：
- 每次使用一个卷积核，通过滑动窗口


## 常见问题

### `1*1` 卷积的作用
> [卷积神经网络中用 1*1 卷积有什么作用或者好处呢？ - 知乎](https://www.zhihu.com/question/56024942)

- **计算**，`n*n` 卷积会作用于 `width` 和 `height`，包括 `depth`；`1*1` 则仅用于 `depth`，实际上就是对 `depth` 维度的特征做一次全连接操作（每个像素位置共享权重）；
- **作用**：
    1. 在全连接后接激活函数，加入非线性；或者说实现了跨通道（channel）的交互；
    2. 降维/减少参数、升维；