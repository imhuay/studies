BERT+CRF 等备忘
===
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2025-07-08%2016%3A53%3A13&color=yellowgreen&style=flat-square)

<!--END_SECTION:badge-->
> [ BERT中进行NER为什么没有使用CRF，我们使用DL进行序列标注问题的时候CRF是必备么？ - 知乎](https://www.zhihu.com/question/358892919)
- 加入 CRF 的原因？
    - 引入 CRF，是为了建模标注序列内部的依赖或约束；
    - CRF 中的转移概率矩阵，会考虑上个 label 来预测下一个 label；
- 可以去掉 CRF 吗？
    - 可以；如果模型的拟合能力足够强，...
- 标准的 CRF 有两类特征函数，一类是 ，一类是
- 在 BERT+CRF 中，第一类特征函数的计算由 BERT 取代，CRF 层仅提供第二类特征


CRF 和 HMM 的区别和联系？
- 都属于概率图模型；
- CRF是生成模型，HMM是判别模型；
- HMM是概率有向图，CRF是概率无向图；
- HMM求解过程可能是局部最优，CRF可以全局最优；
- HMM 假设：一是输出观察值之间严格独立（观察独立性假设），二是状态的转移过程中当前状态只与前一状态有关(齐次马尔科夫假设)
- CRF没有上述假设，所以CRF能容纳更多上下文信息；
- CRF的概率计算和解码过程和HMM相同，就是学习过程不同，HMM直接基于统计，CRF一般是迭代学习。


GBDT 和 XGBoost
- GBDT 是一种基于决策树的集成学习算法；XGBoost 是 GBDT 算法的一种高效实现，类似的还有 LightGBM 等；
- 基学习器：集成学习，GBDT 只使用决策树，而 XGBoost 还可以使用线性分类器；
- 优化器：GBDT 使用一阶导，XGboos 使用二阶导；
- 损失函数：XGBoost 在损失函数中加入了正则项，控制模型的复杂度；
- 其他优化：
    - 权重衰减：
    - 列采样：
    - 并行：


transformer encoder



```python
class Transformer(nn.Module):

    def __init__(self, d_head, n_head, d_model, d_ff, act=F.gelu):
        super().__init__()

        self.d = d_head
        self.h = n_head
        n = d_head * n_head
        self.Q = nn.Linear(n, n)
        self.K = nn.Linear(n, n)
        self.V = nn.Linear(n, n)
        self.O = nn.Linear(n, n)
        self.LayerNorm_1 = nn.LayerNorm(n)
        self.LayerNorm_2 = nn.LayerNorm(n)
        self.W_1 = nn.Linear(d_model, d_ff)
        self.W_2 = nn.Linear(d_ff, d_model)
        self.act = act
        self.dropout = nn.Dropout(0.2)

    def attn(self, x, mask):
        q, k, v = self.Q(x), self.K(x), self.V(x)
        q = einops.rearrange(q, 'B L (H D) -> B H L D', H=self.h)
        k = einops.rearrange(k, 'B L (H D) -> B H D L', H=self.h)
        v = einops.rearrange(v, 'B L (H D) -> B H L D', H=self.h)
        a = torch.softmax(q @ k / math.sqrt(self.d) + mask, dim=-1)  # [B H L L]
        o = einops.rearrange(a @ v, 'B H L D -> B L (H D)')
        o = self.O(o)
        return o
    
    def ffn(self, x):
        return self.dropout(self.W_2(self.dropout(self.act(self.W_1(x)))))

    def forward(self, x, mask):
        x = self.LayerNorm_1(x + self.dropout(self.attn(x, mask)))
        x = self.LayerNorm_2(x + self.dropout(self.ffn(x)))
        return x
```

最小的 k 个数
```python
class Solution:
    def GetLeastNumbers_Solution(self, tinput, k):
        
        def partition(a, lo, hi):
            if lo >= hi: return 
            
            p = a[lo]
            l, r = lo, hi
            while l < r:
                while l < r and a[r] >= p: r -= 1
                while l < r and a[l] <= p: l += 1
                a[l], a[r] = a[r], a[l]
            
            a[lo], a[l] = a[l], a[lo]
            
            # 因为只需要前 k 个数，所有加上 if，去掉 if 就是标准的快排
            if l > k - 1: partition(a, lo, l - 1)
            if l < k - 1: partition(a, l + 1, hi)
        
        partition(tinput, 0, len(tinput) - 1)
        return tinput[: k]
```
