数据不平衡专题
===
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2025-07-08%2016%3A53%3A13&color=yellowgreen&style=flat-square)

<!--END_SECTION:badge-->

- [概述](#概述)
    - [评价指标](#评价指标)
    - [机器学习中的一般方法](#机器学习中的一般方法)
- [深度学习中常见的解决方法](#深度学习中常见的解决方法)
    - [数据层](#数据层)
        - [ROS（上采样）](#ros上采样)
        - [Two‑phase learning（两阶段学习）](#twophase-learning两阶段学习)
        - [Dynamic sampling（动态采样）](#dynamic-sampling动态采样)
        - [ROS, RUS, and two‑phase learning](#ros-rus-and-twophase-learning)
    - [算法层](#算法层)
        - [Mean Squared False Error (MFE) loss](#mean-squared-false-error-mfe-loss)
        - [Focal Loss](#focal-loss)
        - [Cost‑sensitive deep neural network (CSDNN)](#costsensitive-deep-neural-network-csdnn)
- [参考资料](#参考资料)

## 概述

- 数据不平衡的影响会随着问题复杂度的增加而增加；简单的线性可分问题不会受到数据不平衡的影响；
- 一个简单衡量数据集不平衡率的指标：
    $$\rho = \frac{\max_i\{|C_i|\}}{\min_i\{|C_i|\}}$$
    比如最大类别的样本数为 100，最小的为 10，则 $\rho = 10$；
- 需要注意的是，有时少数类别样本的绝对值比占比更重要；比如在一个包含 100 万样本的数据集中，即使某个类别只占 1%，也有 1 万条样本可供学习；
- 一些研究将不平衡问题看做是**对困难样本的学习**问题；在大多数场景下，可以认为两者的目标是一致的；

### 评价指标

- 在处理不平衡问题时，只使用准确率或错误率是不够的；此时占主导的是多数类别的样本；
- 常用指标计算公式
    - **混淆矩阵**
        | \                  | Actual positive     | Actual negative     |
        | ------------------ | ------------------- | ------------------- |
        | Predicted positive | True positive (TP)  | False positive (FP) |
        | Predicted negative | False negative (FN) | True negative (TN)  |
    - **Accuracy（准确率）**
        $$Accuracy = \frac{TP + TN}{TP + TN + FP + FN}$$
    - **Error Rate（错误率）**
        $$Error Rate = 1 − Accuracy$$
    - **Precision（精确率）**
        $$Precision = \frac{TP}{TP + FP}$$
    - **Recall（召回率）或 TPR（True Positive Rate，真阳率）**
        $$Recall = TPR = \frac{TP}{TP + FN}$$
    - **Selectivity 或 TNR（True Negative Rate，真阴率）**
        $$Selectivity = TNR = \frac{TN}{TN + FP}$$
    - **F-Measure**
        $$F_\beta=(1+\beta^2)\times \frac{Precision \times Recall}{(\beta^2 \times Precision) + Recall}$$
        $$F_1 = 2 \times \frac{Precision \times Recall}{Precision + Recall}$$
    - **G-Mean**
        $$G\text{-}Mean = \sqrt{TPR * TRN}$$ 
    - **Balanced Accuracy**
        $$Balanced Accuracy = \frac{1}{2} \times (TPR + TRN)$$ 
- TODO: 精读各指标的作用


### 机器学习中的一般方法

**数据层**
- 随机**下采样/欠采样**（Random Under-Sampling, RUS）：减少多数群体样本
    - 目标：保留有价值的信息（去除冗余的多数群体样本）
    - 常见方法：
        - 利用 K-NN（最近邻）选择需要丢弃的多数群体样本；
- 随机**上采样/过采样**（Random Over-Sampling, ROS）：增加少数群体样本
    - 目标：较少过拟合
    - 常见方法：
        - 利用插值生成新样本；
        - 先对样本进行 K-Means 聚类，再上采样；
- 相关工具：[scikit-learn-contrib/imbalanced-learn: A Python Package to Tackle the Curse of Imbalanced Datasets in Machine Learning](https://github.com/scikit-learn-contrib/imbalanced-learn)
- **一般结论**：
    - 下采样（RUS）效果普遍优于上采样（ROS）；
    - 采样效果高度依赖于学习器和评估指标，没有通用有效的采样方案；

**算法层**
- 相比从数据入手的方法，算法侧的方法**不会改变数据的分布**；
- 基本策略：通过调整不同类别的惩罚权重，从而减少样本偏置；
- 成本矩阵（Cost Matrix）

<!-- 
**混合方法**
- 集成学习 
 -->


## 深度学习中常见的解决方法

- 对浅层网络，有研究表明，在类别不平衡的场景下，少数类的梯度分量会远小于多数类的梯度分量；其结果就是训练过程中模型会快速降低多数类的误差，且通常会导致少数类的误差增加；
- 下面总结了目前深度学习中常见的、用于解决类别不平衡问题的方法，包括数据层面、算法层面和混合方法；
    - 对每种方法，讨论了该方法的**实现细节**，以及用于评估该方法的**数据集特征**；
    - 随后讨论了不同方法的优缺点，比如：类别不平衡的程度、结果的可解释性、相对性能、使用并推广到其他结构和问题的难度；


### 数据层
- 主要还是基于**下采样**（RUS）和**上采样**（ROS）；

#### ROS（上采样）
> 相关论文：The Impact of Imbalanced Training Data for Convolutional Neural Networks

- **数据集**
    - 基于 CIFAR-10 人工生成的 10 个数据集；
    - 最大 $\rho=2.3$；
- **做法**
    - 通过上采样（随机复制数据）使类别达到平衡；
- 本文的研究相对较早（2015），主要讨论了不平衡数据对深度学习模型的影响，在方法上没有更多创新；

#### Two‑phase learning（两阶段学习）
> 相关论文：Plankton classification on imbalanced large scale database via convolutional neural networks with transfer learning
- **数据集**
    - 数据来源：WHOI-Plankton
    - 103 个类别，340 万张图片；
    - $\rho > 650$，数量最多的前 5 个类别占 90%，第 5 大的类别仅占 1.3%，其他大多数类别都小于 0.1%；
- **实现细节**
    - 两阶段训练过程：
        - 一阶段：使用**阈值数据**（thresholded data）预训练；
            > 阈值数据：每个类别最多随机采样 N 个样本（论文中 N = 5000）；
        - 二阶段：使用全部数据微调；
- **有效性解释**：
    - 朴素的 RUS 方法直接丢弃多数类样本，这些被丢弃的样本不再参与到训练中，而这些样本可能是潜在有用的样本；
    - 两阶段训练方法，只在预训练阶段丢弃多数类样本，这保证了少数类样本这此时能得到更大的权重；同时在微调阶段允许模型观察到全部训练样本；
- **一些优化点**：
    - 作者没有提供预训练阶段更多信息，比如预训练的 epoch、预训练结束标准等；这些信息是重要的，因为预训练模型的状态（高偏差或高方差）必然会影响最终的结果；
    - 目前在预训练阶段只对多数类进行下采样，由于少数类的数据非常少，限制了 N 的大小，一个改进方法是同时加入对少数类的上采样结果，这样就可以进一步提高阈值 N 的大小；


#### Dynamic sampling（动态采样）
> 相关论文：Dynamic sampling in convolutional neural networks for imbalanced data classification

- **数据集**
    - 数据来源：作者自己收集的
    - 19 个类别，10000+ 图像；
    - $\rho = 500$；
    - 评价指标：Average F1、Weighted average F1
- **实现细节**
    - 实时数据增强：就是目前 CV 中的常规做法，在输入层对图片做变换后再 forward；
    - 迁移学习：基于预训练好的 Inception-V3 模型微调；
    - 动态采样：
        $$SampleSize(F_i,c_j) = \frac{1-f_{i,j}}{\sum_{c_k\in C}(1-f_{i,k})} \times N^*$$ 
        - 上式用于生成下一轮训练中各类别采样的数量；
        - $F_i$ 是一个向量，由每个类在第 $i$ 轮迭代后的 F1 分数组成；
        - $f_{i,j}$ 表示类别 $j$ 在第 $i$ 轮迭代后的 F1 分数；
        - $c_j$ 表示类别 $j$；
        - $N^*$ 表示类别的平均数量，即样本总数除以类别数；
        - 在下一轮迭代中，F1 较低的类别会以更高的比率被采样，以迫使学习器更多关注错误率较高的类别；
        - **模型融合**（Model Fusion）：在训练集上根据**是否使用动态采样**，训练两个模型；然后根据验证集上类别的正负比例设定一个阈值，根据阈值选择其中某个模型的结果，详见论文；
            > **动机**：原文认为使用动态采样训练得到的模型会在少数类上的效果更好，而不使用动态采样的模型会在多数类上效果更好，因此采用融合的方案；但是这里阈值的计算方法没有看懂；
- **有效性解释**：
    - 自适应调整采样率本质上就是在通过样本量调整类别权重；
    - 在每一轮训练中，由于高指标的类别数量少，低指标的类别数量多，将迫使模型将更多的学习权重放在低指标的数据上；
    - 因此该方法不仅适用于类别不平衡的问题，对于均衡但类别学习难度不同的数据集也有用；
- **一些优化点**：
    - 论文没有给出对比方法中具体的上采样和下采样细节，导致不能确定动态采样的方法是否能完全取代 ROS 和 RUS；
    - 该方法依赖于验证集的构建，对验证集的数据分布要求较高；
    - 可以尝试拓展到 CV 外的其他领域；


#### ROS, RUS, and two‑phase learning
> 相关论文： A systematic study of the class imbalance problem in convolutional neural networks.

- 本文比较了 7 种基于 ROS、RUS 和两阶段训练的方法；
    - 少数类上采样
    - 多数类下采样
    - 基于随机上采样的二阶段训练
    - 基于随机下采样的二阶段训练
    - 阈值法
    - 上采样+阈值法
    - 下采样+阈值法


### 算法层

- 主要思路：
    - 损失函数：促使少数类对损失做出更大的贡献；
    - 代价敏感学习（cost-sensitive learning）
    - 阈值移动（threshold moving）

#### Mean Squared False Error (MFE) loss
> 相关论文：Training deep neural networks on imbalanced data sets

- **数据集**
    - 基于 CIFAR-100（图像）和 20 Newsgroup（文本）人工构建的不平衡数据集；
    - 数据量：2000 - 3500 之间；
    - $\rho$ 在 5 到 20 之间；
- **背景&动机**
    - 均方误差损失（MSE Loss）很难在不平衡条件下捕捉到少数类群体的误差，此时多数类主导了损失函数；
    - 受到混淆矩阵的启发，提出 Mean False Error(MFE) Loss 和 Mean Squared False Error(MSFE) Loss，通过分别计算不同类别的 MSE Loss，来平衡少数类和多数类的误差；
- **方法**
    $$MFE = FPE + FNE$$
    $$MSFE = \frac{1}{2}((FPE + FNE)^2 + (FPE - FNE)^2) = FPE^2 + FNE^2$$
    - 其中 $FPE$ 为**假阳误差**（False Positive Error），$FNE$ 为**假阴误差**（False Negative Error），两者均为 MSE Loss；
- **存在问题**
    - 无论是 MFE Loss 还是 MSFE Loss，都是基于 MSE Loss，但是在分类问题上使用 MSE 损失的效果并不好；
        > [机器学习理论—损失函数（二）：MSE、0-1 Loss与Logistic Loss - 知乎](https://zhuanlan.zhihu.com/p/346935187)
- **改进**
    - 可以考虑把基础损失替换成交叉熵；

#### Focal Loss
> 相关论文：Focal loss for dense object detection

- **数据集**
    - 目标检测；
    - $\rho = 1000$，极端不平衡；
- **背景**
    - 希望提升 One-stage（如 SSD、YOLO） 方法的效果，达到 Two-stage（如 R-CNN） 的水平；
        > [目标检测专题(一) One-Stage方法 - 知乎](https://zhuanlan.zhihu.com/p/107780772)  
        > [目标检测专题(二) Two-Stage方法 - 知乎](https://zhuanlan.zhihu.com/p/107852736)
    - 分析认为不平衡问题是阻碍 One-stage 方法效果的主要原因；
    - 基于交叉熵，提出 Focal Loss 降低容易分类的样本对损失的影响；
- **方法**
    - 交叉熵
        $$CELoss = -\log(p_t)$$ 
    - Focal Loss
        $$Focal Loss= -\alpha_t(1-p_t)^\gamma\log(p_t)$$ 
    - Focal Loss 在交叉熵的基础上加入了**调制系数** $\alpha_t(1-p_t)^\gamma$
    - 其中 $\gamma$（> 0）为超参数，用于调整简单样本的权重的下降率；$\alpha_t$ 为类别权重用于提升少数类的重要性；论文中取 $\gamma=2, \alpha=0.25$
    - 简单解释：对于**易分类**的样本，当其概率 $p_t$ 接近 1，此时调制系数将趋向于 0，进而降低其对 loss 的影响；
- 相关分析
    - [从loss的硬截断、软化到focal loss - 科学空间|Scientific Spaces](https://kexue.fm/archives/4733)


#### Cost‑sensitive deep neural network (CSDNN)
> 相关论文


## 参考资料
- [Survey on deep learning with class imbalance | Journal of Big Data | Full Text](https://journalofbigdata.springeropen.com/articles/10.1186/s40537-019-0192-5)
