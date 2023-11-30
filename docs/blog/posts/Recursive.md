---
comments: true
authors:
    - stormckey
categories:
    - PL
date: 2023-11-28
nostatistics: true
---

# Y-combinator 与递归

!!! abstract
    介绍了 lambda 演算中的 Y-combinator,主要是希望用抽象的思想来帮助理解

<!-- more -->

首先请看 xg[:octicons-link-16:的笔记这里](https://note.tonycrane.cc/cs/pl/ppl/topic1/#y-combinator),推导的过程讲的很清楚了。

这里主要讨论另外几个问题

## 不用 Y-combinator 可以吗

当然可以，可以看到文中的`proto proto`本来就是等价于`Y u`的，要用这种方式实现递归主要走以下四步

1. 写出调用自己的那一版的 lambda: $fact_1 = \lambda n . is0\ n\ 1\ ( *\ n\ (fact_1\ (pred\ n)))$
2. 把对自己的调用改成对参数 f 的调用：$fact_2 = \lambda f. \lambda n . is0\ n\ 1\ ( *\ n\ (f\ (pred\ n)))$
3. 把 f 改写成 f f: $fact_3 = \lambda f. \lambda n . is0\ n\ 1\ ( *\ n\ (f\ f\ (pred\ n)))$
4. 对得到的新的 lambda 表达式应用自己：$fact = fact_3\ fact_3$

直接看这玩意还是有点抽象，我们可以用抽象的思想来看看这个东西有哪些性质，而舍去中间化简的细节

=== "$fact_3\ fact_3\ 0 \rightarrow 1$"

    \begin{align}
        &fact_3\ fact_3\ 0  \\
        =& \lambda f. \lambda n .( is0\ n\ 1\ ( *\ n\ (f\ f\ (pred\ n))))\ fact_3\ 0  \\
        =& \lambda n .( is0\ n\ 1\ ( *\ n\ (fact_3\ fact_3\ (pred\ n))))\ 0  \\
        =& is0\ 0\ 1\ ( *\ 0\ (fact_3\ fact_3\ (pred\ 0)))  \\
        =& 1
    \end{align}


=== "$fact_3\ fact_3\ 2 \rightarrow *\ 2\ (fact_3\ fact_3\ 1)$"

    \begin{align}
        &fact_3\ fact_3 2  \\
        =& \lambda f. \lambda n .( is0\ n\ 1\ ( *\ n\ (f\ f\ (pred\ n))))\ fact_3\ 2  \\
        =& \lambda n .( is0\ n\ 1\ ( *\ n\ (fact_3\ fact_3\ (pred\ n))))\ 2  \\
        =& is0\ 2\ 1\ ( *\ 2\ (fact_3\ fact_3\ (pred\ 2)))  \\
        =& *\ 2\ (fact_3\ fact_3\ 1)  \\
    \end{align}

以上，第一个性质是 base case,第二个性质是 indection case,可以显然看出实现了递归

## Y-combinator 的实例

上面那样已经实现了递归，为什么还需要 Y-combinator? 因为上面的实现方法中递归的逻辑和函数的逻辑混在了一起，我们可以把递归的逻辑抽象成 Y,把函数的逻辑抽象成 u,对 Y 应用 u 就得到了递归的 u.具体来说可以分成以下三步

1. 写出调用自己的那一版的 lambda: $fact_1 = \lambda n . is0\ n\ 1\ ( *\ n\ (fact_1\ (pred\ n)))$
2. 把对自己的调用改成对参数 f 的调用：$fact_2 = \lambda f. \lambda n . is0\ n\ 1\ ( *\ n\ (f\ (pred\ n)))$
3. 应用于 Y-combinator: $fact = Y\ fact_2$

可以看到简洁了许多，下面再来介绍一下 Y-combinator 本身，直接看他的内容的话也是一坨，我们可以利用抽象的思想，不管他的内容，也不在乎化简的细节，只看几个性质：

=== "$Y\ fact_2 \rightarrow fact_2\ (Y\ fact_2)$"

    \begin{aligned}
        &Y\ fact_2  \\
        =& (\lambda f. fact_2\ (f\ f)) (\lambda f. fact_2\ (f\ f))  \\
        =& fact_2\ ((\lambda f. fact_2\ (f\ f)) (\lambda f. fact_2\ (f\ f)))  \\
        =& fact_2\ (Y\ fact_2)  \\
    \end{aligned}

=== "$Y\ fact_2\ 0 \rightarrow 1$"

    \begin{aligned}
        &Y\ fact_2\ 0  \\
        =& fact_2\ (Y\ fact_2)\ 0  \\
        =& \lambda f. \lambda n .( is0\ n\ 1\ ( *\ n\ (f\ (pred\ n))))\ (Y\ fact_2)\ 0  \\
        =& \lambda n .( is0\ n\ 1\ ( *\ n\ ((Y\ fact_2)\ (pred\ n))))\ 0  \\
        =& is0\ 0\ 1\ ( *\ 0\ ((Y\ fact_2)\ (pred\ 0)))  \\
        =& 1
    \end{aligned}

=== "$Y\ fact_2\ 2 \rightarrow *\ 2\ (Y\ fact_2\ 1)$"

    \begin{aligned}
        &Y\ fact_2\ 2  \\
        =& fact_2\ (Y\ fact_2)\ 2  \\
        =& \lambda f. \lambda n .( is0\ n\ 1 ( *\ n\ (f\ (pred\ n)))) (Y\ fact_2)\ 2  \\
        =& \lambda n .( is0\ n\ 1\ ( *\ n\ ((Y\ fact_2)\ (pred\ n))))\ 2  \\
        =& is0\ 2\ 1\ ( *\ 2\ ((Y\ fact_2)\ (pred\ 2)))  \\
        =& *\ 2\ (Y\ fact_2\ 1)
    \end{aligned}

以上，可以看到其性质有

1. 在前面凭空多应用一次 fact_2
2. base case
3. induction case

以上推导的比较吊诡的地方是需要以这种运算顺序才好出结果，虽然我们这里对有好几个子项的时候先演算什么并没有规定

有以上性质，毫无疑问$Y fact_2$也实现了递归

!!! reference
    - [:octicons-book-16: Lambda 演算](https://note.tonycrane.cc/cs/pl/ppl/topic1/#y-combinator)
    - [:octicons-book-16: Recursive Lambda Functions the Y-Combinator](https://sookocheff.com/post/fp/recursive-lambda-functions/)
