---
comments: true
---

# 聚类方法

## 一些定义

!!! definition "样本间距"
    === "闵可夫斯基近距离"
        $$
            d_{ij} = \left( \sum_{k=1}^p \left| x_{ik} - x_{jk} \right|^r \right)^{\frac{1}{r}}
        $$
    === "马氏距离"
        首先计算协方差矩阵S
        $$
            S = \frac{1}{n-1} \sum_{i=1}^n (x_i - \bar{x})(x_i - \bar{x})^T
        $$
    === "相关系数"
        $$
            r_{ij} = \frac{S_{ij}}{\sqrt{S_{ii}S_{jj}}}
        $$
    === "夹角余弦"
        $$
            \cos \theta_{ij} = \frac{x_i^T x_j}{\sqrt{x_i^T x_i x_j^T x_j}}
        $$



