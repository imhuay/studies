Attention
===
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2025-07-08%2016%3A53%3A13&color=yellowgreen&style=flat-square)

<!--END_SECTION:badge-->

- [Multi-head Self Attention](#multi-head-self-attention)
    - [前向过程（PyTorch 实现）](#前向过程pytorch-实现)

## Multi-head Self Attention

<!-- 
### 前向过程

$$
\begin{aligned}
    \text{Attention}(Q,K,V) &= \text{softmax}(\frac{QK^T}{\sqrt{d_k}})V \\
    \text{head}_\text{i} &= \text{Attention}(QW_i^Q,KW_i^K,VW_i^V) \\
    \text{MultiHead}(Q,K,V) &= \text{Concat}(\text{head}_1,..,\text{head}_\text{h})W^O
\end{aligned}
$$
 -->

### 前向过程（PyTorch 实现）

```python
def forward(x, mask, H, D):
    q = k = v = x  # [B, L, N]
    B, L, N = x.shape

    # linear
    q = W_q(q).reshape([B, L, H, D]).transpose(1, 2)  # [B, H, T, D]
    k = W_k(k).reshape([B, L, H, D]).transpose(1, 2)  # [B, H, T, D]
    v = W_v(v).reshape([B, L, H, D]).transpose(1, 2)  # [B, H, T, D]

    # attention
    logits = matmul(q, k.transpose(-2, -1)) / sqrt(D) + mask
    a = softmax(logits)

    # output
    o = matmul(a, v)
    o = W_o(o).reshape([B, L, N])
    return o

```