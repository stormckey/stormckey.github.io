# 主成分分析

## 动机

设想我们有一组线性的二维数据点，如下图所示

![](images/PCA/Screenshot_2024-01-14-11-45-04-320_com.desmos.cal.jpg#pic)

那么我们存储每个点都使用了两个维度的数据。但是由于这些点都分布在同一条直线上，所以我们其实可以只用一个维度来表示这些点，具体来说，我们把 x 轴旋转到这条直线上，y 轴旋转到与直线垂直，那么所有的点的
y 坐标都是 0，自然就可以只用一维度的数据(2)记录这些点了。这样我们就实现了降维，我们用一维的数据来存储本来两维的信息，并且是无损的(1)。
{.annotate}

1.  无损的意思就是我们可以完美的还原出原数据。
2.  横坐标

然而这只是线性的数据上的情况，如果数据并非线性，比如下图这样的：

![](images/PCA/image.png#pic)

那么显然我们像之前那样旋转坐标轴，是无法只用一个维度完美的表示这些数据的。但是我们隐隐可以感觉到，如果只让用一个维度来表示这些点的话，最好的方式应该是使用 x 轴旋转到椭圆长轴后的横坐标。

事实上正是如此！我们不妨把这种思想用更数学化的方式表述出来。我们希望在原数据集中彼此分隔的数据点不要混在一起。对于线性的例子，我们选择的旋转后的 x 轴正是使得数据投影最分散的一种方式，如果我们渐渐旋转我们的选择的话，会发现数据点会越来越聚拢，直至我们最终旋转到与该直线垂直的位置上，此时所有的点都被投影到同一个点上，我们就丢失了所有的信息。

不难发现，我们最后是使用数据点到某条直线的投影来表示这些点，而我们希望这些投影尽可能分散，也就是方差最大。

主成分分析（Principal Component Analysis，PCA）就是这样一种降维的方法。具体来说，PCA 会选出彼此正交的 N 个单位向量(1)，其中第一个单位向量是使得数据投影方差最大的方向，第二个单位向量是在与第一个单位向量正交的方向上使得数据投影方差最大的方向，以此类推。这些单位向量就被称作的主成分，我们可以把原数据投影到这些主成分上，从而实现降维的同时，最大限度的保留原数据的方差(2)。
{.annotate}

1.  也就对应 N 条直线，或者说 N 个轴
2.  原数据的反差也就是原数据的信息


## 总体主成分分析

### 一般分析
给定$x = (x_1, \dots, x_n)^T$，是 m 维随机变量，其对应的协方差矩阵$\Sigma = E[(x-\mu)(x-\mu)^T]$，其中$\mu = E[x]$，我们希望找到一个单位向量$\alpha$，使得 x 在$\alpha$上的投影$y_i = \alpha^T x$的方差最大。对于$y_i$而言

\begin{align*}
    E(y_i) &= \alpha_i^T \mu \\
    Var(y_i) &= \alpha_i^T \Sigma \alpha_i \\
    Cov(y_i, y_j) &= \alpha_i^T \Sigma \alpha_j
\end{align*}

### 第一主成分
先求第一主成分，我们希望找到使得$y_1$方差最大的$\alpha_1$，也就是：

\begin{align*}
    \max_{\alpha_1} \alpha_1^T \Sigma \alpha_1 \\
    s.t. \alpha_1^T \alpha_1 = 1
\end{align*}

利用拉格朗日乘子法，我们可以得到：

\begin{align*}
    \alpha_1^T \Sigma \alpha_1 - \lambda (\alpha_1^T \alpha_1 - 1) = 0 \\
\end{align*}

对$\alpha_1$求导，得到：

\begin{align*}
    \Sigma \alpha_1 - \lambda \alpha_1 = 0 \\
\end{align*}

这就意味着，$\alpha_1$是$\Sigma$的特征向量，$\lambda$是对应的特征值。所以

$$
    \alpha_1^T \Sigma \alpha_1 = \lambda
$$

所以我们只需要找到$\Sigma$的最大特征值$\lambda_1$和对应的特征向量$\alpha_1$就可以了。该主成分对应的方差为$\lambda_1$。

### 其余主成分

第二主成分要在要求$\alpha_2^T x$与$\alpha_1^T x$正交的情况下，找到使得$\alpha_2^T x$方差最大的$\alpha_2$，也就是：

\begin{align*}
    \max_{\alpha_2} \alpha_2^T \Sigma \alpha_2 \\
    s.t. \alpha_2^T \alpha_2 = 1 \\
    \alpha_2^T \alpha_1 = 0
\end{align*}

写出拉格朗日函数：

\begin{align*}
    \alpha_2^T \Sigma \alpha_2 - \lambda_1 (\alpha_2^T \alpha_2 - 1) - \lambda_2 (\alpha_2^T \alpha_1 - 0) = 0 \\
\end{align*}

对$\alpha_2$求导并且令其为零，得到

\begin{align*}
    \Sigma \alpha_2 - \lambda_1 \alpha_2 - \lambda_2 \alpha_1 = 0 \\
\end{align*}

左乘$\alpha_1^T$后得到

\begin{align*}
    \alpha_1^T \Sigma \alpha_2 - \lambda_1 \alpha_1^T \alpha_2 - \lambda_2 \alpha_1^T \alpha_1 = 0 \\
    \lambda_2 = 0
\end{align*}

把$\lambda_2$代回得到

\begin{align*}
    \Sigma \alpha_2 - \lambda_1 \alpha_2 = 0 \\
\end{align*}

同样的，$\alpha_2$是$\Sigma$的特征向量，$\lambda_1$是对应的特征值。所以我们只需要找第二大的特征值$\lambda_2$和对应的特征向量$\alpha_2$就可以了。对应的方差为$\lambda_2$。

!!! tip "结论"
    x 的第 k 个主成分是$\alpha_k^T x$，其中$\alpha_k$是$\Sigma$的第 k 大特征值对应的特征向量。对应的方差为$\lambda_k$。

    求主成分分析之前可以先对随机变量进行规范化(1)
    {.annotate}

    1.  $x_i^* = \frac{x_i - E(x_i)}{\sqrt{var(x_i)}}$

### 性质

- $Cov(y) = diag(\lambda_1, \dots, \lambda_n)$，也就是说，主成分之间是不相关的。
- $tr(\Sigma) = \Sigma \lambda_i = \Sigma \sigma_{ii}$，也就是说，主成分的方差之和等于原协方差矩阵的迹。
- $\rho(y_k,x_i) =\frac{\sqrt{\lambda_k}\alpha_{ik}}{\sqrt{\sigma_{ii}}}$，这被称为因子负荷量。

## 样本主成分分析

如果我们拥有的不是个随机变量而是一些样本点的话，我们就需要进行样本主成分分析：

假设我们对随机变量$x = (x_1, \dots, x_m)^T$进行了 n 次观测，每次观测得到一个样本$x_j = (x_{1j}, \dots, x_{mj})^T$，我们可以得到样本均值$\bar{x} = \frac{1}{n} \sum_{j=1}^n x_j$，样本协方差矩阵$S = \frac{1}{n-1} \sum_{j=1}^n (x_j - \bar{x})(x_j - \bar{x})^T$。

对于一个单位向量$\a_i$，可以把 x 进行投影得到$y_i = \a_i^T x$。其均值为$\bar{y_i} = \a_i^T \bar{x}$，方差为$var(y_i) = \a_i^T S \a_i$,协方差为$cov(y_i, y_j) = \a_i^T S \a_j$。

那么样本主成分分析的步骤如下：

- 首先对样本进行规范化，$x_{ij} = \frac{x_{ij} - \bar{x_i}}{\sqrt{s_{ii}}}$ 得到 X
- 然后计算相关矩阵$R = \frac{1}{n-1} X X^T$
- 求相关矩阵的 k 个特征值$\lambda_1, \dots, \lambda_k$和对应的单位特征向量$\a_1, \dots, \a_k$
- 利用单位特征向量进行投影，就得到了前 k 个主成分。

## 奇异值法

- 令 $X' = \frac{1}{\sqrt{n-1}} X$
- 进行截断奇异值分解，$X' = U \Sigma V^T$
- 样本主成分矩阵就是： $Y = V^T X$





