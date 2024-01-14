# 奇异值分解

## 动机

我们希望找到一种对任意非零实矩阵(1)的分解方式，使得其可以被对角化，奇异值分解（Singular Value Decomposition，SVD）就是这样一种分解方式。
{ .annotate }

1.  即使是非方阵

形式化的表述如下：

对于 \( A_{m \times n} \) ，我们希望找到

$$
    A_{m \times n} = U_{m \times m} \Sigma_{m \times n} V_{n \times n}^T
$$

其中 \( U \) 和 \( V \) 是正交矩阵(1)，其中$U$的列向量称为左奇异向量而$V$的列向量被称为右奇异向量。
{ .annotate }

1.  也就是与自己的转置矩阵相乘得到单位矩阵

\( \Sigma \) 是对角矩阵，对角线上的元素非负并且降序排列，它们被称为奇异值。因为并不是方阵，所以对角线元素个数为 $min(m,n)$。

## 思想

不失一般性，假设$m>n$，那么对角矩阵可以表示为$\Sigma = \begin{bmatrix} \Sigma' \\ 0 \end{bmatrix}$, 而$\Sigma'$中并不是每个对角线元素都为 0，所以我们可以假设所有非零元素构成一个对角矩阵$\Sigma_1$，使得$\Sigma' = \begin{bmatrix} \Sigma_1 & 0 \\ 0 & 0 \end{bmatrix}$，变量$r = r(\Sigma_1) = r(A)$。

那么对应的，我们可以把$U$和$V$分成两个子矩阵$U = [U_1 \ U_2] \ \ \ \ U_1 = [ u_1 \dots u_r] \ \ \ \ U_2 = [u_{r+1} \dots u_m]$，$V = [V_1 \ V_2] \ \ \ \ V_1 = [ v_1 \dots v_r] \ \ \ \ V_2 = [v_{r+1} \dots v_n]$。

代回原式，可以得到

$$
    A = U \Sigma V^T = [U_1 \ U_2] \begin{bmatrix} \Sigma_1 & 0 \\ 0 & 0 \end{bmatrix} [V_1 \ V_2]^T = U_1 \Sigma_1 V_1^T
$$

所以一旦确定了$U_1, \Sigma_1, V_1$就可以通过乘积还原出$A$，因此找到这三个矩阵将是构造的重点。

而找到这三个矩阵之后，我们就只需要把$U_1,V_1$扩充成正交矩阵即可。

## 构造

由于我们已经知道了如何对实对称矩阵进行特征值分解，所以我们希望可以从 $A$ 构造出来一个实对称矩阵，然后对其进行特征值分解，这样就可以得到 $ A $ 的奇异值分解了。

显然，矩阵 $ A^T A $ 是一个实对称矩阵，对其进行特征值分解，得到

$$
    V^T (A^T A) V = \Lambda
$$

$\Lambda$ 特征值均非负(1)并且 $r(\Lambda) = r(A^T A) = r(A) = r$
{.annotate}

1.  $\|Ax\|^2 = x^T A^T A x = \lambda x^T x = \lambda \|x\|^2$

    $\lambda = \frac{\|Ax\|^2}{\|x\|^2} \geq 0$

那么我们可以对 $\Lambda$ 的特征值进行一个非减的排序 $\lambda_1 \geq \lambda_2 \geq \dots \geq \lambda_r \ \ \ \ \lambda_{r+1} = \dots = \lambda_n = 0$  并且定义奇异值为 $\sigma_i = \sqrt{\lambda_i}$

依据对应的特征值是不是 0，我们可以把$V$分成两个子矩阵 $V = [V_1 \ V_2] \ \ \ \ V_1 = [ v_1 \dots v_2] \ \ \ \ V_2 = [v_{r+1} \dots v_n]$

对应的，我们也对 $\Sigma$ 进行划分，$\Sigma = \begin{bmatrix} \Sigma_1 & 0 \\ 0 & 0 \end{bmatrix} \ \ \ \ \Sigma_1 = \begin{bmatrix} \sigma_1 & & \\ & \ddots & \\ & & \sigma_r \end{bmatrix}$

将分割后的矩阵代回原式，得到

$$
    V^T(A^T A)V = [V_1 V_2]^T (A^T A) [V_1 V_2] = \begin{bmatrix} V_1^T A^T A V_1 & V_1^T A^T A V_2 \\ V_2^T A^T A V_1 & V_2^T A^T A V_2 \end{bmatrix} = \begin{bmatrix} \Sigma_1^2 & 0 \\ 0 & 0 \end{bmatrix} = \Lambda
