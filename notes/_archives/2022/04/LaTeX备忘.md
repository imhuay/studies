LaTeX in Markdown 备忘
===
<!--START_SECTION:badge-->

![create date](https://img.shields.io/static/v1?label=create%20date&message=2022-04-xx&label_color=gray&color=lightsteelblue&style=flat-square)
![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2025-08-27%2009%3A29%3A07&label_color=gray&color=thistle&style=flat-square)

<!--END_SECTION:badge-->
<!--info
top: false
draft: false
hidden: false
tag: [tools]
-->

<!--START_SECTION:toc-->
- [参考](#参考)
- [常用符号](#常用符号)
- [多行公式对齐](#多行公式对齐)
    - [无编号](#无编号)
    - [有编号](#有编号)
- [括号](#括号)
- [标记](#标记)
<!--END_SECTION:toc-->

## 参考
- [【LaTeX】LaTeX符号大全_Ljnoit-CSDN博客_latex 绝对值符号](https://blog.csdn.net/ljnoit/article/details/104264753)
- 在线 LaTeX 公式编辑器：https://editor.codecogs.com


## 常用符号

$$
    \sum_{a}^{e}
$$


## 多行公式对齐

### 无编号

写在行 $\begin{aligned} x &= a + b \\  &= c + d \end{aligned}$ 内;

**单独一行**:  

$$
\begin{align*}
 a &= 1+2 \\ 
   &= 2+1
\end{align*}
$$

**左括号**:  

$$
\left \lbrace
    \begin{aligned}
    a &= 1+2 &// 说明1  \\ 
    b &= 2+1 &// 说明2
    \end{aligned}
\right.
$$

### 有编号

$$
\begin{align}
 a &= 1+1 &// 说明1 \\ 
 b &= 2+2 &// 说明2
\end{align}
$$


## 括号

**绝对值**  

$$
\left | a \right |
$$

**中括号** (直接使用 \[ 和 \] 在 VSCode 中有警告)  

$$
\lbrack \rbrack
$$


## 标记

**转置**  
$$\begin{align*}
& \mathbf{A}^\mathrm{T}                 \\
& \mathbf{A}^\top           &// 推荐     \\
& \mathbf{A}^\mathsf{T}                 \\
& \mathbf{A}^\intercal                  \\
\end{align*}$$
