RNN
===
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2025-07-08%2016%3A53%3A13&color=yellowgreen&style=flat-square)

<!--END_SECTION:badge-->

- [RNN](#rnn)
    - [RNN 的前向过程](#rnn-的前向过程)
- [LSTM](#lstm)
    - [LSTM 的前向过程](#lstm-的前向过程)
    - [常见问题](#常见问题)
        - [LSTM 和 RNN 的区别](#lstm-和-rnn-的区别)
        - [Cell state 和 Hidden state 的关系](#cell-state-和-hidden-state-的关系)
        - [LSTM 中各个门的作用是什么？](#lstm-中各个门的作用是什么)
        - [LSTM 前向过程（门的顺序）](#lstm-前向过程门的顺序)
- [GRU](#gru)
    - [GRU 的前向过程](#gru-的前向过程)
    - [常见问题](#常见问题-1)
        - [GRU 中各门的作用](#gru-中各门的作用)
        - [GRU 与 LSTM 的区别](#gru-与-lstm-的区别)

## RNN

### RNN 的前向过程

$$
\begin{aligned}
    y_t &= W[h_{t-1},x_t] + b \\ 
    h_t &= \tanh(a_t) 
\end{aligned}
$$
> 

或

$$
\begin{aligned}
    y_t &= W[y_{t-1},x_t] + b \\ 
    h_t &= \tanh(a_t) 
\end{aligned}
$$
> $[x1,x2]$ 表示**向量拼接**；RNN 为递推结构，其中 $h_0$ 一般初始化为 0；

> 前者来自 Elman，后者来自 Jordan；两个过程的区别仅在于当前步的输入不同，一般所说的 RNN 指的是前者；
>> [Recurrent neural network - Wikipedia](https://en.wikipedia.org/wiki/Recurrent_neural_network#Elman_networks_and_Jordan_networks)


## LSTM

### LSTM 的前向过程

$$
\begin{aligned}
    f_t &= \sigma(W_f[h_{t-1},x_t] + b_t) \\
    i_t &= \sigma(W_i[h_{t-1},x_t] + b_i) \\
    \tilde{C}_t &= \tanh(W_C[h_{t-1},x_t] + b_C) \\
    C_t &= f_t * C_{t-1} + i_t * \tilde{C}_t \\
    o_t &= \sigma(W_o[h_{t-1},x_t] + b_o) \\
    h_t &= o_t * \tanh(C_t)
\end{aligned}
$$
> $[x1,x2]$ 表示**向量拼接**；$*$ 表示**按位相乘**；  
> $f_i$：长期记忆的遗忘比重；  
> $i_i$：短期记忆的保留比重；  
> $\tilde{C}_t$：当前时间步的 Cell 隐状态，即短期记忆；也就是普通 RNN 中的 $h_t$  
> $C_{t-1}$：历史时间步的 Cell 隐状态，即长期记忆；  
> $C_t$：当前时间步的 Cell 隐状态；  
> $o_t$：当前 Cell 隐状态的输出比重；  
> $h_t$：当前时间步的隐状态（输出）；

### 常见问题

#### LSTM 和 RNN 的区别
> 相关问题：**Cell 状态的作用**、**LSTM 是如何实现长短期记忆的？**
- LSTM 相比 RNN 多了一组 **Cell 隐状态**，记 $C$（Hidden 隐状态两者都有）；
    - $C$ 保存的是当前时间步的隐状态，具体包括来自之前（所有）时间步的隐状态 $C_{t-1}$ 和当前时间步的**临时隐状态** $\tilde{C}_t$。
- 由于 Cell 的加入，使 LSTM 具备了控制**长期/短期记忆比重**的能力，具体来说：
    - 如果**长期记忆**（之前时间步）的信息不太重要，就**减小** $C_{t-1}$ 的比重，反映在遗忘门的输出 $f_t$ 较小；
    - 如果**短期记忆**（当前时间步）的信息比较重要，就**增大** $\tilde{C}_t$ 的比重，反映在记忆门的输出 $i_t$ 较大；
- **参考**：
    - [对LSTM的理解 - 知乎](https://zhuanlan.zhihu.com/p/332736318)

#### Cell state 和 Hidden state 的关系
> [如何理解 LSTM 中的 cell state 和 hidden state? - 知乎](https://www.zhihu.com/question/68456751?sort=created)

- 从前向过程可以看到 Cell 存储了全部时间步的信息，而 Hidden 由 Cell 经过输出门后得到，可以把 Hidden 看做是网络在 Cell 基础上进行特征选择的结果；
- 一种说法是 Cell 偏向长期记忆，Hidden 偏向短期记忆；

#### LSTM 中各个门的作用是什么？
- “**遗忘门**”控制前一步记忆状态（$C_{t-1}$）中的信息有多大程度被遗忘；
- “**输入门**（记忆门）”控制当前的新状态（$\tilde{C}_t$）以多大的程度更新到记忆状态中；
- “**输出门**”控制当前输出（$h_t$）多大程度取决于当前的记忆状态（$C_t$）；

#### LSTM 前向过程（门的顺序）
- 遗忘门 -> 输入门 -> 输出门


## GRU

### GRU 的前向过程

$$
\begin{aligned}
    z_t &= \sigma(W_z[h_{t-1},x_t] + b_z) \\
    r_t &= \sigma(W_r[h_{t-1},x_t] + b_r) \\
    \tilde{h}_t &= \tanh(W[r_t*h_{t-1},x_t] + b) \\
    h_t &= (1-z_t)*h_{t-1} + z_t * \tilde{h}_t
\end{aligned}
$$
> $[x1,x2]$ 表示**向量拼接**；$*$ 表示**按位相乘**；

### 常见问题

#### GRU 中各门的作用
- “更新门”用于控制前一时刻的状态信息被融合到当前状态中的程度；
- “重置门”用于控制忽略前一时刻的状态信息的程度

#### GRU 与 LSTM 的区别
- 合并 “遗忘门” 和 “记忆门” 为 “更新门”；
    - 其实更像是移除了 “输出门”；
- 移除 Cell 隐状态，直接使用 Hidden 代替；