$$

不难发现 $AV_2 = 0$，也就是$V_2$在$A$的零空间中。

这也就意味着

$$
    A = A I = A(V^T V) = A (V_1 V_1^T + V_2 V_2^T) = A V_1 V_1^T + A V_2 V_2^T = A V_1 V_1^T
$$

!!! tip "回想"
    回想我们之前的思路，我们需要找到三个矩阵，使得

    $$
        U_1 \Sigma_1 V_1^T = A
    $$

    而我们又推出了$A = A V_1 V_1^T$，所以我们需要找到

    \begin{align*}
        U_1 \Sigma_1 V_1^T &= A V_1 V_1^T \\
        U_1 \Sigma_1 &= A V_1 \\
    \end{align*}

不难发现，在已经有了$V_1, \Sigma$ 的情况下， $U_1$其实是很好构造的，我们只需要对 $\forall j \in [1,r]$ ，令$u_j = \frac{1}{\sigma_j} A v_j$，那么$U_1 = [u_1 \dots u_r]$就是我们需要的矩阵了。

最后我们只需要把$U_1$扩充成正交矩阵$U = [U_1 \ U_2]$，便可以得到

$$
    A = U \Sigma V^T
$$

## 变体

不难发现，我们只需要$U_1, \Sigma_1, V_1$就可以还原出$A$了，所以我们可以只取这三个矩阵作为一个分解，这就是紧奇异值分解。

更进一步的，如果我们连 r 维的矩阵都无法接受的话，我们可以选择只保留前$k$维，这样得到的就是截断奇异值分解。截断奇异值分就无法准确的还原出$A$了，但是可以证明，截断奇异值分解是弗洛贝尼乌斯范数(1)下的最优近似。
{.annotate}

1.  $\|A\|_F = \sqrt{\sum_{i=1}^m \sum_{j=1}^n a_{ij}^2}$

## 性质

左右奇异向量互相转化：

\begin{align*}
    \sigma_j u_j &= A v_j  \ \ \ \ \forall j \in [1,r] \\
    A^T u_j &= \sigma_j v_j \ \ \ \ \forall j \in [1,r]\\
\end{align*}

右奇异向量$v_1, \dots, v_r$是$A^T$的正交基，$v_{r+1}, \dots, v_n$是$N(A)$的正交基。

左奇异向量$u_1, \dots, u_r$是$A$的正交基(1)，$u_{r+1}, \dots, u_m$是$N(A^T)$的正交基。
{.annotate}

1.  \begin{align*}
        u_i^T u_j  &= ( \frac{1}{\sigma_i} v_i^T A^T) ( \frac{1}{\sigma_j A v_j}) \\
                    &= \frac{1}{\sigma_i \sigma_j} v_i^T A^T A v_j \\
                    &= \frac{1}{\sigma_i \sigma_j} v_i^T v_j (v_j^T A^T A v_j) \\
                    &= \frac{1}{\sigma_i \sigma_j} \sigma_j^2 v_i^T v_j \\
                    &= \delta_{ij}
    \end{align*}

$A^T A$和$A A^T$的特征值分解存在，并且可以方便的得到：

\begin{align*}
    A^T A = (U \Sigma V^T)^T (U \Sigma V^T) = V \Sigma^T U^T U \Sigma V^T = V \Sigma^T \Sigma V^T \\
    A A^T = (U \Sigma V^T) (U \Sigma V^T)^T = U \Sigma V^T V \Sigma^T U^T = U \Sigma \Sigma^T U^T
\end{align*}

## 几何解释

作为一个 m*n 矩阵，我们可以吧$A$理解成一个从$\mathbb{R}^n$到$\mathbb{R}^m$的线性变换，而奇异值分解就是把这个线性变换分解成三个部分：

-   $V^T$：从$\mathbb{R}^n$到$\mathbb{R}^n$的旋转变换
-   $\Sigma$：从$\mathbb{R}^n$到$\mathbb{R}^m$的缩放变换
-   $U$：从$\mathbb{R}^m$到$\mathbb{R}^m$的旋转变换

因为$U,V$都是正交矩阵，所以它们天然的对应一个旋转变换，而$\Sigma$作为对角矩阵，对应一个缩放变换。

奇异值分解的存在性隐含了这种变换分解的存在性，也就是任意一个非零的实变换都可以分解为这三个变换的组合。

![](images/SVD/image.png#pic)


