XGBoost 学习笔记
===
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2025-07-08%2016%3A53%3A13&color=yellowgreen&style=flat-square)

<!--END_SECTION:badge-->

- [Boosting 方法](#boosting-方法)
    - [AdaBoost 算法](#adaboost-算法)
    - [前向分步算法](#前向分步算法)
    - [目标函数](#目标函数)
- [学习算法：GBDT](#学习算法gbdt)
- [优化](#优化)
- [CART 树](#cart-树)


## Boosting 方法

**基本思路**
- 通过改变训练样本的权重，学习多个若学习器，然后将这些弱学习器组合成一个强学习器；

**两个基本问题**
1. 在每一轮训练中，如何调整训练样本的权重；
2. 如何将训练得到的一系列弱学习器组合成一个强学习器；

### AdaBoost 算法

- AdaBoost 是 Boosting 的一个代表性算法；  
- AdaBoost 对两个基本问题的解决方法：
    1. 提高上一轮分类错误样本的权重，降低分类正确样本的权重；
    2. 加权线性组合（**加法模型**）；具体地，弱分类器的误差越小，权重越大；

### 前向分步算法

### 目标函数

## 学习算法：GBDT
- 什么是 GBDT 算法？

## 优化


## CART 树
- CART 树（Classification And Regression Tree）可用于分类和回归，是常见的决策树算法；

- 回归树的几个基本概念：
    - 

回归树 
$$q(x) = j$$

函数表达式
$$I_j = \{ i | q(x_i) = j \}$$

