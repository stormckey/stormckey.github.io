# 支持向量机

!!! warning
    很多人都吐槽，支持向量机这个名字起的依托

## 模型描述

对于数据集$\{(x_i，y_i)\}$，其中$x_i \in \mathbb{R}^n， y \in \{1，-1\}$，我们希望找到一个超平面$w\cdot x + b = 0$将数据集分开.

!!! definition "实例点到超平面的几何间隔"
    $$
        \gamma_i = \frac{y_i(w\cdot x_i + b)}{\|w\|}
    $$

    可以看出，其绝对值也就是点到直线距离

!!! definition "实例点到超平面的函数间隔"
    $$
        \hat{\gamma_i}   = y_i(w\cdot x_i + b)
    $$

    可以看出，其绝对值也就是函数间隔除去了$||w||$这个因素

![](images/Support_Vector_Machine/2023-11-25-23-37-51.png#pic)

上述的变量的绝对值含义都表示某种距离，而符号表示分类正确与否，分类正确时间隔为正，分类错误时间隔为负

给定一组数据点和一个超平面，我们可以计算出各个函数间隔和几何间隔.但是如果我们成比例的同时放缩 w 和 b，那么超平面和几何间隔都完全不变，但是所有点的函数间隔都会随着 w 的变化而变化，因为函数间隔其实就是几何间隔（不变）乘上 w 的模（正在被成比例放缩）

为了提高分类的确信度和泛化能力，我们希望最大化最小几何间隔，也就是尽量提高所有点到超平面的距离的下界，也就是让所有点都尽可能离超平面远一点（离超平面很近的话，稍微有一点扰动就容易被分成另一类）

于是我们写出优化目标

\begin{aligned}
    \underset {w，b}{\operatorname{max}} & \quad \gamma \\
    s.t. & \quad y_i(w\cdot x_i + b) \geq \gamma， i = 1，2，...，N \\
\end{aligned}

其中的$\gamma = \underset {i}{\operatorname{min}} \gamma_i$，也就是最小几何间隔

观察到$\gamma\|w\| = \hat{\gamma}$，我们可以将上述优化目标转化为

\begin{aligned}
    \underset {w，b}{\operatorname{max}} & \quad \frac{\hat{\gamma}}{\|w\|} \\
    s.t. & \quad y_i(w\cdot x_i + b) \geq \hat{\gamma}， i = 1，2，...，N \\
\end{aligned}

因为我们可以通过成比例的放缩 w 和 b 来调节$\hat{\gamma}$，我们就放缩$w$使得$\hat{\gamma} = 1$，上述优化目标转化为

\begin{aligned}
    \underset {w，b}{\operatorname{max}} & \quad \frac{1}{\|w\|} \\
    s.t. & \quad y_i(w\cdot x_i + b) \geq 1， i = 1，2，...，N \\
\end{aligned}

求解上述优化问题可得到最优解$w^*，b^*$，构成最优分离超平面，可以证明，该超平面存在且唯一，那些离超平面最近的点就被称为支持向量

## 模型求解

### 对偶问题

#### 写出对偶问题

拉格朗日函数为：

$$
    L(w，b，\alpha) = \frac{1}{2}||w||^2 - \sum_{i=1}^{N}\alpha_iy_i(w\cdot x_i + b) + \sum_{i=1}^{N}\alpha_i
$$

我们将最小最大问题转化为最大最小问题，写出对偶问题：

$$
    \underset {\alpha}{\operatorname{min}} \underset {w，b}{\operatorname{max}} L(w，b，\alpha) \rightarrow \underset {\alpha}{\operatorname{min}} \underset {w，b}{\operatorname{max}} L(w，b，\alpha)
$$

#### 极小化

我们需要让$\nabla_w L(w，b，\alpha) = 0$和$\nabla_b L(w，b，\alpha) = 0$，也就是

\begin{aligned}
    & w = \sum_{i=1}^{N}\alpha_i y_i x_i \\
    & 0 = \sum_{i=1}^{N}\alpha_i y_i \\
\end{aligned}

带回原式中，得到：

$$
    L(w，b，\alpha) = \sum_{i=1}^{N}\alpha_i - \frac{1}{2}\sum_{i=1}^{N}\sum_{j=1}^{N}\alpha_i\alpha_jy_iy_j(x_i\cdot x_j)
$$

#### 极大化

在极小化之后，剩下的问题就是

\begin{aligned}
    \underset {\alpha}{\operatorname{max}} & \quad L(\alpha) =  \sum_{i=1}^{N}\alpha_i - \frac{1}{2}\sum_{i=1}^{N}\sum_{j=1}^{N}\alpha_i\alpha_jy_iy_j(x_i\cdot x_j) \\
    s.t. & \quad \sum_{i=1}^{N}\alpha_i y_i = 0 \\
    & \quad \alpha_i \geq 0， i = 1，2，...，N \\
\end{aligned}

通过某种方式求解上述问题，我们得到最优解$\alpha^*$

### 原始问题

#### 应用 KKT 条件

有了对偶问题的最优解$\alpha^* = (\alpha_1^*，\alpha_2^*，...，\alpha_N^*)$，应用 KKT 条件：

\begin{align}
    & \alpha_i^* \geq 0 \tag{1}\\
    & y_i(w^*\cdot x_i + b^*) - 1 \geq 0 \tag{2}\\
    & \alpha_i^*(y_i(w^*\cdot x_i + b^*) - 1) = 0 \tag{3}\\
    & \nabla_w L(w^*，b^*，\alpha^*) = w^* - \sum_{i=1}^{N}\alpha_i^* y_i x_i = 0 \tag{4}\\
    & \nabla_b L(w^*，b^*，\alpha^*) = \sum_{i=1}^{N}\alpha_i^* y_i = 0 \tag{5}\\
\end{align}

若$\alpha^* = 0$，由(4)可以推出$w^* = 0$，显然不对，所以$\alpha^*$不全为零

若$\alpha_i^* > 0$，由(3)可以推出$y_i(w^*\cdot x_i + b^*) = 1$，回忆前文我们已经令$\hat{\gamma} = 1$，所以 j 的函数间隔跟最小函数间隔相等，每个 j 都因此成为一个支持向量，其中既有正例也有反例

#### 求最优 w，b

利用支持向量，我们可以得到

\begin{align}
    & w^* = \sum_{i=1}^{N}\alpha_i^* y_i x_i \\
    & b^* = y_j - \sum_{i=1}^{N}\alpha_i^* y_i (x_i\cdot x_j) \\
\end{align}

#### 得到分离函数

利用最优解，我们可以得到分离函数

$$
    f(x) = sign(\sum_{i=1}^{N}\alpha_i^* y_i (x_i\cdot x) + b^*)
$$

以上便是求解二次规划问题得到最优间隔超平面的方法，其中只有对偶问题中的求的最优$\alpha^*$的方法没有阐明，后面会给出

## 软间隔

一般而言，由于噪声的干扰，我们很难直接拿到一个线性可分的数据集，而是一个近似线性可分的数据集，我们去掉大部分的噪点后可以做到线性可分，但是这些噪点实际上是跑到了支持向量以内甚至超平面对面的，这意味着

$$
    y_i(w\cdot x_i + b) \geq 1 - \xi_i \quad i = 1，2，...，N (\xi_i \geq 0 )
$$

也就是说，并非所有点的函数间隔都大于 1 了（函数间隔为 1 的是支持向量，不大于一就位于支持向量以内了），

当然，我们不能允许无限制的松弛，不然所谓的其他向量都可以随意跑到支持向量以内的话，支持向量也就没有意义的，我们进形正则化

$$
 \underset {w，b，\xi}{\operatorname{min}} \quad \frac{1}{2}||w||^2 + C\sum_{i=1}^{N}\xi_i \\
$$

其中的 C 是一个我们手动设置的惩罚参数

我们的对偶问题随之变成：

\begin{aligned}
    \underset {\alpha}{\operatorname{max}} & \quad L(\alpha) =  \sum_{i=1}^{N}\alpha_i - \frac{1}{2}\sum_{i=1}^{N}\sum_{j=1}^{N}\alpha_i\alpha_jy_iy_j(x_i\cdot x_j) \\
    s.t. & \quad \sum_{i=1}^{N}\alpha_i y_i = 0 \\
    & \quad 0 \leq \alpha_i \leq C， i = 1，2，...，N \\
\end{aligned}

其中由于松弛条件，我们极小化的过程中新增了以下的约束：

\begin{aligned}
    \nabla_{\xi_i} L(w，b，\alpha，\xi) = C - \alpha_i - \mu_i = 0  \quad i = 1，2，...，N \\
    \mu_i \geq 0 \quad i = 1，2，...，N \\
\end{aligned}

这也是上述条件中出现$\alpha_i \leq C$的原因

同样求解最优解$\alpha^*$，然后带回原式，得到最优解$w^*，b^*，\xi^*$，构成最优分离超平面

那些被松弛的点的位置和$\xi$的的关系为：

![](images/Support_Vector_Machine/2023-11-26-00-47-33.png#pic)


## 核函数

我们想要把点$x， z \in \mathbb{R}^n$映射到一个更高维的空间，也就是($\phi(x)$被映射到更高维），在这个映射中，我们需要保证高维空间中二者的点积是原空间中点积的函数，也就是

$$
    K(x，z) = \phi(x)\cdot \phi(z)
$$

一般而言，给定这个把原内积映射到高维内积的 K 就可以了，不用具体给出把向量映射到高位向量的$\phi()$

在对偶问题中，我们注意到$x_i$之间只有内积，所以我们就直接用映射后的高位内积进行替换

$$
    \underset {\alpha}{\operatorname{max}} \quad L(\alpha) =  \sum_{i=1}^{N}\alpha_i - \frac{1}{2}\sum_{i=1}^{N}\sum_{j=1}^{N}\alpha_i\alpha_jy_iy_jK(x_i，x_j) \\
$$

!!! info "常用核函数"
    多项式核函数

    $$
        K(x，z) = (x\cdot z + 1)^p
    $$

    高斯核函数(KBF)

    $$
        K(x，z) = \exp(-\frac{||x-z||^2}{2\sigma^2})
    $$

## SMO 算法

最后我们给出 SMO 算法，这是一种具体求解上述的$\alpha^*$的数值方法.

输入：数据集$D = \{(x_i，y_i)\}$，核函数$K(x，z)$，容忍度$\epsilon$

- 初始化$\alpha = 0$，k = 0
- 取优化变量$\alpha_1，\alpha_2$，解析求解最优化问题，更新$\alpha_1，\alpha_2$
- 若在容忍度$\epsilon$内满足：

    \begin{aligned}
        & \sum_{i=1}^{N}\alpha_i y_i = 0 \\
        & 0 \leq \alpha_i \leq C， i = 1，2，...，N \\
        & y_i(g(x_i)) = \left\{
        \begin{aligned}
            & \geq 1， \alpha_i = 0 \\
            & = 1， 0 < \alpha_i < C \\
            & \leq 1， \alpha_i = C \\
        \end{aligned}
        \right.
    \end{aligned}

    则令$\alpha = (\alpha_1，\alpha_2，...，\alpha_N)$，退出循环
