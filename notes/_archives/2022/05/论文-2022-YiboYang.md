Do We Really Need a Learnable Classifier at the End of Deep Neural Network?
===
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2025-07-08%2016%3A53%3A13&color=yellowgreen&style=flat-square)

<!--END_SECTION:badge-->
> https://arxiv.org/abs/2203.09081

- [摘要](#摘要)
- [引言](#引言)
- [代码](#代码)
    - [生成 ETF](#生成-etf)

---

## 摘要
- 用于**分类**的神经网络模型通常由两部分组成：一个输出表示特征的**主干网络**（backbone network）和一个输出 logits 的**线性分类器**（linear classifier）；
- 最近的研究显示了一种称为**神经坍缩**（neural collapse）的现象，即**特征的类内均值**和**分类器向量**在**平衡数据集**的训练结束阶段会收敛到一个**单纯型等角紧框架**（Simplex Equiangular Tight Frame, Simplex ETF）的顶点；
    - **特征的类内均值**，指所有类别的训练数据通过主干网络后得到特征向量的均值；  
    - **分类器向量**，指分类层的权重；
    - **ETF 结构**会最大程度的分离分类器中所有类的成对角度（pair-wise angles）；
- 引出本文的课题：当我们知道一个分类器的最佳几何结构时，是否还需要去训练它？
- 研究表明，使用**固定的 ETF 分类器**能够自然导致神经奔溃状态，即使在**不平衡数据**上；
- 本文进一步证明在这种情况下，可以用一个简单的平方损失代替交叉熵损失，两者具有相同的全局最优性，且平方损失有着更精确的梯度和更好的收敛性；
- 实验表明，本文提出的方法，能在平衡数据上达到相似的性能，而在长尾的细粒度分类（**不平衡数据**）任务上带来显著的改进；


## 引言
- **使用神经网络模型解决分类问题的基本框架**；
    - 选择一个**主干网络**（backbone network）；
    - 设置**线性分类头**（linear classifier）；
    - 使用**交叉熵损失函数**（cross entropy loss）进行训练；
    - 虽然目前基于神经网络的网络在可解释性方面有待进一步研究，但其目标是明确的，就是生成尽可能**线性可分离**（linearly separable）的特征，然后**线性分类头的作用**就是将这些特征区分开来，得到各类别的 logits；
- 最近一项研究揭示了一个称为“**神经奔溃**”（neural collapse）的现象；
    - 在一个平衡数据集上训练至收敛时，
    - 同一类的特征（经过主干网络得到的特征向量）将奔溃为类内均值，
    - 所有类的类内均值及其相应的分类器向量，将收敛到具有自对偶性的单纯形等角紧框架（ETF）的顶点


## 代码

### 生成 ETF

```python
import numpy as np
from scipy import linalg


def simplex_equiangular_tight_frame(k, d):
    """
    生成单纯型等角紧框架
    返回矩阵 M（k 个 d 维向量）
    满足如下性质：对任意 i,j
        当 i == j 时，有 M[i] @ M[j].T == 1
        当 i != j 时，有 M[i] @ M[j].T == -1/(k-1)

    Examples:
        >>> k, d = 4, 5  # noqa
        >>> M = simplex_equiangular_tight_frame(k, d)  # noqa
        >>> for i in range(k):
        ...     for j in range(k):
        ...         if i == j: assert np.isclose(M[i] @ M[j].T, 1)
        ...         else: assert np.isclose(M[i] @ M[j].T, -1/(k-1))

    Args:
        k: k 个向量
        d: 每个向量的维度，assert k <= d + 1

    Returns: 
        shape [k, d]

    References:
        Do We Really Need a Learnable Classifier at the End of Deep Neural Network?
    """
    assert k <= d + 1, 'assert k <= d + 1'
    # 生成随机矩阵
    A = np.random.randn(k, d)
    # 通过极分解得到酉矩阵 U
    U, _ = linalg.polar(A)  # [k, d]
    # 计算 EFT
    M = np.sqrt(k / (k - 1)) * (np.eye(k) - np.ones(k) / k) @ U  # [k, d]
    return M
```
