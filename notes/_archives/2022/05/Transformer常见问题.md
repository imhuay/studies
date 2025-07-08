Transformer 常见问题
===
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2023-02-02%2016%3A35%3A31&color=yellowgreen&style=flat-square)

<!--END_SECTION:badge-->
<!--info
top: true
-->

- [Transformer Encoder 代码](#transformer-encoder-代码)
- [Transformer 与 RNN/CNN 的比较](#transformer-与-rnncnn-的比较)
    - [RNN](#rnn)
    - [CNN](#cnn)
    - [Transformer](#transformer)
    - [Transformer 能完全取代 RNN 吗？](#transformer-能完全取代-rnn-吗)
- [Transformer 中各模块的作用](#transformer-中各模块的作用)
    - [QKV Projection](#qkv-projection)
        - [为什么在 Attention 之前要对 Q/K/V 做一次投影？](#为什么在-attention-之前要对-qkv-做一次投影)
    - [Self-Attention](#self-attention)
        - [为什么要使用多头？](#为什么要使用多头)
        - [为什么 Transformer 中使用的是乘性 Attention（点积），而不是加性 Attention？](#为什么-transformer-中使用的是乘性-attention点积而不是加性-attention)
        - [Attention 计算中 Scaled 操作的目的是什么？](#attention-计算中-scaled-操作的目的是什么)
        - [在 Softmax 之前加上 Mask 的作用是什么？](#在-softmax-之前加上-mask-的作用是什么)
    - [Add & Norm](#add--norm)
        - [加入残差的作用是什么？](#加入残差的作用是什么)
        - [加入 LayerNorm 的作用是什么？](#加入-layernorm-的作用是什么)
        - [Pre-LN 和 Post-LN 的区别](#pre-ln-和-post-ln-的区别)
    - [Feed-Forward Network](#feed-forward-network)
        - [FFN 层的作用是什么？](#ffn-层的作用是什么)
        - [FFN 中激活函数的选择](#ffn-中激活函数的选择)
- [BERT 相关面试题](#bert-相关面试题)
- [参考资料](#参考资料)


## Transformer Encoder 代码

<details><summary><b>Transformer Encoder（点击展开）</b></summary> 

```python
import math

import torch
import torch.nn as nn
import torch.nn.functional as F
import einops


class TransformerEncoder(nn.Module):

    def __init__(self, n_head, d_model, d_ff, act=F.gelu):
        super().__init__()

        self.h = n_head
        self.d = d_model // n_head
        # Attention
        self.Q = nn.Linear(d_model, d_model)
        self.K = nn.Linear(d_model, d_model)
        self.V = nn.Linear(d_model, d_model)
        self.O = nn.Linear(d_model, d_model)
        # LN
        self.LN1 = nn.LayerNorm(d_model)
        self.LN2 = nn.LayerNorm(d_model)
        # FFN
        self.W1 = nn.Linear(d_model, d_ff)
        self.W2 = nn.Linear(d_ff, d_model)
        self.act = act
        #
        self.dropout = nn.Dropout(0.2)

    def attn(self, x, mask):
        q, k, v = self.Q(x), self.K(x), self.V(x)
        q = einops.rearrange(q, 'B L (H d) -> B H L d', H=self.h)
        k = einops.rearrange(k, 'B L (H d) -> B H d L', H=self.h)
        v = einops.rearrange(v, 'B L (H d) -> B H L d', H=self.h)
        a = torch.softmax(q @ k / math.sqrt(self.d) + mask, dim=-1)  # [B H L L]
        o = einops.rearrange(a @ v, 'B H L d -> B L (H d)')
        o = self.O(o)
        return o

    def ffn(self, x):
        x = self.dropout(self.act(self.W1(x)))
        x = self.dropout(self.W2(x))
        return x

    def forward(self, x, mask):
        x = self.LN1(x + self.dropout(self.attn(x, mask)))
        x = self.LN2(x + self.dropout(self.ffn(x)))
        return x


model = TransformerEncoder(2, 4, 8)
x = torch.randn(2, 3, 4)
mask = torch.randn(1, 1, 3, 3)
o = model(x, mask)

model.eval()
traced_model = torch.jit.trace(model, (x, mask))

x = torch.randn(2, 3, 4)
mask = torch.randn(1, 1, 3, 3)

assert torch.allclose(model(x, mask), traced_model(x, mask))
```

</details>


## Transformer 与 RNN/CNN 的比较
> 其他提法：Transformer 为什么比 RNN/CNN 更好用？优势在哪里？  
> 参考资料：
> - [自然语言处理三大特征抽取器（CNN/RNN/Transformer）比较 - 知乎](https://zhuanlan.zhihu.com/p/54743941)
>   - [CNN/RNN/Transformer比较 - 简书](https://www.jianshu.com/p/67666ada573b)
>   - [NLP常用特征提取方法对比 - CSDN博客](https://blog.csdn.net/u013124704/article/details/105201349)

### RNN
- 特点/优势（Transformer之前）：
    - 适合解决线性序列问题；天然能够捕获位置信息（相对+绝对）；
        > 绝对位置：每个 token 都是在固定时间步加入编码；相对位置：token 与 token 之间间隔的时间步也是固定的；
    - 支持不定长输入；
    - LSTM/Attention 的引入，加强了长距离语义建模的能力；
- 劣势：
    - 串行结构难以支持并行计算；
    - 依然存在长距离依赖问题；
        > 有论文表明：RNN 最多只能记忆 50 个词左右的距离（How Neural Language Models Use Context）；
    - 单向语义建模（Bi-RNN 是两个单向拼接）

### CNN
- 特点/优势：
    - 捕获 n-gram 片段信息（局部建模）；
    - 滑动窗口捕获相对位置特征（但 Pooling 层会丢失位置特征）；
    - 并行度高（滑动窗口并行、卷积核并行），计算速度快；
- 劣势：
    - 长程建模能力弱：受感受野限制，无法捕获长距离依赖，需要空洞卷积或加深层数等策略来弥补；
    - Pooling 层会丢失位置信息（目前常见的作法会放弃 Pooling）；
    - 相对位置敏感，绝对位置不敏感（平移不变性）

### Transformer
- 特点/优势：
    - 通过位置编码（position embedding）建模相对位置和绝对位置特征；
    - Self-Attention 同时编码双向语义和解决长距离依赖问题；
    - 支持并行计算；
- 缺点/劣势：
    - 不支持不定长输入（通过 padding 填充到定长）；
    - 计算复杂度高；

### Transformer 能完全取代 RNN 吗？
> [有了Transformer框架后是不是RNN完全可以废弃了？ - 知乎](https://www.zhihu.com/question/302392659?sort=created)

- 不行；

<!-- 
下面主要从三个方面进行比较：对**上下文语义特征**和**序列特征**的表达能力（主要），以及**计算速度**；

### 1. 上下文语义特征
在抽取上下文语义特征（方向+距离）方面：**Transformer > RNN > CNN**
- RNN 只能进行单向编码（Bi-RNN 是两个单向）；  
  在**长距离**特征抽取上也弱于 Transformer；有论文表明：RNN 最多只能记忆 50 个词左右的距离；
    > How Neural Language Models Use Context
- CNN 只能对短句编码（N-gram）；
- Transformer 可以同时**编码双向语义**和**抽取长距离特征**；

### 2. 序列特征
在抽取序列特征方面：**RNN > Transformer > CNN**
- Transformer 的序列特征完全依赖于 Position Embedding，当序列长度没有超过 RNN 的处理极限时，位置编码对时序性的建模能力是不及 RNN 的；
- CNN 的时序特征 TODO；

### 3. 计算速度
在计算速度方面：**CNN > Transformer > RNN**
- RNN 因为存在时序依赖难以并行计算；
- Transformer 和 CNN 都可以并行计算，但 Transformer 的计算复杂度更高；
 -->

## Transformer 中各模块的作用

### QKV Projection

#### 为什么在 Attention 之前要对 Q/K/V 做一次投影？
- 首先在 Transformer-Encoder 中，Q/K/V 是相同的输入；
- 加入这个全连接的目的就是为了将 Q/K/V 投影到不同的空间中，增加多样性；
- 如果没有这个投影，在之后的 Attention 中相当于让相同的 Q 和 K 做点击，那么 attention 矩阵中的分数将集中在对角线上，即每个词的注意力都在自己身上；这与 Attention 的初衷相悖——**让每个词去融合上下文语义**；

### Self-Attention

#### 为什么要使用多头？
> 其他提法：多头的加入既没有增加宽度也没有增加深度，那加入它的意义在哪里？
- 这里的多头和 CNN 中多通道的思想类似，目的是期望不同的注意力头能学到不同的特征；

#### 为什么 Transformer 中使用的是乘性 Attention（点积），而不是加性 Attention？
- 在 GPU 场景下，矩阵乘法的效率更高（原作说法）；
- **在不进行 Scaled 的前提下**，随着 d（每个头的特征维度）的增大，乘性 Attention 的效果减弱，加性 Attention 的效果更好（原因见下一个问题）；
    > [小莲子的回答 - 知乎](https://www.zhihu.com/question/339723385/answer/811341890)

#### Attention 计算中 Scaled 操作的目的是什么？
> 相似提法：为什么在计算 Q 和 K 的点积时要除以根号 d？  
> 参考内容：[Transformer 中的 attention 为什么要 scaled? - 知乎](https://www.zhihu.com/question/339723385)
- **目的**：防止梯度消失；
- **解释**：在 Attention 模块中，注意力权重通过 Softmax 转换为概率分布；但是 Softmax 对输入比较敏感，当输入的方差越大，其计算出的概率分布就越“尖锐”，即大部分概率集中到少数几个分量位置。极端情况下，其概率分布将退化成一个 One-Hot 向量；其结果就是雅可比矩阵（偏导矩阵）中绝大部分位置的值趋于 0，即梯度消失；通过缩放操作可以使注意力权重的方差重新调整为 1，从而缓解梯度消失的问题；
    - 假设 $Q$ 和 $K$ 的各分量 $\vec{q_i}$ 和 $\vec{k_i}$ 相互独立，且均值为 $0$，方差为 $1$；
        > 在 Embedding 和每一个 Encoder 后都会过一个 LN 层，所以可以认为这个假设是合理的；
    - 则未经过缩放的注意力权重 $A$ 的各分量 $\vec{a_i}$ 将服从均值为 $0$，方差为 $d$ 的正态分布；
    - $d$ 越大，意味着 $\vec{a_i}$ 中各分量的差越大，其结果就是经过 softmax 后，会出现数值非常小的分量；这样在反向传播时，就会导致**梯度消失**的问题；
    - 此时除以 $\sqrt{d}$ 会使 $\vec{a_i}$ 重新服从标准的正态分布，使 softmax 后的 Attention 矩阵尽量平滑，从而缓解梯度消失的问题；
    - **数学推导**：
        > [Transformer 中的 attention 为什么要 scaled? - TniL的回答（已删除）](https://www.zhihu.com/question/339723385/answer/782509914)
        - 定义 $Q=[\vec{q_1}, \vec{q_2}, .., \vec{q_n}]^T$, $K=[\vec{k_1}, \vec{k_2}, .., \vec{k_n}]^T$，其中 $\vec{q_i}$ 和 $\vec{k_i}$ 都是 $d$ 维向量；
        - 假设 $\vec{q_i}$ 和 $\vec{k_i}$ 的各分量都是服从标准正态分布（均值为 0，方差为 1）的随机变量，且相互独立，记 $q_i$ 和 $k_i$，即 $E(q_i)=E(k_i)=0$, $D(q_i)=D(k_i)=1$；
        - 根据期望与方差的性质，有 $E(q_ik_i)=0$ 和 $D(q_ik_i)=1$，推导如下：
            $$\begin{align*}
                E(q_ik_i) &= E(q_i)E(k_i) = 0 \times 0 = 0 \\
                D(q_ik_i) &= E(q_i^2k_i^2) - E^2(q_ik_i) \\
                &= E(q_i^2)E(k_i^2) - E^2(q_i)E^2(k_i) \\
                &= \left [E(q_i^2) - E^2(q_i) \right ] \left [E(k_i^2) - E^2(k_i) \right ] - 0^2 \times 0^2 \\
                &= D(q_i)D(k_i) - 0 \\
                &= 1
            \end{align*}$$
        - 进一步，有 $E(\vec{q_i}\vec{k_i}^T)=0$ 和 $D(\vec{q_i}\vec{k_i}^T)=d$，推导如下：
            $$\begin{align*}
                E(\vec{q_i}\vec{k_i}^T) &= E(\sum_{i=1}^d q_ik_i) = \sum_{i=1}^d E(q_ik_i) = 0 \\
                D(\vec{q_i}\vec{k_i}^T) &= D(\sum_{i=1}^d q_ik_i) = \sum_{i=1}^d D(q_ik_i) = d
            \end{align*}$$
        - 根据 attention 的计算公式（softmax 前）, $A'=\frac{QK^T}{\sqrt{d}}=[\frac{\vec{q_1}\vec{k_1}^T}{\sqrt{d}}, \frac{\vec{q_2}\vec{k_2}^T}{\sqrt{d}}, .., \frac{\vec{q_n}\vec{k_n}^T}{\sqrt{d}}]=[\vec{a_1}, \vec{a_2}, .., \vec{a_n}]$，可知 $E(\vec{a_i})=0$, $D(\vec{a_i})=1$，推导如下：
            $$\begin{align*}
                E(\vec{a_i}) &= E(\frac{\vec{q_i}\vec{k_i}^T}{\sqrt{d}}) = \frac{E(\vec{q_i}\vec{k_i}^T)}{\sqrt{d}} = \frac{0}{\sqrt{d}} = 0 \\
                D(\vec{a_i}) &= D(\frac{\vec{q_i}\vec{k_i}^T}{\sqrt{d}}) = \frac{D(\vec{q_i}\vec{k_i}^T)}{(\sqrt{d})^2} = \frac{d}{d} = 1
            \end{align*}$$
    - **代码验证**
        ```python
        import torch

        def get_x(shape, eps=1e-9):
            """创建一个 2d 张量，且最后一维服从正态分布"""
            x = torch.randn(shape)
            mean = x.mean(-1, keepdim=True)
            std = x.std(-1, keepdim=True)
            return (x - mean) / (std + eps)

        d = 400  # 数字设大一些，否则不明显
        q = get_x((2000, d))
        k = get_x((2000, d))

        # 不除以 根号 d
        a = torch.matmul(q, k.transpose(-1, -2))  # / (d ** 0.5)
        print(a.mean(-1, keepdim=True))  # 各分量接近 0
        print(a.var(-1, keepdim=True))  # 各分量接近 d

        # 除以根号 d
        a = torch.matmul(q, k.transpose(-1, -2)) / (d ** 0.5)
        print(a.mean(-1, keepdim=True))  # 各分量接近 0
        print(a.var(-1, keepdim=True))  # 各分量接近 1
        ```

    <!-- </details> -->


#### 在 Softmax 之前加上 Mask 的作用是什么？
> 相关问题：为什么将被 mask 的位置是加上一个极小值（-1e9），而不是置为 0？
- 回顾 softmax 的公式；
- 其目的就是使无意义的 token 在 softmax 后得到的概率值（注意力）尽量接近于 0；从而使正常 token 位置的概率和接近 1；

### Add & Norm

#### 加入残差的作用是什么？
- 在求导时加入一个恒等项，以减少梯度消失问题；

#### 加入 LayerNorm 的作用是什么？
- 提升网络的泛化性；（TODO：详细解释）
- 加在激活函数之前，避免激活值落入饱和区，减少梯度消失问题；

#### Pre-LN 和 Post-LN 的区别

- Post-LN（BERT 实现）：
    $$x_{n+1} = \text{LN}(x_n + f(x_n))$$
    - 先做完残差连接，再归一化；
    - 优点：保持主干网络的方程比较稳定，是模型泛化能力更强，性能更好；
    - 缺点：把恒等路径放在 norm 里，使模型收敛更难（反向传播时梯度变小，残差的作用被减弱）
- Pre-LN：
    $$x_{n+1} = x_n + f(\text{LN}(x_n))$$
    - 先归一化，再做残差连接；
    - 优点：加速收敛
    - 缺点：效果减弱

### Feed-Forward Network

- 前向公式
    $$W_2 \cdot \text{ReLU}(W_1x + b_1) + b_2$$

#### FFN 层的作用是什么？
- 功能与 1*1 卷积类似：1）跨通道的特征融合/信息交互；2）通过激活函数增加非线性；
    > [1*1卷积核的作用_nefetaria的博客-CSDN博客](https://blog.csdn.net/nefetaria/article/details/107977597)
- 之前操作都是线性的：1）Projection 层并没有加入激活函数；2）Attention 层只是线性加权；

#### FFN 中激活函数的选择
> 相关问题：BERT 为什么要把 FFN 中的 ReLU 替换为 GeLU？
- 背景：原始 Transformer 中使用的是 **ReLU**；BERT 中使用的是 **GeLU**；
- GeLU 在激活函数中引入了正则的思想，越小的值越容易被丢弃；相当于综合了 ReLU 和 Dropout 的功能；而 ReLU 缺乏这个随机性；
- 为什么不使用 sigmoid 或 tanh？——这两个函数存在饱和区，会使导数趋向于 0，带来梯度消失的问题；不利于深层网络的训练；



## BERT 相关面试题
- [daily-interview/BERT面试题.md at master · datawhalechina/daily-interview](https://github.com/datawhalechina/daily-interview/blob/master/AI%E7%AE%97%E6%B3%95/NLP/%E7%89%B9%E5%BE%81%E6%8C%96%E6%8E%98/BERT/BERT%E9%9D%A2%E8%AF%95%E9%A2%98.md)



## 参考资料
- [深入剖析PyTorch中的Transformer API源码_哔哩哔哩_bilibili](https://www.bilibili.com/video/BV1o44y1Y7cp/?spm_id_from=333.788)
- [超硬核Transformer细节全梳理！_哔哩哔哩_bilibili](https://www.bilibili.com/video/BV1AU4y1d7nT)
- [Transformer、RNN 与 CNN 三大特征提取器的比较_Takoony的博客-CSDN博客](https://blog.csdn.net/ningyanggege/article/details/89707196)
