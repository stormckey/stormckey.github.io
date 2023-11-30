# 感知机

## 原始形式

感知机的结构如下图所示，被视为是最简单的前馈神经网络，是一种二元线性分类器.

!!! example ""
    ![](images/Perceptron/2023-11-20-11-24-41.png#pic)

下面给出形式化表述：

!!! definition "感知机"
    给定数据集$\{(x_i，y_i)\}$，其中$y_i \in \{1，-1\}$是数据标签，我们需要找到一组$(w，b)$使得函数$f(x) = sign(w \cdot x + b)$的损失函数最小：

    $$
       \min L(w，b) = - \sum_{i=1}^{n} y_i(w \cdot x_i + b)
    $$

注意上文中的$sign$函数，它的定义如下：

$$
    sign(x) = \left\{
    \begin{aligned}
        1， & x \geq 0 \\
        -1， & x < 0
    \end{aligned}
    \right.
$$

可以看出，如果$y_i$和$f(x)$若是符号相同（也就是分类正确），那么$y_i(w \cdot x_i + b)$的值就是 1，反之则是-1.因此我们的目标就是尽可能最大化所有$y_i(w \cdot x_i + b)$求和的值，这也等效于最小化其负数.（该领域约定俗成就是写成最小化优化目标，最小化和最大化之间只要加一个负号就可以互相转化）

我们可以用 SGD（Stochastic Gradient Descent）来求解上述问题，损失函数的梯度为：

\begin{aligned}
    &\nabla_w L(w，b) = - \sum_{i=1}^{n} y_i x_i \\
    &\nabla_b L(w，b) = - \sum_{i=1}^{n} y_i
\end{aligned}

从数据集中随机选取一个样本$(x_i，y_i)$，更新参数：

\begin{aligned}
    & w = w + \eta y_i x_i\\
    & b = b + \eta y_i \\
\end{aligned}

直到没有误分类点.其中$\eta \in (0，1]$是学习率.

## 收敛性

可以证明，感知机的误分类次数 K 存在一个上界，即；

\begin{aligned}
    & K \leq (\frac{R}{\gamma})^2 \\
    & R = \max_{1 \leq i \leq n} ||x_i|| \\
    & \gamma = \min_{1 \leq i \leq n} y_i(w^* \cdot x_i + b^*)
\end{aligned}

其中$w^*，b^*$是最优解，$R$是数据集中样本点的最大范数，$\gamma$是数据集中所有样本点到超平面的最小距离.
对证明过程感兴趣的可以看书，这里不展开.

## 对偶形式

假设我们初始化参数为$w_0 = 0，b_0 = 0$，那么我们可以得到：

\begin{aligned}
    & w = \sum \eta y_i x_i \\
    & b = \sum \eta y_i
\end{aligned}

其中$\eta$是学习率.因为我们是从 0 开始每次都往参数上加一定的更新值，所以上式自然成立.

假设其中第 i 个数据点在 SGD 中被随机选中了$n_i$次，那么它因此导致了$n_i$次参数的更新，我们可以把上式写成：

\begin{aligned}
    & w = \sum_{i=1}^{n} \eta n_i y_i x_i \\
    & b = \sum_{i=1}^{n} \eta n_i y_i
\end{aligned}

令$\alpha_i = \eta n_i$，那么我们可以得到：

\begin{aligned}
    & w = \sum_{i=1}^{n}\alpha_i y_i x_i \\
    & b = \sum_{i=1}^{n}\alpha_i y_i
\end{aligned}

那么我们的分类函数就可以写成：

$$
    f(x) = sign(\sum_{i=1}^{n}\alpha_i y_i（ x_i \cdot x ） + \sum_{i=1}^{n}\alpha_i y_i)
$$

每步 SGD 中我们只需要更新$\alpha_i$:

$$
    \alpha_i = \alpha_i + \eta
$$

可以看到我们的分类函数中只有$\alpha_i$需要每次更新，除此之外还有大量的 x 的内积运算，为了方便，我们可以把 x 的内积预先计算出来，这被称作 Gram 矩阵：

!!! info "Gram 矩阵"
    给定 n 个向量$x_1，x_2，...，x_n$，那么 Gram 矩阵$G$是由这些向量所有可能的内积组成的矩阵，即：

    $$
        g_{ij} = x_i \cdot x_j
    $$
