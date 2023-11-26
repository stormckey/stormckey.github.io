---
comments: true
---

# 提升方法

## AdaBoost

输入：$\{(x_i,y_i)\}$,一种弱学习算法
输出：最终分类器 G(x)

- 初始化训练数据的权值分布

    $$
        D_1 = (w_{11},\cdots,w_{1i},\cdots,w_{1N}),w_{1i} = \frac{1}{N},i=1,2,\cdots,N
    $$

- 运行弱学习算法，得到弱分类器$G_m(x)$
    
    计算误差率 : $e_m = \sum_{i=1}^{N} P(G_m(x_i) \neq y_i) = \sum_{i=1}^{N} w_{mi}I(G_m(x_i) \neq y_i)$

    该分类器的权重为：$\alpha_m = \frac{1}{2} \log \frac{1-e_m}{e_m}$
    
    更新新一轮的权重，其中每个样本的权重为：$w_{m+1,i} = \frac{w_{mi}}{Z_m} \exp(-\alpha_m y_i G_m(x_i))$ （可以看到如果分类正确，那么权重会减小，如果分类错误，那么权重会增大）

- 重复第二步，直到强分类器$G(x) = \sum_{m=1}^{M} \alpha_m G_m(x)$已经满足分类要求

## 提升树

提升树是以决策树/回归树为基分类器的假发模型。

我们定义一个前行分步为：

$$
    f_m(x) = f_{m-1}(x) + T(x;\Theta_m)
$$

其中新树的参数通过经验风险极小化进行更新：

$$
    \Theta_m = \underset{\Theta}{\operatorname{argmin}} \sum_{i=1}^{N} L(y_i,f_{m-1}(x_i) + T(x_i;\Theta))
$$

对于回归树，我们写出平方损失函数：

$$
    L = (y - f(x))^2 = (y - f_{m-1}(x) - T(x;\Theta))^2 = [r - T(x;\Theta)]^2
$$

也就是说我们只要新训练一个树 T 来拟合餐叉$r = y - f_{m-1}(x)$就可以了。

## 梯度提升

对于一般的损失函数（非平方损失函数）,不是那么容易找到残差

通常我们会用$\frac{\partial L(y_i,f(x_i))}{\partial f(x_i)}$来代替残差，训练一棵新的树来拟合残差，对于新树的每个分支，用经验风险最小化来确定代表值
