Transformer
===
- 原始 Transformer 指的是一个基于 Encoder-Decoder 框架的 Seq2Seq 模型，用于解决机器翻译任务；
- 后其 Encoder 部分被用于 BERT 而广为人知，因此有时 Transformer 也特指其 Encoder 部分；
- 相关论文：
    - [[1706.03762] Attention Is All You Need](https://arxiv.org/abs/1706.03762)
    - [[1810.04805] BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding](https://arxiv.org/abs/1810.04805)

---

- [整体框架](#整体框架)
- [常见问题](#常见问题)
    - [Attention 相关](#attention-相关)
- [参考资料](#参考资料)


## 整体框架

- 



## 常见问题

### Attention 相关

**Attention 计算中缩放（Scaled）的目的是什么？**
- 目的：防止梯度消失；
- 解释：
    - 在 Attention 模块中，注意力权重通过 Softmax 转换为概率分布；但是 Softmax 对输入比较敏感，当输入的方差越大，其计算出的概率分布就越“尖锐”，即大部分概率集中到少数几个分量位置。极端情况下，其概率分布将退化成一个 One-Hot 向量；其结果就是雅可比矩阵（偏导矩阵）中绝大部分位置的值趋于 0，即梯度消失；
        > [transformer中的attention为什么scaled? - 知乎](https://www.zhihu.com/question/339723385/answer/782509914) 
    - 对 $d$ 维向量 $q$ 和 $k$，假设其分量 $q_i$ 和 $k_i$ 为**相互独立**的随机变量，且均值都为 0，方差都为 1；则有 $q_id_i$ 的均值为 0，方差为 1，$qk^\top$ 的均值为 0，方差为 $d$；
    - 通过 Scaled 操作（除以 $\sqrt{d}$），可以将 $q\cdot k$ 相乘的方差还原到 1，从而缓解梯度消失的问题；
    - **推导如下**：
        $$$$ 
        $$\begin{align*}
            E(q_ik_i) &= E(q_i)E(k_i) = 0 \times 0 = 0 \\
            D(q_ik_i) &= E(q_i^2k_i^2) - E^2(q_ik_i) \\
            &= E(q_i^2)E(k_i^2) - E^2(q_i)E^2(k_i) \\
            &= [E(q_i^2) - E^2(q_i)][E(k_i^2) - E^2(k_i)] - E^2(q_i)E^2(k_i) \\
            &= D(q_i)D(k_i) - E^2(q_i)E^2(k_i) \\
            &= 1 \times 1 - 0 \times 0 = 1 \\
            E(qk^\top) &= E(\sum_{i=1}^d q_ik_i) = \sum_{i=1}^d E(q_ik_i) = 0 \\
            D(qk^\top) &= D(\sum_{i=1}^d q_ik_i) = \sum_{i=1}^d D(q_ik_i) = d \\
            D(\frac{qk^\top}{\sqrt{d}}) &= \frac{D(qk^\top)}{(\sqrt{d})^2} = \frac{D(qk^\top)}{d} = 1
        \end{align*}$$
    - **验证代码**
        ```python
        def softmax(score):
            return F.softmax(score, dim=-1)

        d = 10
        score1 = torch.randn(d)
        score2 = score1 * d  # 模拟高方差
        probs1 = softmax(score1)
        probs2 = softmax(score1)

        jacob1 = torch.autograd.functional.jacobian(softmax, score1)
        jacob2 = torch.autograd.functional.jacobian(softmax, score2)

        print(jacob1)  # 正常的梯度
        print(jacob2)  # 高方差下的梯度，各分量趋于0
        ``` 


## 参考资料

